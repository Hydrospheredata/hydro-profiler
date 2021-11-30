export class EntityFilter<T, U extends keyof T> {
  filters: Map<U, (value: T[U]) => boolean> = new Map();
  addFilter = (key: U) => (fn: (value: T[U]) => boolean) => this.filters.set(key, fn);
  removeFilter = (key: U) => this.filters.delete(key);
  filter = (xs: Array<T>) => {
    if (this.filters.size == 0) {
      return xs;
    }

    return xs.filter((x) => [...this.filters.entries()].some(([key, fn]) => fn(x[key])));
  };
  getByKey = (obj: T, key: U) => obj[key];
}

export const moreThanZero = (value: number) => value > 0;
