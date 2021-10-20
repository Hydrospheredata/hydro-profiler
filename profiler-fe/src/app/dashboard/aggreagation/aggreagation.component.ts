import { Component, OnInit, ChangeDetectionStrategy, Input } from '@angular/core';
import { Aggregation } from '../state/dashboard.store';


@Component({
  selector: 'app-aggreagation',
  templateUrl: './aggreagation.component.html',
  styleUrls: ['./aggreagation.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AggreagationComponent implements OnInit {
  @Input() aggregation: Aggregation | null = null

  constructor() {
  }

  ngOnInit(): void {
  }

}
