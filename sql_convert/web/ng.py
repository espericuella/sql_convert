import os

from sql_convert.common import is_number, is_boolean, snake_to_dash, snake_to_camel


# Module
def generate_module(schema_name: str, tbl_name: str):
    module_ts = f"""import {{ NgModule }} from '@angular/core';
import {{ CommonModule }} from '@angular/common';
import {{ ListComponent }} from './list/list.component';
import {{ EditComponent }} from './edit/edit.component';
import {{ MaterialModule }} from '../shared/material.module';
import {{ {snake_to_camel(tbl_name)}Service }} from './{snake_to_dash(tbl_name)}.service';
import {{ {snake_to_camel(tbl_name)}RoutingModule }} from './{snake_to_dash(tbl_name)}-routing.module';
@NgModule({{
  declarations: [
    ListComponent,
    EditComponent,
  ],
  imports: [
    CommonModule,
    MaterialModule,
    {snake_to_camel(tbl_name)}RoutingModule,
  ],
  providers: [
    {snake_to_camel(tbl_name)}Service,
  ],
}})
export class {snake_to_camel(tbl_name)}Module { {} }"""
    file_path = os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}.module.ts')
    os.makedirs(os.path.join('dist', 'www'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(module_ts)


# Routing module
def generate_routing(schema_name: str, tbl_name: str):
    module_ts = f"""import {{ NgModule }} from '@angular/core';
import {{ RouterModule, Routes }} from '@angular/router';
import {{ ListComponent }} from './list/list.component';
import {{ EditComponent }} from './edit/edit.component';
const routes: Routes = [
  {{
    path: '',
    redirectTo: 'list',
    pathMatch: 'full',
  }},
  {{
    path: 'list',
    component: ListComponent,
  }},
  {{
    path: 'edit/:id',
    component: EditComponent,
  }},
];
@NgModule({{
  declarations: [],
  imports: [
    RouterModule.forChild(routes),
  ],
}})
export class {snake_to_camel(tbl_name)}RoutingModule {{}}"""
    file_path = os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}-routing.module.ts')
    os.makedirs(os.path.join('dist', 'www'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(module_ts)


# Service
def generate_service(schema_name: str, tbl_name: str):
    service_ts = f"""import {{ Injectable }} from '@angular/core';
import {{ HttpClient }} from '@angular/common/http';
import {{ Observable }} from 'rxjs';
import {{
  Configuration,
  ListFilterRequestDto,
  {{{snake_to_camel(tbl_name)}}}Dto,
  {{{snake_to_camel(tbl_name)}}}ListResponseDto,
  {{{snake_to_camel(tbl_name)}}}Service as Api{snake_to_camel(tbl_name)}Service,
}} from '../api';
import {{ environment }} from '../../environments/environment';
@Injectable({{
  providedIn: 'root',
}})
export class {snake_to_camel(tbl_name)}Service {{
  constructor(
    private httpClient: HttpClient,
    private api{snake_to_camel(tbl_name)}Service: Api{snake_to_camel(tbl_name)}Service,
  ) {{
    const basePath = environment.apiUrl;
    const conf = new Configuration();
    this.api{snake_to_camel(tbl_name)}Service = new Api{snake_to_camel(tbl_name)}Service(this.httpClient, basePath, conf);
  }}

  public savedFilter: ListFilterRequestDto = {{
    filter: [],
    sort: [],
    page_size: 25,
    sort_direction: 'asc',
    page_index: 0,
  }};
  public getFilterValue(fieldName: string): string {{
    let result = this.savedFilter.filter?.find((item) => item.field === fieldName)?.value;
    if ( !result ) {{
      result = '';
    }}
    return result;
  }}
  public list(body: ListFilterRequestDto): Observable< {snake_to_camel(tbl_name)}ListResponseDto > {{
    return this.api{snake_to_camel(tbl_name)}Service.{snake_to_camel(tbl_name, False)}ControllerList(body);
  }}
  public delete(id: number) {{
    return this.api{snake_to_camel(tbl_name)}Service.{snake_to_camel(tbl_name, False)}ControllerDelete(id);
  }}
  public save(body: {snake_to_camel(tbl_name)}Dto) {{
    return this.api{snake_to_camel(tbl_name)}Service.{snake_to_camel(tbl_name, False)}ControllerAdd(body);
  }}
  public view(id: number): Observable< {snake_to_camel(tbl_name)}Dto> {{
    return this.api{snake_to_camel(tbl_name)}Service.{snake_to_camel(tbl_name, False)}ControllerGet(id);
  }}
  // public getGroups() {{
  //   return this.api{snake_to_camel(tbl_name)}Service.{snake_to_camel(tbl_name, False)}ControllerGetGroups();
  // }}
}}"""
    file_path = os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}.service.ts')
    os.makedirs(os.path.join('dist', 'www'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(service_ts)


# Datasource for list
def generate_data_source(schema_name: str, tbl_name: str):
    ds_ts = f"""import {{ CollectionViewer, DataSource }} from '@angular/cdk/collections';
import {{ BehaviorSubject, Observable, of }} from 'rxjs';
import {{ catchError, finalize }} from 'rxjs/operators';
import {{ {snake_to_camel(tbl_name)}Dto, ListFilterRequestDto }} from '../api';
import {{ {snake_to_camel(tbl_name)}Service }} from './{snake_to_dash(tbl_name)}.service';
export class {snake_to_camel(tbl_name)}Datasource extends DataSource< {snake_to_camel(tbl_name)}Dto> {{
  private {snake_to_camel(tbl_name, False)}Subject = new BehaviorSubject<{snake_to_camel(tbl_name)}Dto[]>([]);
  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$ = this.loadingSubject.asObservable();
  public cntSubject = new BehaviorSubject<number>(0);
  constructor(
    private {snake_to_camel(tbl_name, False)}Service: {snake_to_camel(tbl_name)}Service,
    private alertService: AlertService,
  ) {{
    super();
  }}
  load(filter?: ListFilterRequestDto) {{
    this.loadingSubject.next(true);
    if (filter) {{
      this.{snake_to_camel(tbl_name, False)}Service.savedFilter = filter;
    }}
    this.{snake_to_camel(tbl_name, False)}Service.list(this.{snake_to_camel(tbl_name, False)}Service.savedFilter)
      .pipe(
        catchError((err) => {{
          this.alertService.clear();
          this.alertService.error(err.error.message);
          return of([]);
        }}),
        finalize(() => this.loadingSubject.next(false)),
      )
      .subscribe({{
        next: (items) => {{
          if ('data' in items) {{
            this.cntSubject.next(items.cnt);
            this.{snake_to_camel(tbl_name, False)}Subject.next(items.data);
          }}
        }},
      }});
  }}
  // eslint-disable-next-line @typescript-eslint/no-unused-vars-experimental
  connect(collectionViewer: CollectionViewer): Observable<{snake_to_camel(tbl_name)}Dto[]> {{
    return this.{snake_to_camel(tbl_name, False)}Subject.asObservable();
  }}
  // eslint-disable-next-line @typescript-eslint/no-unused-vars-experimental
  disconnect(collectionViewer: CollectionViewer): void {{
    this.{snake_to_camel(tbl_name, False)}Subject.complete();
    this.loadingSubject.complete();
    this.cntSubject.complete();
  }}
}}"""
    file_path = os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}.datasource.ts')
    os.makedirs(os.path.join('dist', 'www'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(ds_ts)


def generate_edit_ts(schema_name: str, tbl_name: str, field_array: list):
    edit_ts = f"""import {{ Component, OnDestroy }} from '@angular/core';
import {{ ActivatedRoute, Router }} from '@angular/router';
import {{ filter, takeUntil }} from 'rxjs/operators';
import {{ Subject }} from 'rxjs';
import {{ FormBuilder, FormGroup, Validators }} from '@angular/forms';
import {{ AlertService }} from '../../shared/alert/alert.service';
import {{ {snake_to_camel(tbl_name)}Dto }} from '../../api';
import {{ {snake_to_camel(tbl_name)}Service }} from '../{snake_to_dash(tbl_name)}.service';
@Component({{
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.scss'],
}})
export class EditComponent implements OnDestroy {{
  form: FormGroup;
  
  private destroy$ = new Subject<void>();
  item: {snake_to_camel(tbl_name)}Dto | undefined;
  constructor(
    private {snake_to_camel(tbl_name, False)}Service: {snake_to_camel(tbl_name)}Service,
    private route: ActivatedRoute,
    private router: Router,
    private fb: FormBuilder,
    private alert: AlertService,
  ) {{
    this.form = this.fb.group({{\n"""

    for item in field_array:
        edit_ts += f'      {item["field"]}: ['
        if is_number(item):
            edit_ts += "0"
        elif is_boolean(item):
            edit_ts += "true"
        else:
            edit_ts += '\'\''

        if item["not_null"] is True:
            edit_ts += ', Validators.required'

        edit_ts += '],\n'

    edit_ts += f"""    }});
    this.route.params
      .pipe(
        takeUntil(this.destroy$),
        filter((params) => params.id),
      )
      .subscribe((params) => {{
        if (params.id.toString() === '0') {{ return; }}
        this.{snake_to_camel(tbl_name, False)}Service.view(params.id).subscribe({{
          next: (item) => {{
            this.item = item;
            this.form.patchValue(item);
          }},
        }});
      }});
  }}

  ngOnDestroy(): void {{
    this.destroy$.next();
    this.destroy$.unsubscribe();
  }} \n
  save() {{
    if (this.form.invalid) {{
      Object.keys(this.form.controls).forEach((field) => {{
        const control = this.form.get(field);
        control?.markAsTouched({{ onlySelf: true }});
      }});
      this.alert.error('There is error on form.');
      return;
    }} \n
    this.{snake_to_camel(tbl_name, False)}Service.save(this.form.value)
      .pipe(takeUntil(this.destroy$))
      .subscribe({{
        next: () => {{
          this.router.navigate(['/{tbl_name}/list']).then();
        }},
        error: (error) => {{
          this.alert.error(error.error.message);
        }},
      }});
  }} \n
  close() {{
    this.router.navigate(['/{tbl_name}/list']).then();
  }}
}}"""
    file_path = os.path.join('dist', 'www', 'edit', f'{tbl_name.lower()}-edit.component.ts')
    os.makedirs(os.path.join('dist', 'www', 'edit'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(edit_ts)


def generate_angular_module(schema_name: str, tbl_name: str, field_array: list):
    generate_module(schema_name, tbl_name)

    generate_routing(schema_name, tbl_name)

    generate_service(schema_name, tbl_name)

    generate_data_source(schema_name, tbl_name)

    generate_edit_ts(schema_name, tbl_name, field_array)
