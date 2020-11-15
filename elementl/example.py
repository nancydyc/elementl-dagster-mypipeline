from dagster import solid

@solid
def add_two_nums(_context, num1, num2):
    return num1 + num2