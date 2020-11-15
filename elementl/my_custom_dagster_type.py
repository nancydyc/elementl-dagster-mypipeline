from dagster import DagsterType, dagster_type_loader, check, check_dagster_type, TypeCheck, EventMetadataEntry

# ensure inputs are positive numbers
def positive_num_check(_, value):
    # return True if value > 0 else False
    if value <= 0:
        return TypeCheck(
            success=False,
            description=(
                "Numbers cannot be 0 or negative, got "
                "{value} for PositiveNumber type"
            ).format(value=value),
            metadata_entries=[
                EventMetadataEntry.int(
                    value,
                    "The input number"
                )
            ]
        )
    else:
        return True


@dagster_type_loader(int)
def positive_num_loader(_context, value):
    return value


PositiveNumber = DagsterType(
    name="PostivieNumber",
    description="Numbers cannot be 0 or negative",
    type_check_fn=positive_num_check,
    loader=positive_num_loader
)


# check input value is not zero
def not_zero_type_check(_, values):
    for value in values:
        if value == 0:
            return False
    return True


@dagster_type_loader(list)
def not_zero_type_loader(_context, values):
    return values


NotZero = DagsterType(
    name="NotZero",
    description="No zero in the list of numbers",
    type_check_fn=not_zero_type_check,
    loader=not_zero_type_loader
)


# load string value and convert to int
# Then check if value is int
# load fn runs before type check fn
def check_string(_, value):
    return type(value) == int


@dagster_type_loader(str)
def load_string_num(_, value):
    if value == "one":
        return 1
    if value == "two":
        return 2


StringNumber = DagsterType(
    name="StringNumber",
    description="transfer a string to a number",
    type_check_fn=check_string,
    loader=load_string_num
)


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