from dagster import DagsterType, dagster_type_loader, execute_pipeline, Int, solid, pipeline, PythonObjectDagsterType, ExpectationResult, EventMetadataEntry, Output

import typing

# def positive_num_check(_, value):
#     return True if value > 0 else False


@dagster_type_loader(Int) # int works, but Field(Int) raise error
def positive_num_loader(_context, value):
    """ The second parameter for this loader, value, contains the value of the inputs paras num1 and num2.
        The loader transfers the value in run_config to the solid whose data are not produced by a dependency.
    """
    return value


# How to use PythonObjectDagsterType
class PercentType:
    """Transfer the input value to 100 times. """ # pylint: disable=too-few-public-methods
    def __init__(self, number):
        self.value = number * 100

PercentDagsterType = PythonObjectDagsterType(PercentType, name="PercentDagsterType")

# MyPy Compliance
# typing.TYPE_CHECKING: it is A special constant that is assumed to be True by 3rd party static type checkers(mypy package). It is False at runtime.
if typing.TYPE_CHECKING: # static check
    PositiveNumber = str # it should be int, but str type doesn't affect runtime result
else: # runtime
    PositiveNumber = DagsterType(
        name="PositiveNumber",
        type_check_fn=lambda _, value: value > 0,
        loader=positive_num_loader,
        description="A number greater than 0."
    )


@solid
def add_two_nums(_context, num1: PositiveNumber, num2: PositiveNumber) -> PercentDagsterType: # catches the input type error if not int or not positive
    adding = num1 + num2 # 2 + 3 => 5
    add_percent_type = PercentType(adding) # object 5
    yield ExpectationResult(
        success=add_percent_type.value > 100, # value is 500
        description="ensure PercentType gets a number greater than 100",
        metadata_entries=[
            EventMetadataEntry.text("{result}".format(result=add_percent_type), label="transfer to percent type")
        ])
    yield Output(add_percent_type) # object 5


@solid
def divide_a_hundred(_context, num: PercentDagsterType):
    return num.value / 100 # 500 /100


@pipeline
def compute_pipeline():
    divide_a_hundred(add_two_nums()) # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    execute_pipeline(
        compute_pipeline,
        run_config={
            "solids": {"add_two_nums": {"inputs": {"num1": 2, "num2": 3}}}
        },
    )
