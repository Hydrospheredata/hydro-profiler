import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { ModelsService } from '../state/models.service';
import { Model } from '../state/models.store';

@Component({
  templateUrl: './add-dialog.component.html',
  styleUrls: ['./add-dialog.component.scss'],
})
export class AddDialogComponent {
  contract: File | undefined = undefined;
  training: File | undefined = undefined;
  formGroup: FormGroup = this.fb.group({
    name: ['', Validators.required],
    version: ['', Validators.required],
    contract: ['', Validators.required],
    training: ['', Validators.required],
  });
  error = '';
  succeed = false;
  constructor(
    private fb: FormBuilder,
    private service: ModelsService,
    public dialogRef: MatDialogRef<AddDialogComponent>,
  ) {}

  handleContract(evt: any) {
    console.log(evt.target.files[0]);
    this.contract = evt.target.files[0];
  }

  handleTraining(evt: any) {
    console.log(evt.target.files[0]);
    this.training = evt.target.files[0];
  }

  onSubmit() {
    const fd = new FormData();

    fd.append('contract', this.contract as File);
    fd.append('training', this.training as File);
    fd.append('name', this.formGroup.get('name')?.value);
    fd.append('version', this.formGroup.get('version')?.value);

    this.service.registerModel(fd).subscribe(
      (model) => {
        this.succeed = true;
        this.service.addModel(model as Model);
      },
      (err) => {
        this.error = err;
      },
    );

    // this.dialogRef.close()
  }
}
