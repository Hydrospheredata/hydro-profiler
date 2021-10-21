import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ModelsService } from '../state/models.service';

@Component({
  templateUrl: './load-batch.component.html',
  styleUrls: ['./load-batch.component.scss'],
})
export class LoadBatchComponent {
  formGroup: FormGroup = this.fb.group({
    batch: ['', Validators.required],
  });
  batch: File | undefined = undefined;
  error = '';
  succeed = false;

  constructor(
    private fb: FormBuilder,
    private service: ModelsService,
    public dialogRef: MatDialogRef<LoadBatchComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { modelName: string; modelVersion: number },
  ) {
    console.log(data);
  }

  handleBatch(evt: any) {
    this.batch = evt.target.files[0];
  }

  onSubmit() {
    const fd = new FormData();

    fd.append('model_name', this.data.modelName);
    fd.append('batch_name', (this.batch as File).name);
    fd.append('model_version', `${this.data.modelVersion}`);
    fd.append('batch', this.batch as File);

    this.service.loadBatch(fd).subscribe(
      () => {
        this.succeed = true;
      },
      (error) => {
        this.error = error;
      },
    );
  }
}
