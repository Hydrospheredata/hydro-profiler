import {AfterViewInit, ChangeDetectionStrategy, Component, Input, OnInit, ViewChild} from '@angular/core';
import {BehaviorSubject, combineLatest, Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {DataRowReport, DataRowStatus, ModelReport} from 'src/app/domain/report';
import {FilterKind} from './normalized-data';
import {MatTableDataSource} from "@angular/material/table";
import {MatPaginator} from "@angular/material/paginator";
import {animate, state, style, transition, trigger} from "@angular/animations";

@Component({
  selector: 'profiler-batch-report',
  templateUrl: './batch-report.component.html',
  styleUrls: ['./batch-report.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0'})),
      state('expanded', style({height: '*'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ],
})
export class BatchReportComponent implements OnInit, AfterViewInit {
  @Input()
  report!: ModelReport;

  filter: BehaviorSubject<Set<FilterKind>> = new BehaviorSubject(new Set());
  filter$: Observable<Set<FilterKind>> = this.filter.asObservable();

  expandedElement: DataRowReport | null = null;
  displayedColumns: string[] = ['number', 'status'];

  data: BehaviorSubject<DataRowReport[]> = new BehaviorSubject<DataRowReport[]>([]);
  data$: Observable<DataRowReport[]> = combineLatest([this.data.asObservable(), this.filter$]).pipe(
    map(([items, filter]) => {
      if (filter.size == 0) return items;

      let rows: DataRowReport[] = [];
      if (filter.has('failed')) {
        rows.push(...items.filter((x) => x.status == DataRowStatus.HAS_FAILED));
      }
      if (filter.has('suspicious')) {
        rows.push(...items.filter((x) => x.status == DataRowStatus.HAS_SUSPICIOUS));
      }
      if (filter.has('succeed')) {
        rows.push(...items.filter((x) => x.status == DataRowStatus.HEALTHY));
      }

      return rows.sort((a, b) => a.id - b.id);
    }),
  );

  dataSource!: MatTableDataSource<DataRowReport>;

  constructor() {
  }

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  ngAfterViewInit() {
      this.dataSource.paginator = this.paginator;
  }

  ngOnInit(): void {
    if (this.report.failed_count > 0) {
      this.toggleFilter('failed');
    }
    if (this.report.failed_count == 0 && this.report.suspicious_count > 0) {
      this.toggleFilter('suspicious');
    }

    this.data.next(this.report.rows);

    this.data$.subscribe(
      report => {
        this.dataSource = new MatTableDataSource<DataRowReport>(report);
        this.dataSource.paginator = this.paginator
      }
    )
  }

  isExpandable(status: DataRowStatus): boolean {
    return status !== DataRowStatus.HEALTHY
  }

  isActive(kind: FilterKind): boolean {
    return this.filter.getValue().has(kind);
  }

  isHealthy(status: DataRowStatus) {
    return status === DataRowStatus.HEALTHY;
  }

  isFailed(status: DataRowStatus) {
    return status === DataRowStatus.HAS_FAILED;
  }

  isSuspicious(status: DataRowStatus) {
    return status === DataRowStatus.HAS_SUSPICIOUS;
  }

  toggleFilter(kind: FilterKind) {
    const currentFilter = this.filter.getValue();

    if (currentFilter.has(kind)) {
      currentFilter.delete(kind);
    } else {
      currentFilter.add(kind);
    }

    this.filter.next(currentFilter);
  }
}
