from dagster import (
    Field,
    solid,
    pipeline,
    execute_pipeline,
    composite_solid,
    InputDefinition,
    Shape,
    repository,
    Output,
    ExpectationResult,
    EventMetadataEntry,
)
from my_custom_dagster_type import NotZero

"""This repo uses config mapping to supply computation pipelines with multiple solid config schemas. """


@solid(
    config_schema={
        "cluster_cfg": Shape({"%": int, "ave": int}),
        "operator": Field(str, is_required=False, default_value="ave"),
    },
)
def operate_two_nums(context, nums: list):
    if context.solid_config["operator"] == "ave":
        x = context.solid_config["cluster_cfg"]["ave"]
        answer = (nums[1] + nums[0]) / x
        context.log.info(f"The average of the two numbers is: {answer}")
        return answer  # 150

    elif context.solid_config["operator"] == "subtract":
        return nums[1] - nums[0]

    elif context.solid_config["operator"] == "divide":
        y = context.solid_config["cluster_cfg"]["%"]
        return (nums[1] / nums[0]) * y  # (200 / 100) * 100 = 200

    elif context.solid_config["operator"] == "multiply":
        return nums[1] * nums[0]


@solid
def combine(_context, num1, num2):
    result = num2 + num1
    # Use EventMetadataEntry.text to view result against expected result description
    # In dagit Expectation: success -> green, failure -> yellow
    yield ExpectationResult(
        success=result > 0,
        description="ensure positive result",
        metadata_entries=[
            EventMetadataEntry.text("{result}".format(result=result), label="combine result")
        ],
    )
    yield Output(result)


def config_mapping_fn(cfg):
    # if missing solid name res1, res 2, will raise Undefined field "solids" at path root error,
    # which means configured_composite_solid_cannot_stub_inner_solids_config
    # so fully configure the solids here
    # cfg: parse in runtime config
    return {
        "res1": {
            "config": {
                "cluster_cfg": {"%": 100, "ave": 2},
                # "operator": "ave" # (by default, operator will be "ave")
            }
        },
        "res2": {
            "config": {
                "cluster_cfg": {"%": 100, "ave": 2},
                "operator": cfg["operator"]  # can be provided by run_config
                # can also hard code value "divide" or "ave"
                # "operator" : "divide"
            }
        },
    }


@composite_solid(
    config_fn=config_mapping_fn,
    config_schema={"operator": Field(str, is_required=False, default_value="divide")},
)
def example_computation(nums: list):
    res1 = operate_two_nums.alias("res1")
    res2 = operate_two_nums.alias("res2")

    return combine(res1(nums), res2(nums))  # pylint: disable=no-value-for-parameter


@pipeline
def example_computation_pipeline():
    example_computation()  # pylint: disable=no-value-for-parameter


@repository
def config_mapping():
    return [example_computation_pipeline]


if __name__ == "__main__":
    execute_pipeline(
        example_computation_pipeline,
        run_config={  # there's default value so the run_config is optional
            "solids": {
                "example_computation": {
                    # "inputs": {"nums": [{"value": 100}, {"value": 200}]},
                    "inputs": {"nums": [{"json": {"path": "inputs.json"}}, {"value": 200}]},
                    # "inputs": {"nums": [{"pickle": {"path": "data.pickle"}}, {"value": 200}]},
                    "config": {"operator": "divide"},
                }
            }
        },
    )
