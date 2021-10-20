import { Component } from "@angular/core";
import { RouterQuery } from "@datorama/akita-ng-router-store";
import { DashboardQuery } from "../state/dashboard.query";
import { DashboardService } from "../state/dashboard.service";
import { tap } from 'rxjs/operators'

@Component({
    templateUrl: './batch-report-page.component.html',
  })
export class BatchReportPageComponent {
    report$ = this.query.batch$.pipe(tap(console.log));

    constructor(private query: DashboardQuery, service: DashboardService, routerQuery: RouterQuery){
        routerQuery
        .selectParams(['modelName', 'modelVersion', 'batchName'])
        .subscribe(([modelName, modelVersion, batchName]) => { 
            console.log(modelName, batchName),
            service.resetBatch()
            service.getBatch(modelName, modelVersion, batchName)
        })
    }
}