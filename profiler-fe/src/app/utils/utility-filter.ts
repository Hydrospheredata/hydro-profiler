export class EntityFilter<T, U extends keyof T> {
  filters: Map<string, (value: T) => boolean> = new Map();
  addFilter = (filterName: string) => (fn: (value: T) => boolean) =>
    this.filters.set(filterName, fn);
  removeFilter = (key: string) => this.filters.delete(key);
  filter = (xs: Array<T>) => {
    if (this.filters.size == 0) {
      return xs;
    }

    return xs.filter((x) => [...this.filters.entries()].some(([_, fn]) => fn(x)));
  };
  getByKey = (obj: T, key: U) => obj[key];
}

export const moreThanZero = (value: number) => value > 0;
