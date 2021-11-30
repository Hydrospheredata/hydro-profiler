import { Overall } from 'src/app/domain/report';
import { EntityFilter } from './utility-filter';

describe('filter', () => {
  let overallFilter: EntityFilter<Overall, keyof Overall>;
  let list: Overall[];

  beforeAll(() => {
    const successOverall: Overall = {
      count: 1,
      succeed: 1,
      suspicious: 0,
      failed: 0,
    };

    const suspiciousOverall: Overall = {
      count: 1,
      succeed: 0,
      suspicious: 1,
      failed: 0,
    };

    const failedOverall: Overall = {
      count: 1,
      succeed: 0,
      suspicious: 0,
      failed: 1,
    };

    list = [successOverall, suspiciousOverall, failedOverall];
  });

  beforeEach(() => {
    overallFilter = new EntityFilter<Overall, keyof Overall>();
  });

  it('empty filter', () => {
    const res = overallFilter.filter(list);
    expect(res.length).toEqual(3);
  });

  it('suspicious filter', () => {
    overallFilter.addFilter('suspicious')((value) => value > 0);
    const res = overallFilter.filter(list);
    expect(res.length).toEqual(1);
  });

  it('suspicious and failed filter', () => {
    overallFilter.addFilter('suspicious')((value) => value > 0);
    overallFilter.addFilter('failed')((value) => value > 0);
    const res = overallFilter.filter(list);
    expect(res.length).toEqual(2);
  });

  it('dynamically behaviour', () => {
    overallFilter.addFilter('suspicious')((value) => value > 0);
    expect(overallFilter.filter(list).length).toEqual(1);

    overallFilter.addFilter('failed')((value) => value > 0);
    expect(overallFilter.filter(list).length).toEqual(2);

    overallFilter.removeFilter('suspicious');
    overallFilter.removeFilter('failed');
    expect(overallFilter.filter(list).length).toEqual(3);
  });
});
