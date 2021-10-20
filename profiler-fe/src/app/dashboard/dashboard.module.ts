import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DashboardRoutingModule } from './dashboard-routing.module';
import { DashboardComponent } from './dashboard.component';
import { AggreagationComponent } from './aggreagation/aggreagation.component';
import { DataSectionComponent } from './aggreagation/components/data-section/data-section.component';
import { BatchReportComponent } from './batch-report/batch-report.component';
import { BatchReportPageComponent } from './batch-report/batch-report-page.component';
import { SharedModule } from '../shared/shared.module';

@NgModule({
  declarations: [
    DashboardComponent,
    AggreagationComponent,
    DataSectionComponent,
    BatchReportComponent,
    BatchReportPageComponent,

  ],
  imports: [
    CommonModule,
    DashboardRoutingModule,
    SharedModule
  ]
})
export class DashboardModule { }
