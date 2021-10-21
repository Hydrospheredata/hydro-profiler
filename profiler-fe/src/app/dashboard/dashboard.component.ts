import { Component } from '@angular/core';
import { RouterQuery } from '@datorama/akita-ng-router-store';
import { DashboardQuery } from './state/dashboard.query';
import { DashboardService } from './state/dashboard.service';

@Component({
  selector: 'profiler-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent {
  batch$ = this.query.batch$;
  aggregation$ = this.query.agg$;

  constructor(
    private query: DashboardQuery,
    private service: DashboardService,
    routerQuery: RouterQuery,
  ) {
    routerQuery.selectData().subscribe(console.log);

    routerQuery
      .selectParams(['modelName', 'modelVersion'])
      .subscribe(([modelName, modelVersion]) =>
        this.service.getAggregation(modelName, modelVersion),
      );
  }
}
