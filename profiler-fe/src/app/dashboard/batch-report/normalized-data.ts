import { CheckStatus } from 'src/app/domain/check';
import { Overall } from 'src/app/domain/report';

export type FilterKind = 'succeed' | 'failed' | 'suspicious';

export interface NormalizedCheck {
  feature: string;
  status: CheckStatus;
  metricType: String;
  description: string;
  style_class: string;
}

export interface NormalizedDataItem {
  row_id: string;
  count: number;
  succeed: number;
  suspicious: number;
  failed: number;
  row_color: string;
  checks: NormalizedCheck[];
}

export type RowsIndexes = Record<FilterKind, number[]>;

export interface NormalizedReport {
  rows_overall: Overall;
  report: NormalizedDataItem[];
  indexes: RowsIndexes;
}
