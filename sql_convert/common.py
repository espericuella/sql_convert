import re
from sql_convert.includes.field_definition import FieldDefinition


def camel_to_kebab(stroke: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '-', stroke).lower()


def capitalize(stroke: str) -> str:
    return stroke[0].upper() + stroke[1:]


def snake_to_camel(stroke: str, set_capitalize: bool = True) -> str:
    word = stroke
    if set_capitalize:
        word = stroke[0].upper() + stroke[1:]
    return re.sub(r'_([a-z])', lambda match: match.group(1).upper(), word)


def snake_to_dash(stroke: str) -> str:
    return stroke.lower().replace('_', '-')


def is_number(item: FieldDefinition) -> bool:
    return item['type'].upper() in ['INT4', 'INT8', 'INTEGER', 'INT']


def is_string(item: FieldDefinition) -> bool:
    return item['type'].upper() in ['VARCHAR', 'BPCHAR', 'TEXT']


def is_boolean(item: FieldDefinition) -> bool:
    return item['type'].upper() in ['BOOL', 'BOOLEAN']


def is_date(item: FieldDefinition) -> bool:
    return item['type'].upper() in ['DATE', 'TIMESTAMP']


def get_description(tbl_name: str, field_name: str, sql_file_content: str) -> str:
    response = field_name
    for line in sql_file_content.split('\n'):
        elems = line.strip().split()
        if len(elems) < 6:
            continue
        if elems[0].upper() != 'COMMENT':
            continue
        if elems[1].upper() != 'ON':
            continue
        if elems[2].upper() != 'COLUMN':
            continue
        if f'{tbl_name.upper()}.{field_name.upper()}' not in elems[3].upper():
            continue
        desc_arr = line.strip().split("'")
        response = desc_arr[1]
        break
    return response
