import { Component, ChangeDetectionStrategy, Input, OnInit } from '@angular/core';
import { AggregationBatch, FeatureStatistic } from 'src/app/dashboard/state/dashboard.store';
import * as d3 from 'd3';

@Component({
  selector: 'profiler-column',
  templateUrl: './column.component.html',
  styleUrls: ['./column.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ColumnComponent implements OnInit {
  @Input() column!: AggregationBatch;
  @Input() features: string[] = [];

  colors: string[] = [];

  constructor() {}

  ngOnInit() {
    this.colors = this.features.map((feature) => {
      return this.cellColor(this.column.feature_statistics[feature]);
    });
  }

  tooltip(column: AggregationBatch) {
    return `${new Date(column.file_timestamp)} ${column.batch_name}`;
  }

  cellColor(unsucceeded: FeatureStatistic) {
    if (unsucceeded == undefined) return 'lightgray';

    if (this.column == null) return;

    let { count } = unsucceeded;

    if (count == 0) return;

    let { failed, suspicious } = unsucceeded;

    const failed_multiplier = 10;
    const suspicious_multiplier = 5;

    const failed_score = Math.min((failed / count) * failed_multiplier, 1);
    const suspicious_score = Math.min((suspicious / count) * suspicious_multiplier, 0.5);

    const color = d3.piecewise(d3.interpolateRgb.gamma(1.5), ['#ef4e4e', '#f7c948', '#65d6ad']);
    return color(1 - (failed_score + suspicious_score));
  }
}
