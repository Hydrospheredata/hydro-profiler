import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LayoutComponent } from './layout.component';

const routes: Routes = [
  {
    path: '',
    component: LayoutComponent,
    children: [
      { path: 'models', loadChildren: () => import('../models/models.module').then(m => m.ModelsModule) },
      { path: ':modelName/:modelVersion/dashboard', loadChildren: () => import('../dashboard/dashboard.module').then(m => m.DashboardModule) },
    ]
    // children: [
    //   {
    //     path: 'visualization',
    //     loadChildren: () =>
    //       import('../features/visualization/visualization.module').then(
    //         (m) => m.VisualizationModule
    //       ),
    //   },
    // ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class LayoutRoutingModule {}
