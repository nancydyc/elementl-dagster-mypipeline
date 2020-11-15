from dagster import DagsterType, dagster_type_loader, execute_pipeline, Int, solid, pipeline, PythonObjectDagsterType, ExpectationResult, EventMetadataEntry, Output, InputDefinition, OutputDefinition

import typing

def positive_num_check(_, value):
    return True if value > 0 else False


@dagster_type_loader(Int) # int works, but Field(Int) raise error
def positive_num_loader(_context, value):
    """ The second parameter for this loader, value, contains the value of the inputs paras num1 and num2.
        The loader transfers the value in run_config to the solid whose data are not produced by a dependency.
    """
    return value


PositiveNumber = DagsterType(
    name="PostivieNumber",
    description="Only take in numbers greater than zero",
    type_check_fn=positive_num_check,
    loader=positive_num_loader
)


# How to use PythonObjectDagsterType
class PercentType:
    def __init__(self, number):
        self.value = number * 100

PercentDagsterType = PythonObjectDagsterType(PercentType, name="PercentDagsterType")


@solid(
    input_defs=[InputDefinition("num1", PositiveNumber), InputDefinition("num2", PositiveNumber)],
    output_defs=[OutputDefinition(PercentDagsterType)] # mypy compliance
)
@solid
def add_two_nums(_context, num1: PositiveNumber, num2: PositiveNumber): # mypy compliance only works for naked python type
    adding = num1 + num2 # 2 + 3 => 5
    add_percent_type = PercentType(adding) # object 5
    yield ExpectationResult(
        success=add_percent_type.value > 100, # value is 500
        description="ensure PercentType gets a number greater than 100",
        metadata_entries=[
            EventMetadataEntry.text("{result}".format(result=add_percent_type), label="transfer to percent type")
        ])
    yield Output(add_percent_type) # object 5


@solid(input_defs=[InputDefinition("num", PercentDagsterType)])
def divide_a_hundred(_context, num):
    return num.value / 100 # 500 /100


@pipeline
def compute_pipeline():
    divide_a_hundred(add_two_nums())



if __name__ == "__main__":
    execute_pipeline(
        compute_pipeline,
        run_config={
            "solids": {"add_two_nums": {"inputs": {"num1": 0, "num2": 3}}}
        },
    )
