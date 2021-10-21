import { Component, OnInit } from '@angular/core';
import { ModelsQuery } from './state/models.query';
import { ModelsService } from './state/models.service';
import { MatDialog } from '@angular/material/dialog';
import { AddDialogComponent } from './add-dialog/add-dialog.component';
import { LoadBatchComponent } from './load-batch/load-batch.component';

@Component({
  selector: 'profiler-models',
  templateUrl: './models.component.html',
  styleUrls: ['./models.component.scss'],
})
export class ModelsComponent implements OnInit {
  models$ = this.query.models$;

  constructor(
    private service: ModelsService,
    private query: ModelsQuery,
    public dialog: MatDialog,
  ) {}

  ngOnInit(): void {
    this.service.getAll();
  }

  openLoadBatch(evt: Event, modelName: string, modelVersion: number) {
    evt.stopPropagation();
    const dialogRef = this.dialog.open(LoadBatchComponent, {
      width: '450px',
      data: { modelName, modelVersion },
    });
  }

  openDialog() {
    const dialogRef = this.dialog.open(AddDialogComponent, {
      width: '450px',
    });

    dialogRef.afterClosed().subscribe((result) => {
      console.log('The dialog was closed');
    });
  }
}
