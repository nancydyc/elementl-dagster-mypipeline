from dagster import solid, pipeline, execute_pipeline, dagster_type_loader, DagsterType
from d_type import add_two_nums

""" Write a pipeline that looks like multiply_two_numbers(add_two_numbers(), add_two_numbers())
"""

def positive_num_check(_, value):
    return True if value > 0 else False


@dagster_type_loader(int)
def positive_num_loader(_context, value):
    return value


PositiveNumber = DagsterType(
    name="PostivieNumber",
    description="Only take in numbers greater than zero",
    type_check_fn=positive_num_check,
    loader=positive_num_loader
)


@solid
def add_two_nums(_context, num1: PositiveNumber, num2: PositiveNumber):
    return num1 + num2


@solid
def multiply_three_numbers(_context, num1: PositiveNumber, num2: PositiveNumber, num3: PositiveNumber):
    return num1 * num2 * num3


@pipeline
def combination_pipeline():
    multiply_three_numbers(add_two_nums(), add_two_nums(), add_two_nums())


if __name__ == "__main__":
    execute_pipeline(
        combination_pipeline,
        run_config={
            "solids": {
                "add_two_nums": {
                    "inputs": {"num1": 2, "num2": 4}
                },
                "add_two_nums_2": { # add 2 for the same solid
                    "inputs": {"num1": 1, "num2": 3}
                },
                "add_two_nums_3": { # cannot skip 3 to name it 4
                    "inputs": {"num1": 1, "num2": 3}
                }
            }
        }
    )