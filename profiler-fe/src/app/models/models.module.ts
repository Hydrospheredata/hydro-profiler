import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ModelsRoutingModule } from './models-routing.module';
import { ModelsComponent } from './models.component';
import { FormsModule, ReactiveFormsModule} from '@angular/forms'
import { MatFormFieldModule } from '@angular/material/form-field'
import { MatInputModule } from '@angular/material/input'
import { MatToolbarModule} from '@angular/material/toolbar'
import { MatTableModule } from '@angular/material/table'
import { MatButtonModule} from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { AddDialogComponent } from './add-dialog/add-dialog.component';
import { LoadBatchComponent } from './load-batch/load-batch.component'
import { SharedModule } from '../shared/shared.module';

@NgModule({
  declarations: [
    ModelsComponent,
    AddDialogComponent,
    LoadBatchComponent
  ],
  imports: [
    CommonModule,
    ModelsRoutingModule,
    ReactiveFormsModule,
    FormsModule,
    SharedModule
  ],
  entryComponents: [AddDialogComponent, LoadBatchComponent]
})
export class ModelsModule { }
