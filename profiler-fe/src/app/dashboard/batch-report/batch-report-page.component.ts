import { Component, OnDestroy, OnInit } from '@angular/core';
import { RouterQuery } from '@datorama/akita-ng-router-store';
import { DashboardQuery } from '../state/dashboard.query';
import { DashboardService } from '../state/dashboard.service';
import { filter, takeUntil, tap } from 'rxjs/operators';
import { Subject } from 'rxjs';

@Component({
  templateUrl: './batch-report-page.component.html',
})
export class BatchReportPageComponent implements OnInit, OnDestroy {
  report$ = this.query.batch$;
  batchFileName$ = this.routerQuery.selectParams('batchName');
  private destroy: Subject<any> = new Subject<any>();

  constructor(
    private query: DashboardQuery,
    private service: DashboardService,
    private routerQuery: RouterQuery,
  ) {}

  ngOnInit() {
    this.routerQuery
      .selectParams(['modelName', 'modelVersion', 'batchName'])
      .pipe(
        tap(console.log),
        filter(([modelName, modelVersion, batchName]) => {
          return modelName !== undefined && modelVersion !== undefined && batchName !== undefined;
        }),
        takeUntil(this.destroy),
      )
      .subscribe(([modelName, modelVersion, batchName]) => {
        this.service.resetBatch();
        this.service.getBatch(modelName, modelVersion, batchName);
      });
  }

  ngOnDestroy(): void {
    this.destroy.next();
    this.destroy.complete();
  }
}
