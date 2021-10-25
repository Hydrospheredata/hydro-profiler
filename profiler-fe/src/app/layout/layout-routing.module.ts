import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  // {
  //   path: '',
  //   redirectTo: 'models',
  //   pathMatch: 'full',
  //   children: [
  //     {
  //       path: 'models',
  //       loadChildren: () => import('../models/models.module').then((m) => m.ModelsModule),
  //     },
  //     {
  //       path: ':modelName/:modelVersion/dashboard',
  //       loadChildren: () => import('../dashboard/dashboard.module').then((m) => m.DashboardModule),
  //     },
  //   ]
  // }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class LayoutRoutingModule {}
