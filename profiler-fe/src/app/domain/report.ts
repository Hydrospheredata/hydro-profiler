import { Check } from "./check";

export interface Overall {
    failed: number
    suspicious: number
    succeed: number
    count: number
}

export interface ReportItem {
    "_id": string;
    "_raw_checks": {
        [featureName: string]: Check[]
    }
    "_feature_overall": {
        [featureName: string]: Overall
    }
    "_row_overall": Overall
}