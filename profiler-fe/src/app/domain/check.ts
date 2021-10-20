export type CheckStatus = "succeed" | "failed" | "suspicious";

export interface Check {
    status: CheckStatus
    description: string
    count_score: boolean
    metric_type: string
}