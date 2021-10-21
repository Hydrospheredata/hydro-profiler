import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ModelsRoutingModule } from './models-routing.module';
import { ModelsComponent } from './models.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AddDialogComponent } from './add-dialog/add-dialog.component';
import { LoadBatchComponent } from './load-batch/load-batch.component';
import { SharedModule } from '../shared/shared.module';

@NgModule({
  declarations: [ModelsComponent, AddDialogComponent, LoadBatchComponent],
  imports: [CommonModule, ModelsRoutingModule, ReactiveFormsModule, FormsModule, SharedModule],
  entryComponents: [AddDialogComponent, LoadBatchComponent],
})
export class ModelsModule {}
