import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BatchReportPageComponent } from './batch-report/batch-report-page.component';
import { DashboardComponent } from './dashboard.component';

const routes: Routes = [
  { path: '', component: DashboardComponent, children: [
    { path: ':batchName', component: BatchReportPageComponent }
  ] },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DashboardRoutingModule { }
