from dagster import (
    Failure,
    Field,
    solid,
    String,
    pipeline,
    execute_pipeline,
    dagster_type_loader,
    DagsterType,
    Selector,
    resource,
    ModeDefinition
)

import operator

""" Create solid that multiplies or divides two numbers, where a config value in resources sets whether you multiply or divide."""


def positive_num_check(_, value):
    if value > 0:
        return True 
    else:
        raise Failure(
        "Numbers cannot be 0 or negative, got {num} for PositiveNumber type".format(num=value)
    )


@dagster_type_loader(int)
def positive_num_loader(_context, value):
    return value


PositiveNumber = DagsterType(
    name="PostivieNumber",
    description="Only take in numbers greater than zero",
    type_check_fn=positive_num_check,
    loader=positive_num_loader,
)


@resource(
    config_schema={
        "operator": str
    }
)
def choose_operator(context):
    if context.resource_config["operator"] == "divide":
        return operator.truediv
    if context.resource_config["operator"] == "multiply":
        return operator.mul


@solid(required_resource_keys={"operator"})
def compute_two_nums(context, num1: PositiveNumber, num2: PositiveNumber):
    return context.resources.operator(num1, num2)


@pipeline(
    mode_defs=[
        ModeDefinition("default", resource_defs={"operator": choose_operator} )
    ] # mode is where resource be defined
)
def resource_pipeline():
    compute_two_nums()


if __name__ == "__main__":
    result = execute_pipeline(
        resource_pipeline,
        run_config={
            "solids": {
                "compute_two_nums": {
                    "inputs": {"num1": 2, "num2": 4}
                }
            },
            "resources": {
                "operator": {
                    "config": {"operator": "multiply"}
                }            
            } 
        }
    )
