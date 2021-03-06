export interface FeatureScore {
  [feature: string]: {
    score: number;
  };
}

export interface Aggregation {
  features: string[];
  inputs: string[];
  outputs: string[];
  aggregates: Array<FeatureScore>;
}
export const f1: FeatureScore = {
  x1: { score: 1 },
  x2: { score: 0.5 },
  y: { score: 0 },
};
export const f2: FeatureScore = {
  x1: { score: 0.9 },
  x2: { score: 0.8 },
  y: { score: 0.7 },
};
export const f3: FeatureScore = {
  x1: { score: 0.3 },
  x2: { score: 0.2 },
  y: { score: 0.1 },
};
export const f4: FeatureScore = {
  x1: { score: 0.4 },
  x2: { score: 0.5 },
  y: { score: 0.6 },
};

export const testAggRes: Aggregation = {
  features: ['x1', 'x2', 'y'],
  inputs: ['x1', 'x2'],
  outputs: ['y2'],
  aggregates: [f1, f2, f3, f4],
};
