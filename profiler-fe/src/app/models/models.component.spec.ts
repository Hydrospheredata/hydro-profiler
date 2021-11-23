import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModelsComponent } from './models.component';
import {ModelsService} from "./state/models.service";
import {MatDialog, MatDialogModule} from "@angular/material/dialog";

describe('ModelsComponent', () => {
  let component: ModelsComponent;
  let fixture: ComponentFixture<ModelsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ModelsComponent],
      imports: [MatDialogModule],
      providers: [{provide: ModelsService, useValue: { getAll: () => {}}}]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ModelsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
