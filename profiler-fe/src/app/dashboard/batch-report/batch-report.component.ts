import { Component, OnInit, ChangeDetectionStrategy, Input } from '@angular/core';
import { Overall, ReportItem } from 'src/app/domain/report';
import { animate, state, style, transition, trigger } from '@angular/animations';
import { Check, CheckStatus } from 'src/app/domain/check';
import { EntityFilter } from 'src/app/utils/utility-filter';
import { BehaviorSubject, combineLatest, Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';

interface NormalizedCheck {
  feature: string;
  status: CheckStatus;
  metricType: String;
  description: string;
  style_class: string;
}

interface NormalizedDataItem {
  row_id: string;
  count: number;
  succeed: number;
  suspicious: number;
  failed: number;
  row_color: string;
  checks: NormalizedCheck[];
}

type DataFilter = EntityFilter<NormalizedDataItem, keyof NormalizedDataItem>;

@Component({
  selector: 'profiler-batch-report',
  templateUrl: './batch-report.component.html',
  styleUrls: ['./batch-report.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({ height: '0px', minHeight: '0' })),
      state('expanded', style({ height: '*' })),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ],
})
export class BatchReportComponent implements OnInit {
  @Input() report: ReportItem[] = [];

  statistic: Overall = {
    suspicious: 0,
    succeed: 0,
    failed: 0,
    count: 0,
  };
  dataToShow: NormalizedDataItem[] = [];

  defaultFilter(): EntityFilter<NormalizedDataItem, keyof NormalizedDataItem> {
    const filter = new EntityFilter<NormalizedDataItem, keyof NormalizedDataItem>();
    filter.addFilter('failed')((v) => v > 0);
    filter.addFilter('suspicious')((v) => v > 0);

    return filter;
  }

  filter: BehaviorSubject<DataFilter> = new BehaviorSubject(this.defaultFilter());
  filter$: Observable<DataFilter> = this.filter.asObservable();
  data: BehaviorSubject<NormalizedDataItem[]> = new BehaviorSubject<NormalizedDataItem[]>([]);
  data$: Observable<NormalizedDataItem[]> = combineLatest([
    this.data.asObservable(),
    this.filter$,
  ]).pipe(
    map(([items, filter]) => filter.filter(items)),
    tap(console.log),
  );

  constructor() {}

  ngOnInit(): void {
    this.statistic = this.reportRowsStatistic();
    this.dataToShow = this.normalizeData(this.report);
    this.data.next(this.dataToShow);
  }

  isActive(kind: keyof NormalizedDataItem): boolean {
    return this.filter.getValue().filters.has(kind);
  }

  toggleFilter(kind: keyof NormalizedDataItem) {
    const currentFilter = this.filter.getValue();
    if (currentFilter.filters.has(kind)) {
      currentFilter.removeFilter(kind);
    } else {
      currentFilter.addFilter(kind)((value) => value > 0);
    }

    this.filter.next(currentFilter);
  }

  columnsToDisplay = ['row_id', 'count', 'succeed', 'suspicious', 'failed'];
  expandedElement!: NormalizedDataItem | null;

  private normalizeData(reports: ReportItem[]): NormalizedDataItem[] {
    const getClass = (status: CheckStatus) => {
      switch (status) {
        case 'failed':
          return 'text-red-600';
        case 'suspicious':
          return 'text-yellow-600';
        default:
          return '';
      }
    };

    return reports.map<NormalizedDataItem>((r) => {
      const checks = { ...r._raw_checks };

      const normalizedChecks = Object.entries(checks).reduce((arr, [feature, raw_checks]) => {
        const normalizedChecks = raw_checks
          .filter((_) => _.status != 'succeed')
          .map((check) => ({
            feature,
            metricType: check.metric_type,
            status: check.status,
            description: check.description,
            style_class: getClass(check.status),
          }));

        return [...arr, ...normalizedChecks];
      }, [] as NormalizedCheck[]);

      return {
        row_id: r._id,
        count: r._row_overall.count,
        succeed: r._row_overall.succeed,
        suspicious: r._row_overall.suspicious,
        failed: r._row_overall.failed,
        row_color: this.selectRowColorClass(r._row_overall),
        checks: normalizedChecks,
      };
    });
  }

  selectRowColorClass(overall: Overall): string {
    if (overall.failed > 0) {
      return 'bg-red-50';
    } else if (overall.suspicious > 0) {
      return 'bg-yellow-50';
    } else {
      return 'bg-white';
    }
  }

  filterFailedOrSuspicious(checks: unknown) {
    return (checks as Check[]).filter((ch) => ch.status !== 'succeed');
  }

  describeClasses(checkStatus: CheckStatus): string {
    switch (checkStatus) {
      case 'failed':
        return 'bg-red-50 border-red-400';
      case 'suspicious':
        return 'bg-yellow-50 border-yellow-400';
      default:
        return 'bg-green-50 border-green-400';
    }
  }

  reportRowsStatistic(): Overall {
    const overall: Overall = {
      suspicious: 0,
      succeed: 0,
      failed: 0,
      count: 0,
    };

    return this.report.reduce((a, b) => {
      let newOverall: Partial<Overall> = {};
      if (b._row_overall.failed > 0) {
        newOverall = { failed: a.failed + 1, count: a.count + 1 };
      } else if (b._row_overall.suspicious > 0) {
        newOverall = { suspicious: a.suspicious + 1, count: a.count + 1 };
      } else {
        newOverall = { succeed: a.succeed + 1, count: a.count + 1 };
      }
      return { ...a, ...newOverall };
    }, overall);
  }
}
