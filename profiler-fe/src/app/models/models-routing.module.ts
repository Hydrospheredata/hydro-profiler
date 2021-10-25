import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ModelsComponent } from './models.component';
import {ModelsPageComponent} from "./models-page.component";

const routes: Routes = [
  { path: '',
    component: ModelsPageComponent,
    children: [
      {
        path: '',
        component: ModelsComponent
      },
      {
        path: ':modelName/:modelVersion/dashboard',
        loadChildren: () => import('../dashboard/dashboard.module').then((m) => m.DashboardModule),
      }
  ] },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ModelsRoutingModule {}
