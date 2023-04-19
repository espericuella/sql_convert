import os
from typing import List

from sql_convert.interfaces.interfaces import FieldDefinition
from sql_convert.common import capitalize, is_number, is_boolean, is_string, snake_to_camel, snake_to_dash, camel_to_kebab


# Generate API NestJS templates
def generate_model_dto(schema_name: str, tbl_name: str, field_array: List[FieldDefinition]):
    # model dto
    dto_name = f"{snake_to_camel(tbl_name)}Dto"
    ts_dto = f"""import {{ ApiProperty }} from '@nestjs/swagger';
import {{ IsNotEmpty, IsNumber, IsString, IsOptional }} from 'class-validator';
export class {dto_name} {{\n"""
    for item in field_array:
        # Set swagger decorators
        ts_type = 'string'
        if is_number(item):
            ts_type = 'number'
        if is_boolean(item):
            ts_type = 'boolean'
        if item['not_null'] is True:
            ts_dto += '   @IsNotEmpty()\n'
        if is_number(item):
            ts_dto += '   @IsNumber()\n'
        if is_string(item):
            ts_dto += '   @IsString()\n'
        if item['not_null'] is not True and (is_number(item) or is_string(item)):
            ts_dto += '   @IsOptional()\n'
        ts_dto += f"""   @ApiProperty({{
    description: '{item['description']}',
    type: '{ts_type}',
    example: '',
  }})\n"""
    ts_dto += f' {item["field"]}: {ts_type}\n\n'
    ts_dto += '}'
    file_path = os.path.join('dist', 'api', snake_to_dash(tbl_name), 'implement', f'{camel_to_kebab(snake_to_camel(tbl_name))}.dto.ts')
    os.makedirs(os.path.join('dist', 'api', snake_to_dash(tbl_name), 'implement'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(ts_dto)


# FilterItem.dto.ts - NestJS global definition
def generate_filter_item_dto():
    # FilterItem Dto
    ts_filter_dto = (
        "import { ApiProperty } from '@nestjs/swagger';\n"
        "import { IsString } from 'class-validator';\n"
        "export class FilterItemDto {\n"
        "  @IsString()\n"
        "  @ApiProperty({\n"
        "    description: 'Field name to be search on',\n"
        "    type: 'string',\n"
        "    example: 'name',\n"
        "  })\n"
        "  field: string;\n"
        "  @IsString()\n"
        "  @ApiProperty({\n"
        "    description: 'Search value',\n"
        "    type: 'string',\n"
        "    example: 'Kowalski',\n"
        "  })\n"
        "  value: string;\n"
        "}\n"
    )
    file_path = os.path.join('dist', 'api', 'shared', 'implement', 'filter-item.dto.ts')
    os.makedirs(os.path.join('dist', 'api', 'shared', 'implement'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(ts_filter_dto)


# ListFilterRequest.dto  - NestJS global definition
def generate_list_filter_request_dto():
    ts_item = """import { ApiProperty } from '@nestjs/swagger';
import { IsArray, IsNotEmpty, IsNumber, IsString, IsOptional } from 'class-validator';
import { FilterItemDto } from './FilterItem.dto';
export class ListFilterRequestDto {
  @IsArray()
  @ApiProperty({
    description: 'List filtered fields with search values',
    type: [FilterItemDto],
    required: false,
  })
  filter: FilterItemDto[];
  
  @IsString()
  @ApiProperty({
    description: 'Sort direction',
    type: 'string',
    enum: ['asc', 'desc', ''],
    example: 'asc',
  })
  sort_direction: string;
  
  @IsArray()
  @IsOptional()
  @ApiProperty({
    description: 'Fields to be sorted',
    type: 'array',
    items: {
      type: 'string',
    },
    example: '[\\'name\\', \\'surname\\']',
    required: false,
  })
  sort?: string[];
  
  @IsNotEmpty()
  @IsNumber()
  @ApiProperty({
    description: 'Page index',
    type: 'number',
    example: 1,
  })
  page_index: number;
  
  @IsNotEmpty()
  @IsNumber()
  @ApiProperty({
    description: 'Page size',
    type: 'number',
    example: 25,
  })
  page_size: number;
}"""
    file_path = os.path.join('dist', 'api', 'shared', 'implement', 'list-filter-request.dto.ts')
    os.makedirs(os.path.join('dist', 'api', 'shared', 'implement'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(ts_item)


# List Response Dto
def generate_list_response_dto(schema_name: str, tbl_name: str):
    ts_list_response_dto = f"""import {{ IsNumber }} from 'class-validator';
import {{ ApiProperty }} from '@nestjs/swagger';
import {{ {snake_to_camel(tbl_name)}Dto }} from './{snake_to_camel(tbl_name)}.dto';
export class {snake_to_camel(tbl_name)}ListResponseDto {{
  @IsNumber()
  @ApiProperty({{
    description: 'Table item count',
    type: 'number',
    example: '1000',
  }})
  cnt: number;
  @ApiProperty({{
    description: 'Response item array',
    type: [{snake_to_camel(tbl_name)}Dto],
    example: [],
  }})
  data: {snake_to_camel(tbl_name)}Dto[];
}}"""
    file_path = os.path.join('dist', 'api', snake_to_dash(tbl_name), 'implement', f'{camel_to_kebab(snake_to_camel(tbl_name))}list-response.dto.ts')
    os.makedirs(os.path.join('dist', 'api', snake_to_dash(tbl_name), 'implement'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(ts_list_response_dto)


# Controller
def generate_controller(schema_name: str, tbl_name: str):
    ts_controller = f"""import {{ ApiBearerAuth, ApiResponse, ApiTags }} from '@nestjs/swagger';
import {{
  Body, Controller, Delete, Get, HttpCode, HttpStatus, Param, Post, UseGuards,
}} from '@nestjs/common';
import {{ Observable }} from 'rxjs';
import {{ AuthGuard }} from '../shared/guards/auth.guard';
import {{ {snake_to_camel(tbl_name)}Dto }} from './implement/{snake_to_camel(tbl_name)}.dto';
import {{ {snake_to_camel(tbl_name)}ListResponseDto }} from './implement/{camel_to_kebab(snake_to_camel(tbl_name))}list-response.dto';
import {{ ListFilterRequestDto }} from '../shared/implement/list-filter-request.dto';
import {{ {snake_to_camel(tbl_name)}Service }} from './{snake_to_dash(tbl_name)}.service';\n
@ApiTags('{tbl_name}')
@ApiBearerAuth('Bearer')
@UseGuards(AuthGuard)
@Controller('{tbl_name}')
export class {snake_to_camel(tbl_name)}Controller {{
  constructor(
    private {snake_to_camel(tbl_name, False)}Service: {snake_to_camel(tbl_name)}Service,
  ) {{}}
    
  @Post('list')
  @HttpCode(HttpStatus.OK)
  @ApiResponse({{ status: HttpStatus.INTERNAL_SERVER_ERROR, description: 'Database error' }})
  @ApiResponse({{ status: HttpStatus.FORBIDDEN, description: 'Invalid credentials' }})
  @ApiResponse({{ status: HttpStatus.TOO_MANY_REQUESTS, description: 'Too many requests' }})
  @ApiResponse({{ status: HttpStatus.OK, description: 'Response with list', type: {snake_to_camel(tbl_name)}ListResponseDto }})
  list(@Body() filter: ListFilterRequestDto): Observable< {snake_to_camel(tbl_name)}ListResponseDto > {{
    return this.{snake_to_camel(tbl_name, False)}Service.list(filter);
  }}
  @Get(':id')
  @HttpCode(HttpStatus.OK)
  @ApiResponse({{ status: HttpStatus.INTERNAL_SERVER_ERROR, description: 'Database error' }})
  @ApiResponse({{ status: HttpStatus.FORBIDDEN, description: 'Invalid credentials' }})
  @ApiResponse({{ status: HttpStatus.TOO_MANY_REQUESTS, description: 'Too many requests' }})
  @ApiResponse({{ status: HttpStatus.OK, description: 'Response description', type: {snake_to_camel(tbl_name)}Dto }})
  get(@Param('id') id: number): Observable< {snake_to_camel(tbl_name)}Dto > {{
    return this.{snake_to_camel(tbl_name, False)}Service.get(id);
  }}
  @Post()
  @HttpCode(HttpStatus.OK)
  @ApiResponse({{ status: HttpStatus.INTERNAL_SERVER_ERROR, description: 'Database error' }})
  @ApiResponse({{ status: HttpStatus.FORBIDDEN, description: 'Invalid credentials' }})
  @ApiResponse({{ status: HttpStatus.TOO_MANY_REQUESTS, description: 'Too many requests' }})
  @ApiResponse({{ status: HttpStatus.NOT_FOUND, description: 'Item not found' }})
  @ApiResponse({{ status: HttpStatus.OK, description: 'Response with id' }})
  save(@Body() {snake_to_camel(tbl_name, False)}: {capitalize(snake_to_camel(tbl_name))}Dto) {{
    return this.{snake_to_camel(tbl_name, False)}Service.save({snake_to_camel(tbl_name, False)});
  }}
  @Delete(':id')
  @HttpCode(HttpStatus.OK)
  @ApiResponse({{ status: HttpStatus.INTERNAL_SERVER_ERROR, description: 'Database error' }})
  @ApiResponse({{ status: HttpStatus.FORBIDDEN, description: 'Invalid credentials' }})
  @ApiResponse({{ status: HttpStatus.TOO_MANY_REQUESTS, description: 'Too many requests' }})
  @ApiResponse({{ status: HttpStatus.NOT_FOUND, description: 'Item not found' }})
  @ApiResponse({{ status: HttpStatus.OK, description: 'Deleted' }})
  delete(@Param('id') id: number) {{
    return this.{snake_to_camel(tbl_name, False)}Service.delete(id);
  }}
}}"""
    file_path = os.path.join('dist', 'api', snake_to_dash(tbl_name), f'{snake_to_dash(tbl_name)}.controller.ts')
    os.makedirs(os.path.join('dist', 'api', snake_to_dash(tbl_name)), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(ts_controller)


def generate_service(schema_name: str, tbl_name: str):
    ts_service = f"""import {{ HttpException, Injectable }} from '@nestjs/common';
import {{ Observable }} from 'rxjs';
import {{ {snake_to_camel(tbl_name)}Dto }} from './implement/{camel_to_kebab(snake_to_camel(tbl_name))}.dto';
import {{ {snake_to_camel(tbl_name)}ListResponseDto }} from './implement/{camel_to_kebab(snake_to_camel(tbl_name))}list-response.dto';
import {{ ListFilterRequestDto }} from '../shared/implement/list-filter-request.dto';
import {{ DatabaseWorker }} from '../shared/db.worker.service';
import {{ AppLogger }} from '../shared/app-logger';
@Injectable()
export class {snake_to_camel(tbl_name)}Service {{
  constructor(
    private worker: DatabaseWorker,
    private logger: AppLogger,
  ) {{
    this.logger.setContext('{snake_to_camel(tbl_name)}Service');
  }}"""
    ts_service += f"""list(filter: ListFilterRequestDto): Observable< {snake_to_camel(tbl_name)}ListResponseDto > {{
    return new Observable<{snake_to_camel(tbl_name)}ListResponseDto>((observer) => {{
      this.worker.query('SELECT {schema_name}.{tbl_name}_list($1)', [filter]).subscribe({{
        next: (response) => {{
          if (response.error) {{
            observer.error(new HttpException(response.error, response.code));
            return;
          }}
          observer.next(response);
          observer.complete();
        }},
        error: (error) => observer.error(error),
      }});
    }});
  }} \n
  save({snake_to_camel(tbl_name, False)}: {snake_to_camel(tbl_name)}Dto): Observable<any> {{
    return new Observable<any>((observer) => {{
      this.worker.query('SELECT {schema_name}.{tbl_name}_save($1)', [JSON.stringify({snake_to_camel(tbl_name, False)})]).subscribe({{
        next: (response) => {{
          if (response.error) {{
            observer.error(new HttpException(response.error, response.code));
            return;
          }}
          observer.next(response);
          observer.complete();
        }},
        error: (error) => observer.error(error),
      }});
    }});
  }}
  get(id: number): Observable<{snake_to_camel(tbl_name)}Dto> {{
    return new Observable((observer) => {{
      this.worker.query('SELECT {schema_name}.{tbl_name}_get($1)', [id]).subscribe({{
        next: (response) => {{
          if (response.error) {{
            observer.error(new HttpException(response.error, response.code));
            return;
          }}
          observer.next(response);
          observer.complete();
        }},
        error: (error) => observer.error(error),
      }});
    }});
  }} \n
  delete(id: number) {{
    return new Observable((observer) => {{
      this.worker.query('SELECT {schema_name}.{tbl_name}_delete($1)', [id]).subscribe({{
        next: (response) => {{
          if (response.error) {{
            observer.error(new HttpException(response.error, response.code));
            return;
          }}
          observer.next(response);
          observer.complete();
        }},
        error: (error) => observer.error(error),
      }});
    }});
  }}
}}"""
    file_path = os.path.join('dist', 'api', snake_to_dash(tbl_name), f'{snake_to_dash(tbl_name)}.service.ts')
    os.makedirs(os.path.join('dist', 'api', snake_to_dash(tbl_name)), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(ts_service)


def generate_module(schema_name: str, tbl_name: str):
    ts_module = f"""import {{ Module }} from '@nestjs/common';
import {{ SharedModule }} from '../shared/shared.module';
import {{ {snake_to_camel(tbl_name)}Service }} from './{snake_to_dash(tbl_name)}.service';
import {{ {snake_to_camel(tbl_name)}Controller }} from './{snake_to_dash(tbl_name)}.controller';
@Module({{
  imports: [SharedModule],
  providers: [{snake_to_camel(tbl_name)}Service],
  exports: [{snake_to_camel(tbl_name)}Service],
  controllers: [{snake_to_camel(tbl_name)}Controller],
}})
export class {snake_to_camel(tbl_name)}Module {{}}
"""
    file_path = os.path.join('dist', 'api', snake_to_dash(tbl_name), f'{snake_to_dash(tbl_name)}.module.ts')
    os.makedirs(os.path.join('dist', 'api', snake_to_dash(tbl_name)), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(ts_module)


# Generate whole api
def generate_api(schema_name: str, tbl_name: str, field_array: List):
    # Create module directory
    generate_model_dto(schema_name, tbl_name, field_array)

    generate_filter_item_dto()

    generate_list_filter_request_dto()

    generate_list_response_dto(schema_name, tbl_name)

    generate_service(schema_name, tbl_name)

    generate_controller(schema_name, tbl_name)

    generate_module(schema_name, tbl_name)