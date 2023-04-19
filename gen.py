import sys
import os
import re
import shutil
from sql_convert.common import get_description
from sql_convert.api import generate_api
from sql_convert.sql import generate_sql
from sql_convert.www import generate_angular_module

# Remove dist directory if exists
if os.path.exists('dist'):
    shutil.rmtree('dist', ignore_errors=True)

# Get command line arguments
args = sys.argv[1:]
if not args:
    print('Add SQL file with table definition')
    sys.exit(-1)

# Check if the input file exists
if not os.path.exists(args[0]):
    print('File not exist')
    sys.exit(-1)

# Check if the input file is a SQL file
if not args[0].upper().endswith('.SQL'):
    print('File is not SQL file')
    sys.exit(-1)

# Read the input SQL file
with open(args[0], 'r') as f:
    sql_file = f.read()

# Analyze and process SQL table definition
tbl_name = ''
schema_name = ''
sequence_name = ''

field_array = list()
for line in sql_file.split('\n'):
    elems = re.split(r'\s+', line.strip())
    if elems[0].upper() == 'COMMENT':
        continue
    elif elems[0].upper() == 'CREATE':
        if not elems[2].split('.')[1]:
            schema_name = 'public'
            tbl_name = elems[2].split('.')[0]
        else:
            schema_name = elems[2].split('.')[0]
            tbl_name = elems[2].split('.')[1]
        continue
    elif elems[0] in ['(', ')', '', ');']:
        continue
    else:
        field_array.append({
            "field": elems[0],
            "type": elems[1].upper(),
            "not_null": 'NOT NULL' in line.upper(),
            "description": get_description(tbl_name, elems[0], sql_file)
        })
        # Check sequence name
        nextVal = line.upper().find('NEXTVAL(')
        if nextVal >= 0:
            lastElem = line.find("'", nextVal + 9)
            sequence_name = line[nextVal + 9:lastElem]
            # print('line: ', line)
            # print('Sequence line', nextVal, lastElem, sequenceName)

if not schema_name:
    print('Table should have schema defined')
    sys.exit(-1)

generate_api(schema_name, tbl_name, field_array)

generate_sql(schema_name, tbl_name, sequence_name, field_array)

generate_angular_module(schema_name, tbl_name, field_array)
