import { Component, ChangeDetectionStrategy, Input } from '@angular/core';
import { Aggregation } from '../state/dashboard.store';

@Component({
  selector: 'profiler-aggregation',
  templateUrl: './aggregation.component.html',
  styleUrls: ['./aggregation.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AggregationComponent {
  @Input() aggregation: Aggregation | null = null;

  constructor() {}
}
