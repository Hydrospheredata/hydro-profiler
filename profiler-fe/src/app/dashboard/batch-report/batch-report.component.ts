import { ChangeDetectionStrategy, Component, Input, OnInit } from '@angular/core';
import { BehaviorSubject, combineLatest, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { DataRowReport, DataRowStatus, ModelReport } from 'src/app/domain/report';
import { FilterKind } from './normalized-data';

@Component({
  selector: 'profiler-batch-report',
  templateUrl: './batch-report.component.html',
  styleUrls: ['./batch-report.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class BatchReportComponent implements OnInit {
  @Input()
  report!: ModelReport;

  filter: BehaviorSubject<Set<FilterKind>> = new BehaviorSubject(new Set());
  filter$: Observable<Set<FilterKind>> = this.filter.asObservable();

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

  constructor() {}

  failedCount = 0;
  suspiciousCount = 0;

  ngOnInit(): void {
    this.failedCount = this.report.report.filter(
      (x) => x.status == DataRowStatus.HAS_FAILED,
    ).length;
    this.suspiciousCount = this.report.report.filter(
      (x) => x.status == DataRowStatus.HAS_SUSPICIOUS,
    ).length;

    if (this.failedCount > 0) {
      this.toggleFilter('failed');
    }
    if (this.failedCount == 0 && this.suspiciousCount > 0) {
      this.toggleFilter('suspicious');
    }
    this.data.next(this.report.report);
  }

  onClickRow(el: MouseEvent, row: DataRowReport): void {
    if (row.status == DataRowStatus.HEALTHY) return;

    const target = el.currentTarget as HTMLElement;
    target.classList.toggle('expanded');
  }

  isActive(kind: FilterKind): boolean {
    return this.filter.getValue().has(kind);
  }

  isHealty(status: DataRowStatus) {
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
