import { Component, OnInit } from '@angular/core';
import { RouterQuery } from '@datorama/akita-ng-router-store';
import { DashboardQuery } from '../state/dashboard.query';
import { DashboardService } from '../state/dashboard.service';
import { tap } from 'rxjs/operators';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  templateUrl: './batch-report-page.component.html',
})
export class BatchReportPageComponent implements OnInit {
  report$ = this.query.batch$.pipe(tap(console.log));

  constructor(
    private query: DashboardQuery,
    private service: DashboardService,
    private routerQuery: RouterQuery,
    private route: ActivatedRoute,
  ) {}

  ngOnInit() {
    this.route.params.subscribe(console.log);

    this.routerQuery
      .selectParams(['modelName', 'modelVersion', 'batchName'])
      .subscribe(([modelName, modelVersion, batchName]) => {
        console.log(modelName, batchName), this.service.resetBatch();
        this.service.getBatch(modelName, modelVersion, batchName);
      });
  }
}
