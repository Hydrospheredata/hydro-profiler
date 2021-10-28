import { Component, OnDestroy } from '@angular/core';
import { RouterQuery } from '@datorama/akita-ng-router-store';
import { Subject } from 'rxjs';
import { filter, takeUntil } from 'rxjs/operators';
import { DashboardQuery } from './state/dashboard.query';
import { DashboardService } from './state/dashboard.service';

@Component({
  selector: 'profiler-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnDestroy {
  batch$ = this.query.batch$;
  aggregation$ = this.query.agg$;

  private destroy: Subject<any> = new Subject<any>();

  constructor(
    private query: DashboardQuery,
    private service: DashboardService,
    routerQuery: RouterQuery,
  ) {
    routerQuery
      .selectParams(['modelName', 'modelVersion'])
      .pipe(
        filter(([modelName, modelVersion]) => {
          return modelName !== undefined && modelVersion !== undefined;
        }),
        takeUntil(this.destroy),
      )
      .subscribe(([modelName, modelVersion]) =>
        this.service.getAggregation(modelName, modelVersion),
      );
  }

  ngOnDestroy(): void {
    this.destroy.next();
    this.destroy.complete();
  }
}
