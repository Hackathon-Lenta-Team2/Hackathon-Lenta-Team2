import {ReactElement, useState} from 'react';
import './filter.scss';
import ForecastFilters from '../components/forecast-filters/forecast-filters';
import ActualFilters from '../components/actual-filters/actual-filters';
import Loader from '../components/loader/loader';
import {useSelector} from '../services/hooks/useSelector';

type TabValues = 'Fact' | 'Forecast';

export default function FilterPage(): ReactElement {
  const stores = useSelector((state) => state.filter.stores);
  const groups = useSelector((state) => state.filter.groups);
  const products = useSelector((state) => state.filter.products);
  const [tab, setTab] = useState<TabValues>('Fact');
  function onTabClick(newTab: TabValues) {
    setTab(newTab);

    if (stores.length === 0 || groups.length === 0 || products.length === 0) {
      return <Loader />;
    }
  }

  return (
    <section className='filter'>
      <div className='tab-menu'>
        <button
          type='button'
          className={`tab ${(tab === 'Fact' && 'tab_active') || ''}`}
          onClick={() => onTabClick('Fact')}
        >
          Факт
        </button>
        <button
          type='button'
          className={`tab ${(tab === 'Forecast' && 'tab_active') || ''}`}
          onClick={() => onTabClick('Forecast')}
        >
          Прогноз
        </button>
      </div>
      {tab === 'Fact' ? <ActualFilters /> : <ForecastFilters />}
    </section>
  );
}
