from dagster import (
    solid,
    pipeline,
    execute_pipeline
)
from my_custom_dagster_type import StringNumber

@solid
def add(_context, a: StringNumber, b: StringNumber):
    return a + b

@pipeline
def add_pipeline():
    add()  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    execute_pipeline(
        add_pipeline,
        run_config={
            "solids": {
                "add": {
                    "inputs": {
                        "a": "one", "b": "two"
                    }
                }
            }
        }
    )
