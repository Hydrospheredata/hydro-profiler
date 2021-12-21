import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RouterQuery } from '@datorama/akita-ng-router-store';
import { filter, map } from 'rxjs/operators';
import { Aggregation, AggregationBatch } from 'src/app/dashboard/state/dashboard.store';

@Component({
  selector: 'profiler-data-section',
  templateUrl: './data-section.component.html',
  styleUrls: ['./data-section.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DataSectionComponent {
  @Input() agg: Aggregation | null = null;
  @Input() names: string[] = [];

  selectedBatchName = this.routerQuery.selectParams('batchName').pipe(
    filter((x) => x),
    map((x) => atob(x)),
  );

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private routerQuery: RouterQuery,
  ) {}

  onColumnClick(column: AggregationBatch) {
    const encoded = btoa(column.batch_name);

    this.router.navigate([encoded], { relativeTo: this.route });
  }
}
