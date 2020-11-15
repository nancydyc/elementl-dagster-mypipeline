from dagster import solid, pipeline, execute_pipeline, dagster_type_loader, DagsterType, composite_solid


from example import add_two_nums
from my_custom_dagster_type import PositiveNumber

""" Write a pipeline that execute a composite solid. """


@solid
def add_two_nums(_context, num1: PositiveNumber, num2: PositiveNumber):
    return num1 + num2


@solid
def multiply_two_numbers(_context, num1: PositiveNumber, num2: PositiveNumber):
    return num1 * num2


@composite_solid
def mix_computation():
    res1 = add_two_nums.alias("res1")
    res2 = add_two_nums.alias("res2")
    return multiply_two_numbers(res1(), res2())


@pipeline
def composite_solid_pipeline():
    mix_computation()


if __name__ == "__main__":
    execute_pipeline(
        composite_solid_pipeline,
        run_config={
            "solids": {
                "mix_computation": {
                    "solids": {
                        "res1": {
                            "inputs": {"num1": 2, "num2": 4}
                        },
                        "res2": {
                            "inputs": {"num1": 1, "num2": 3}
                        }
                    }
                }
            }
        }
    )