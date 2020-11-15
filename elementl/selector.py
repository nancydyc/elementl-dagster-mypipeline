from dagster import (
    Field,
    solid,
    String,
    pipeline,
    execute_pipeline,
    dagster_type_loader,
    DagsterType,
    Selector,
)

""" Create solid that multiplies or divides two numbers, where a config value sets whether you multiply or divide."""


def positive_num_check(_, value):
    return True if value > 0 else False


@dagster_type_loader(int)
def positive_num_loader(_context, value):
    return value


PositiveNumber = DagsterType(
    name="PostivieNumber",
    description="Only take in numbers greater than zero",
    type_check_fn=positive_num_check,
    loader=positive_num_loader,
)


@solid(
    config_schema=Field(
        Selector({"multiply": {"operator": bool}, "divide": {"operator": bool}}) # not very good semantics
    )
)
def compute_two_nums(context, num1: PositiveNumber, num2: PositiveNumber):
    if "multiply" in context.solid_config:
        return num1 * num2
    if "divide" in context.solid_config:
        return num1 / num2


@pipeline
def selector_pipeline():
    compute_two_nums()


if __name__ == "__main__":
    execute_pipeline(
        selector_pipeline,
        run_config={
            "solids": {
                "compute_two_nums": {
                    "inputs": {"num1": 2, "num2": 4},
                    "config": {"multiply": {"operator": True}},
                }
            }
        },
    )