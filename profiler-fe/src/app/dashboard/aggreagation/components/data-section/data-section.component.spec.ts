import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataSectionComponent } from './data-section.component';
import {RouterTestingModule} from "@angular/router/testing";

describe('DataSectionComponent', () => {
  let component: DataSectionComponent;
  let fixture: ComponentFixture<DataSectionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [DataSectionComponent],
      imports: [RouterTestingModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DataSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
