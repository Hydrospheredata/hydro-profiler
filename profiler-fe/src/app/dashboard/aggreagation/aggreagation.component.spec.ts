import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AggreagationComponent } from './aggreagation.component';

describe('AggreagationComponent', () => {
  let component: AggreagationComponent;
  let fixture: ComponentFixture<AggreagationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AggreagationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AggreagationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
