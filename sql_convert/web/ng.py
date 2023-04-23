import os

from constants import date_placeholder
from sql_convert.common import is_number, is_boolean, snake_to_dash, snake_to_camel, is_date, capitalize
from sql_convert.includes.field_definition import FieldDefinition


# Module
def generate_module(schema_name: str, tbl_name: str):
    module_ts = f"""import {{ NgModule }} from '@angular/core';
import {{ CommonModule }} from '@angular/common';
import {{ {snake_to_camel(tbl_name)}ListComponent }} from './{snake_to_dash(tbl_name)}-list/{snake_to_dash(tbl_name)}-list.component';
import {{ {snake_to_camel(tbl_name)}EditComponent }} from './{snake_to_dash(tbl_name)}-edit/{snake_to_dash(tbl_name)}-edit.component';
import {{ MaterialModule }} from '../shared/material.module';
import {{ {snake_to_camel(tbl_name)}Service }} from './{snake_to_dash(tbl_name)}.service';
import {{ {snake_to_camel(tbl_name)}RoutingModule }} from './{snake_to_dash(tbl_name)}-routing.module';

@NgModule({{
  declarations: [
    {snake_to_camel(tbl_name)}ListComponent,
    {snake_to_camel(tbl_name)}EditComponent,
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
import {{ {snake_to_camel(tbl_name)}ListComponent }} from './{snake_to_dash(tbl_name)}-list/{snake_to_dash(tbl_name)}-list.component';
import {{ {snake_to_camel(tbl_name)}EditComponent }} from './{snake_to_dash(tbl_name)}-edit/{snake_to_dash(tbl_name)}-edit.component';

const routes: Routes = [
  {{
    path: '',
    redirectTo: 'list',
    pathMatch: 'full',
  }},
  {{
    path: 'list',
    component: {snake_to_camel(tbl_name)}ListComponent,
  }},
  {{
    path: 'edit/:id',
    component: {snake_to_camel(tbl_name)}EditComponent,
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
  {snake_to_camel(tbl_name)}Dto,
  {snake_to_camel(tbl_name)}ListResponseDto,
  {snake_to_camel(tbl_name)}Service as Api{snake_to_camel(tbl_name)}Service,
}} from '../api';
import {{ environment }} from '../../environments/environment'; \n
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
  selector: 'app-{snake_to_dash(tbl_name)}-edit',
  templateUrl: './{snake_to_dash(tbl_name)}-edit.component.html',
  styleUrls: ['./{snake_to_dash(tbl_name)}-edit.component.scss'],
}})
export class {snake_to_camel(tbl_name)}EditComponent implements OnDestroy {{
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
  }}
  
  save() {{
    if (this.form.invalid) {{
      Object.keys(this.form.controls).forEach((field) => {{
        const control = this.form.get(field);
        control?.markAsTouched({{ onlySelf: true }});
      }});
      this.alert.error('There is error on form.');
      return;
    }}
    
    this.{snake_to_camel(tbl_name, False)}Service.save(this.form.value)
      .pipe(takeUntil(this.destroy$))
      .subscribe({{
        next: () => {{
          this.router.navigate(['/{snake_to_dash(tbl_name)}/list']).then();
        }},
        error: (error) => {{
          this.alert.error(error.error.message);
        }},
      }});
  }}
  
  close() {{
    this.router.navigate(['/{snake_to_dash(tbl_name)}/list']).then();
  }}
}}"""
    file_path = os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}-edit', f'{snake_to_dash(tbl_name)}-edit.component.ts')
    os.makedirs(os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}-edit'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(edit_ts)


def generate_edit_scss(tbl_name: str):
    scss = """mat-form-field {
  display: block;
}
mat-card-footer {
  justify-content: flex-end;
}"""
    file_path = os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}-edit', f'{tbl_name.lower()}-edit.component.scss')
    os.makedirs(os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}-edit'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(scss)


def generate_form_field(item: FieldDefinition) -> str:
    if is_boolean(item):
        return f"""<mat-form-field class="full-width-input">
        <mat-slide-toggle formControlName="{item["field"]}">TODO: {item["description"]}</mat-slide-toggle>
        <textarea matInput hidden></textarea>
        <mat-error></mat-error>
      </mat-form-field>"""
    if is_date(item):
        return f""" <mat-form-field class="full-width-input">
        <mat-label>TODO: {item["description"]}</mat-label>
        <input matInput formControlName="{item["field"]}" [matDatepicker]="picker{snake_to_camel(item["field"])}" placeholder="{date_placeholder}"/>
        <mat-datepicker-toggle matSuffix [for]="picker{snake_to_camel(item["field"])}"></mat-datepicker-toggle>
        <mat-datepicker #picker{snake_to_camel(item["field"])}></mat-datepicker>
        <mat-error></mat-error>
      </mat-form-field>`;"""
    return f""" <mat-form-field class="full-width-input">
        <mat-label>TODO: {item["description"]}</mat-label>
        <input matInput formControlName="{item["field"]}" />
        <mat-error></mat-error>
      </mat-form-field>"""


def generate_edit_html(schema_name: str, tbl_name: str, field_array: list):
    edit_html = f"""<mat-card>
  <mat-card-header>
    <h2 *ngIf="item">Edit</h2>
    <h2 *ngIf="!item">Add</h2>
  </mat-card-header>
  <mat-card-content>
    <form [formGroup]="form">\n"""

    for item in field_array:
        edit_html += generate_form_field(item)

    edit_html += f"""
    </form>
  </mat-card-content>
  <mat-card-footer>
    <button mat-button (click)="close()"><mat-icon>close</mat-icon>Close</button>
    <button mat-button (click)="save()"><mat-icon>save</mat-icon>Save</button>
  </mat-card-footer>
</mat-card>"""
    file_path = os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}-edit', f'{snake_to_dash(tbl_name)}-edit.component.html')
    os.makedirs(os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}-edit'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(edit_html)


def generate_list_ts(schema_name: str, tbl_name: str, field_array: list):
    list_ts = f"""import {{
  AfterViewInit, Component, OnInit, ViewChild, OnDestroy
}} from '@angular/core';
import {{ MatSort, SortDirection }} from '@angular/material/sort';
import {{ MatPaginator }} from '@angular/material/paginator';
import {{ Router }} from '@angular/router';
import {{ MatDialog }} from '@angular/material/dialog';
import {{ merge, Subject, Observable }} from 'rxjs';
import {{ debounceTime, distinctUntilChanged, tap, takeUntil }} from 'rxjs/operators';
import {{ FormBuilder, FormGroup }} from '@angular/forms';
import {{ DeleteDialogComponent }} from '../../shared/delete-dialog/delete-dialog.component';
import {{ AlertService }} from '../../shared/alert/alert.service';
import {{ {snake_to_camel(tbl_name)}Service }} from '../{snake_to_dash(tbl_name)}.service';
import {{ {snake_to_camel(tbl_name)}Dto, FilterItemDto }} from '../../api';
import {{ {snake_to_camel(tbl_name)}Datasource }} from '../{snake_to_dash(tbl_name)}.datasource';
/**
 * Server side pagination list based on
 * https://github.com/angular-university/angular-material-course/tree/2-data-table-finished
 * https://blog.angular-university.io/angular-material-data-table/
 */
@Component({{
  selector: 'app-{snake_to_dash(tbl_name)}-list',
  templateUrl: './{snake_to_dash(tbl_name)}-list.component.html',
  styleUrls: ['./{snake_to_dash(tbl_name)}-list.component.scss'],
}})
export class {snake_to_camel(tbl_name)}ListComponent implements OnInit, AfterViewInit, OnDestroy {{
  list: {snake_to_camel(tbl_name)}Dto[] = [];
  
  private destroy$ = new Subject<void>();
  // TODO: Remove unnecessary columns, (leave actions)
  displayedColumns = ["""

    for item in field_array:
        list_ts += f"""'{item["field"]}', """

    list_ts += f"""'actions'];
    
  // @ts-ignore
  public listTable: {snake_to_camel(tbl_name)}Datasource;
  
  @ViewChild(MatSort, {{ static: false }}) sort!: MatSort;
  
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  
  searchForm: FormGroup;
  
  dataSize: number = 0;
  
  pageSizeOpt: number[] = [25, 50, 100];
  
  public filter: {{
    pageSize: number;
    pageIndex: number;
    sortActive: string;
    sortDirection: SortDirection;
  }} = {{
      pageSize: 25,
      pageIndex: 0,
      sortActive: '',
      sortDirection: 'asc',
    }};
    
  constructor(
    private {snake_to_camel(tbl_name, False)}Service: {snake_to_camel(tbl_name)}Service,
    private router: Router,
    public dialog: MatDialog,
    private alertService: AlertService,
    private fb: FormBuilder,
  ) {{
    this.searchForm = this.fb.group({{
      in{capitalize(field_array[1]["field"])}: [this.{snake_to_camel(tbl_name, False)}Service.getFilterValue('{field_array[1]["field"]}')],
    }});
  }}
  
  ngOnInit(): void {{
    this.listTable = new {snake_to_camel(tbl_name)}Datasource(this.{snake_to_camel(tbl_name, False)}Service, this.alertService);
    this.listTable.cntSubject
      .pipe(takeUntil(this.destroy$))
      .subscribe({{
        next: (cnt) => {{
          this.dataSize = cnt;
          this.pageSizeOpt = [25, 50, cnt];
        }},
      }});
      
    if (this.{snake_to_camel(tbl_name, False)}Service.savedFilter) {{
      this.filter.pageIndex = this.{snake_to_camel(tbl_name, False)}Service.savedFilter.page_index;
      this.filter.pageSize = this.{snake_to_camel(tbl_name, False)}Service.savedFilter.page_size;
      this.filter.sortDirection = this.{snake_to_camel(tbl_name, False)}Service.savedFilter.sort_direction;
      if (this.{snake_to_camel(tbl_name, False)}Service.savedFilter.sort) {{
        this.filter.sortActive = this.{snake_to_camel(tbl_name, False)}Service.savedFilter.sort[0];
      }}
    }}
    this.listTable.load();
  }}

  ngOnDestroy(): void {{
    this.destroy$.next();
    this.destroy$.unsubscribe();
  }}
  
  ngAfterViewInit(): void {{
    this.sort.sortChange
      .pipe(takeUntil(this.destroy$))
      .subscribe({{
        next: (sort) => {{
          this.filter.sortDirection = sort.direction;
          this.filter.sortActive = sort.active;
          this.paginator.pageIndex = 0;
        }},
      }});
    const arrEvents: Observable<any>[] = [];
    
    Object.values(this.searchForm.controls).forEach((control) => {{
      arrEvents.push(control.valueChanges);
    }});
    
    // fromEvent(this.search{capitalize(field_array[1]["field"])}Input.nativeElement, 'keyup'),
    merge(
      ...arrEvents,
    ).pipe(
      takeUntil(this.destroy$),
      debounceTime(150),
      distinctUntilChanged(),
      tap(() => {{
        this.paginator.pageIndex = 0;
        this.load();
      }}),
    ).subscribe();
    
    merge(
      this.sort.sortChange,
      this.paginator.page,
    ).pipe(
      takeUntil(this.destroy$),
      tap(() => this.load()),
    ).subscribe();
  }}
  
  load() {{
    // Check if elements are initialized
    if (!this.sort) {{
      return;
    }}
    
    const filter: FilterItemDto[] = [];
    
    Object.keys(this.searchForm.controls).forEach((key) => {{
      const control = this.searchForm.get(key);
      const value = control?.value;
      
      if (value && value !== '')
        filter.push({{
          field: key.toLowerCase().substring(2),
          value: value,
        }});
    }});
    const sort = [];
    if (this.filter.sortActive) {{
      sort.push(this.filter.sortActive);
    }}
    
    this.listTable?.load({{
      filter,
      sort,
      page_index: this.paginator?.pageIndex,
      page_size: this.paginator?.pageSize,
      sort_direction: this.filter.sortDirection,
    }});
  }}
  
  edit(id: number) {{
    this.router.navigate([`{tbl_name}/edit/${{id}}`]).then();
  }}
  
  deleteDlg(row: {snake_to_camel(tbl_name)}Dto) {{
    const dlg = this.dialog.open(DeleteDialogComponent, {{ data: {{ title: `${{row.{field_array[1]["field"]} }}` }} }});
    dlg.afterClosed().pipe(takeUntil(this.destroy$)).subscribe((result) => {{
      if (!result) {{ return; }}
      this.{snake_to_camel(tbl_name, False)}Service.delete(parseInt(row.{field_array[0]["field"]})).subscribe({{
        next: () => {{
          this.alertService.success('Item deleted');
          this.load();
        }},
        error: (error) => {{
          this.alertService.error(error.error.message);
        }},
      }});
    }});
  }}
}}"""
    file_path = os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}-list', f'{snake_to_dash(tbl_name)}-list.component.ts')
    os.makedirs(os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}-list'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(list_ts)


def generate_list_scss(tbl_name: str):
    list_scss = """table {
  width: 100%;
}

.mat-row .mat-cell {
  border-bottom: 1px solid transparent;
  border-top: 1px solid transparent;
}

.mat-row:hover .mat-cell {
  border-color: currentColor;
}

.column-desc {
  cursor: pointer;
}

.column-dt {
  cursor: pointer;
}

.column-actions {
  width: 120px;
}

.spinner-container {
  height: 360px;
  width: 390px;
  position: fixed;
}

.spinner-container mat-spinner {
  margin: 130px auto 0 auto;
}

.header-item {
  margin-left: 5px;
  margin-right: 5px;
}"""
    file_path = os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}-list', f'{snake_to_dash(tbl_name)}-list.component.scss')
    os.makedirs(os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}-list'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(list_scss)


def generate_list_html(schema_name: str, tbl_name: str, field_array: list):
    list_html = f"""<mat-card class="mat-elevation-z4">
  <mat-card-content>
    <form [formGroup]="searchForm">
      <div class="flex-container">
      <div>
        List
      </div>
      <div>
        <button mat-raised-button (click)="edit(0)" class="header-item">
          <mat-icon>add</mat-icon>
          Add
        </button>
        <mat-form-field class="header-item">
          <mat-label>Search {field_array[1]["field"]}</mat-label>
          <input matInput placeholder="Search field" formControlName="in{capitalize(field_array[1]["field"])}">
        </mat-form-field>
      </div>
    </div>
    </form>
  </mat-card-content>
</mat-card>
<br/>
<mat-card  class="mat-elevation-z4">
  <mat-card-content>
    <div class="spinner-container" *ngIf="listTable.loading$ | async">
      <mat-spinner></mat-spinner>
    </div>
    
    <table mat-table matSort [dataSource]="listTable">\n\n"""

    for item in field_array:
        list_html += f"""      <ng-container matColumnDef="{item["field"]}">
        <th mat-header-cell mat-sort-header *matHeaderCellDef>
          TODO: {item["field"]}
        </th>
        <td
          (click)="edit(item.{field_array[0]["field"]})" 
          mat-cell 
          *matCellDef="let item" class="column-dt">
          {{item.{item["field"]}}}
        </td>
      </ng-container>"""
        list_html += "\n\n"

    list_html += f"""`      <ng-container matColumnDef="actions" stickyEnd>
        <th mat-header-cell *matHeaderCellDef></th>
        <td mat-cell *matCellDef="let item" class="column-actions">
          <button mat-icon-button (click)="edit(item.{field_array[0]["field"]})"><mat-icon>edit</mat-icon></button>
          <button mat-icon-button (click)="deleteDlg(item)"><mat-icon>delete</mat-icon></button>
        </td>
      </ng-container>
      <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
      <tr
        mat-row
        *matRowDef="let row; columns: displayedColumns;"
        class="table-row"></tr>
    </table>
    <mat-paginator
      [pageSizeOptions]="pageSizeOpt"
      [pageSize]="filter.pageSize"
      [pageIndex]="filter.pageIndex"
      [length]="dataSize"
      showFirstLastButtons
      aria-label="Choose page">
    </mat-paginator>
  </mat-card-content>
</mat-card>"""
    file_path = os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}-list', f'{snake_to_dash(tbl_name)}-list.component.html')
    os.makedirs(os.path.join('dist', 'www', f'{snake_to_dash(tbl_name)}-list'), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(list_html)


def generate_angular_module(schema_name: str, tbl_name: str, field_array: list):
    generate_module(schema_name, tbl_name)

    generate_routing(schema_name, tbl_name)

    generate_service(schema_name, tbl_name)

    generate_data_source(schema_name, tbl_name)

    generate_edit_ts(schema_name, tbl_name, field_array)

    generate_edit_scss(tbl_name)

    generate_edit_html(schema_name, tbl_name, field_array)

    generate_list_scss(tbl_name)

    generate_list_ts(schema_name, tbl_name, field_array)

    generate_list_html(schema_name, tbl_name, field_array)