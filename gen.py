import sys
import os
import re
import shutil
import argparse
from sql_convert.common import get_description
from sql_convert.rest.nestjs import generate_nestjs_api
from sql_convert.sql.pgsql import generate_pgsql
from sql_convert.web.ng import generate_angular_module

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-b", "--rest", action="store_true", help="Destination backend rest api")
parser.add_argument("-f", "--web", action="store_true", help="Destination frontend framework")
parser.add_argument("-s", "--sql", action="store_true", help="Destination SQL language")
parser.add_argument("<path_to_sql>", help="Path to SQL generation table")
args = parser.parse_args()
config = vars(args)

# Remove dist directory if exists
if os.path.exists('dist'):
    shutil.rmtree('dist', ignore_errors=True)

# Check if sql table file defined in command line arguments
sql_file_path = config['<path_to_sql>']

if not config['<path_to_sql>']:
    print('Add SQL file with table definition')
    sys.exit(-1)

# Check if the input file exists
if not os.path.exists(sql_file_path):
    print('File not exist')
    sys.exit(-1)

# Check if the input file is a SQL file
if not sql_file_path.upper().endswith('.SQL'):
    print('File is not SQL file')
    sys.exit(-1)

# Read the input SQL file
with open(sql_file_path, 'r') as f:
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

if config['sql'] is False and config['web'] is False and config['rest'] is False:
    print('No options selected. Please select an option to generate [-b, -f, -s]')
    sys.exit(-1)

if config['rest'] is True:
    generate_nestjs_api(schema_name, tbl_name, field_array)
    print('NestJS API successfully generated')

if config['web'] is True:
    generate_angular_module(schema_name, tbl_name, field_array)
    print('Angular module successfully generated')

if config['sql'] is True:
    generate_pgsql(schema_name, tbl_name, sequence_name, field_array)
    print('PostgreSQL functions successfully generated')
