import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DashboardComponent } from './dashboard.component';
import { AggregationComponent } from './aggregation/aggregation.component';
import { DataSectionComponent } from './aggregation/components/data-section/data-section.component';
import { BatchReportComponent } from './batch-report/batch-report.component';
import { BatchReportPageComponent } from './batch-report/batch-report-page.component';
import { SharedModule } from '../shared/shared.module';
import { AkitaNgRouterStoreModule } from '@datorama/akita-ng-router-store';
import { RouterModule, Routes } from '@angular/router';
import { ColumnComponent } from './aggregation/components/column/column.component';

export const routes: Routes = [
  {
    path: '',
    component: DashboardComponent,
    children: [{ path: ':batchName', component: BatchReportPageComponent }],
  },
];

@NgModule({
  declarations: [
    DashboardComponent,
    AggregationComponent,
    DataSectionComponent,
    BatchReportComponent,
    BatchReportPageComponent,
    ColumnComponent,
  ],
  imports: [CommonModule, SharedModule, RouterModule.forChild(routes), AkitaNgRouterStoreModule],
})
export class DashboardModule {}
