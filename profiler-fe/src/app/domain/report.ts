export interface Overall {
  failed: number;
  suspicious: number;
  succeed: number;
  count: number;
}

export enum DataRowStatus {
  HAS_FAILED = 'has_failed',
  HAS_SUSPICIOUS = 'has_suspicious',
  HEALTHY = 'healthy',
}

export interface DataRowReport {
  id: number;
  status: DataRowStatus;
  failed_checks: CheckDescription[];
  suspicious_checks: CheckDescription[];
}

export interface CheckDescription {
  feature: string;
  value: any;
  desc: string;
  metric: string;
}

export interface UnsucceedRows {
  [row_id: string]: CheckDescription[]
}

export interface GetModelReportResponse {
  model_name: string;
  model_version: number;
  batch_name: string;
  file_timestamp: string;
  failed_rows: UnsucceedRows;
  suspicious_rows: UnsucceedRows;
  rows_count: number;
}

export interface ModelReport {
  model_name: string;
  model_version: number;
  batch_name: string;
  file_timestamp: string;
  failed_count: number;
  suspicious_count: number;
  rows_count: number;
  rows: DataRowReport[]
}

export function create_model_report(response: GetModelReportResponse):ModelReport {
    const {
      model_name,
      model_version,
      batch_name,
      file_timestamp,
      failed_rows,
      suspicious_rows,
      rows_count
    } = response

    const failed_count = Object.keys(failed_rows).length
    const suspicious_count = Object.keys(suspicious_rows).reduce((acc, id) => {
      return id in failed_rows ? acc : acc + 1
    } , 0)

    const rows:DataRowReport[] = []
    for (let id = 0; id < rows_count; id++) {
      let status: DataRowStatus = DataRowStatus.HEALTHY
      if(id in failed_rows){
        status = DataRowStatus.HAS_FAILED
      } else if(id in suspicious_rows) {
        status = DataRowStatus.HAS_SUSPICIOUS
      }

      const failed_checks = failed_rows[id] || []
      const suspicious_checks = suspicious_rows[id] || []

      rows.push({id, status, failed_checks, suspicious_checks})
    }

    return {
      model_name,
      model_version,
      batch_name,
      file_timestamp,
      failed_count,
      suspicious_count,
      rows_count,
      rows
    }
}
