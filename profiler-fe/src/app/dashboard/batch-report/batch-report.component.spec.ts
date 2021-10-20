import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BatchReportComponent } from './batch-report.component';

describe('BatchReportComponent', () => {
  let component: BatchReportComponent;
  let fixture: ComponentFixture<BatchReportComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BatchReportComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BatchReportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
