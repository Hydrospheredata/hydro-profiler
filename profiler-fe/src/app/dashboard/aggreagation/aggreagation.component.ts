import { Component, ChangeDetectionStrategy, Input } from '@angular/core';
import { Aggregation } from '../state/dashboard.store';

@Component({
  selector: 'profiler-aggreagation',
  templateUrl: './aggreagation.component.html',
  styleUrls: ['./aggreagation.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AggreagationComponent {
  @Input() aggregation: Aggregation | null = null;

  constructor() {}
}
