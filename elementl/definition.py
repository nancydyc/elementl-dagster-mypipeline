from dagster import (
    Failure,
    Field,
    InputDefinition,
    solid,
    String,
    Output,
    pipeline,
    execute_pipeline,
    dagster_type_loader,
    DagsterType,
    Selector,
)

""" Create solid that multiplies or divides two numbers, where a config value sets whether you multiply or divide."""

# from my_custom_dagster_type import PositiveNumber # this statement is the same as the three blocks below
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
# end PositiveNumber def

@solid(
    config_schema=Field(
        Selector({"operator": str}) # one key value pair works for selector
    ),
    input_defs=[InputDefinition("num1", PositiveNumber), InputDefinition("num2", PositiveNumber)]
)
def compute_two_nums(context, num1, num2):
    if "multiply" in context.solid_config["operator"]:
        yield Output(num1 * num2)
    if "divide" in context.solid_config["operator"]:
        yield Output(num1 / num2)


@pipeline
def definition_pipeline():
    compute_two_nums()

    
if __name__ == "__main__":
    execute_pipeline(
        definition_pipeline,
        run_config={
            "solids": {
                "compute_two_nums": {
                    "inputs": {"num1": 2, "num2": 4},
                    "config": {"operator": "divide"},
                }
            }
        },
    )