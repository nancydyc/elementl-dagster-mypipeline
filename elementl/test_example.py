from d_type import compute_pipeline
from resource_pipeline import resource_pipeline
from combination_pipeline import combination_pipeline
from selector import selector_pipeline
from definition import definition_pipeline, PositiveNumber
from composite_solid import composite_solid_pipeline
from config_mapping_and_expectation_result import example_computation_pipeline
from add_string_numbers import add_pipeline

from dagster import execute_pipeline, check_dagster_type, Failure


def test_resource_pipeline_1():
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
    assert result.success
    assert result.result_for_solid("compute_two_nums").output_value() == 8


def test_resource_pipeline_2():
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
                    "config": {"operator": "divide"}
                }            
            } 
        }
    )
    assert result.success
    assert result.result_for_solid("compute_two_nums").output_value() == 0.5


def test_combination_pipeline():
    result = execute_pipeline(
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
    assert result.success
    assert result.result_for_solid("multiply_three_numbers").output_value() == 96
    assert len(result.solid_result_list) == 4
    for solid_res in result.solid_result_list:
        assert solid_res.success # assert the success of each step


def test_selector_pipeline_1():
    result = execute_pipeline(
        selector_pipeline,
        run_config={
            "solids": {
                "compute_two_nums": {
                    "inputs": {"num1": 2, "num2": 4},
                    "config": {"divide": {"operator": True}},
                }
            }
        }
    )
    assert result.success
    assert result.result_for_solid("compute_two_nums").output_value() == 0.5


def test_selector_pipeline_2():
    result = execute_pipeline(
        selector_pipeline,
        run_config={
            "solids": {
                "compute_two_nums": {
                    "inputs": {"num1": 2, "num2": 4},
                    "config": {"multiply": {"operator": True}},
                }
            }
        }
    )
    assert result.success
    assert result.result_for_solid("compute_two_nums").output_value() == 8


def test_definition_pipeline():
    result = execute_pipeline(
        definition_pipeline,
        run_config={
            "solids": {
                "compute_two_nums": {
                    "inputs": {"num1": 2, "num2": 4},
                    "config": {"operator": "divide"}
                }
            }
        }
    )
    assert result.success
    assert result.result_for_solid("compute_two_nums").output_value() == 0.5


def test_positive_num():
    """To test custom types, use check_dagster_type, 1st arg is your customized type, 2nd arg is runtime value"""

    assert check_dagster_type(
        PositiveNumber, 2
    )
    type_check = check_dagster_type(
        PositiveNumber, 0
    )
    assert not type_check.success
    assert type_check.description == (
        "Numbers cannot be 0 or negative, got 0 for PositiveNumber type"
    )


def test_composite_solid_pipeline():
    result = execute_pipeline(
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
    assert result.success
    assert result.result_for_solid("mix_computation").output_value() == 24


def test_example_computation_pipeline():
    result = execute_pipeline(
        example_computation_pipeline,
        run_config={ # this run_config is optional since there's default value
            "solids": {
                "example_computation": {
                    "inputs": {"nums": [{"value": 100}, {"value": 200}]},
                    "config": {"operator": "divide"}
                }
            }
        }
    )
    assert result.success
    assert result.result_for_solid("example_computation").output_value() == 350


def test_python_object_dagster_type():
    result = execute_pipeline(
        compute_pipeline,
        run_config={
            "solids": {"add_two_nums": {"inputs": {"num1": 2, "num2": 3}}}
        },
    )
    assert result.success
    assert result.result_for_solid("divide_a_hundred").output_value() == 5


def test_add_pipeline():
    result = execute_pipeline(
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
    assert result.success
    assert result.result_for_solid("add").output_value() == 3
