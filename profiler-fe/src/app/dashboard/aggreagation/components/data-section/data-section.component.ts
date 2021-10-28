import { Component, ChangeDetectionStrategy, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import * as d3 from 'd3';
import { Aggregation } from 'src/app/dashboard/state/dashboard.store';

@Component({
  selector: 'profiler-data-section',
  templateUrl: './data-section.component.html',
  styleUrls: ['./data-section.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DataSectionComponent {
  @Input() agg: Aggregation | null = null;
  @Input() names: string[] = [];

  readonly labelsWidth: number = 160;
  readonly canvasWidth: number = 720; // 80 column limit * cell.width + padding
  readonly CELL_SIZE = { width: 14, height: 14 };
  private readonly COLUMN_MARGIN_RIGHT = 2;
  private readonly CELL_MARGIN_TOP = 2;

  constructor(private router: Router, private route: ActivatedRoute) {}

  columnTranslate(index: number): string {
    return `translate(${index * this.CELL_SIZE.width + this.COLUMN_MARGIN_RIGHT * index}, 0)`;
  }

  rowTranslate(index: number): string {
    return `translate(2, ${index * this.CELL_SIZE.height + index * this.CELL_MARGIN_TOP})`;
  }

  cellColor(score: number) {
    const color = d3.piecewise(d3.interpolateRgb.gamma(1.5), ['#ef4e4e', '#f7c948', '#65d6ad']);
    return score != undefined ? color(score) : 'lightgrey';
  }

  onColumnClick(column: any) {
    this.router.navigate([column.batch_name], { relativeTo: this.route });
  }

  get canvasHeight() {
    return this.names.length * (this.CELL_SIZE.height + this.CELL_MARGIN_TOP);
  }
}
