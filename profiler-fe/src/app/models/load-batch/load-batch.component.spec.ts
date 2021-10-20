import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoadBatchComponent } from './load-batch.component';

describe('LoadBatchComponent', () => {
  let component: LoadBatchComponent;
  let fixture: ComponentFixture<LoadBatchComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LoadBatchComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LoadBatchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
