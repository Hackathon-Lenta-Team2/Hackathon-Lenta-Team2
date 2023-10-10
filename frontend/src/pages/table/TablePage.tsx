import { ReactElement, useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { RootState } from '../../services/types';
import FactTable from '../../components/fact-table/FactTable';
import ForecastTable from '../../components/forecast-table/ForecastTable';
import ResultsHeading from '../../components/results-heading/ResultsHeading';
import ResultsTabs from '../../components/results-tabs/ResultsTabs';
import styles from './TablePage.module.scss';
// import * as forecastData from '../../utils/mock-forecast.json';
import {
  fetchGetForecasts,
  fetchGetSales,
} from '../../services/async-thunk/filter-thunk';
import { useDispatch } from '../../services/hooks/useDispatch';
import Loader from '../../components/loader/loader';
import NotFound404 from '../not-found';
import NoResults from '../no-results';

export default function TablePage(): ReactElement {
  const { dataType } = useParams();
  const isForecast = dataType === 'forecast';
  const [isLoaded, setIsLoaded] = useState<boolean>(false);
  const sales = useSelector((store: RootState) => store.filter.sales);
  const selectedStores = useSelector(
    (store: RootState) => store.filter.selectedStores
  );
  const selectedProducts = useSelector(
    (store: RootState) => store.filter.selectedProducts
  );
  const factStartDate = useSelector(
    (store: RootState) => store.filter.factStartDate
  );
  const factEndDate = useSelector(
    (store: RootState) => store.filter.factEndDate
  );
  const forecasts = useSelector((store: RootState) => store.filter.forecasts);
  const forecastStartDate = useSelector(
    (store: RootState) => store.filter.forecastStartDate
  );
  const forecastEndDate = useSelector(
    (store: RootState) => store.filter.forecastEndDate
  );

  const startSalesDate = sales.length !== 0 ? sales[0].fact[0].date : '';
  const endSalesDate =
    sales.length !== 0 ? sales[0].fact[sales[0].fact.length - 1].date : '';

  const dispatch = useDispatch();

  useEffect(() => {
    if (isForecast) {
      dispatch(
        fetchGetForecasts({
          stores: selectedStores,
          skus: selectedProducts,
          start_date: forecastStartDate,
          end_date: forecastEndDate,
        })
      ).then(() => setIsLoaded(true));
    } else {
      dispatch(
        fetchGetSales({
          stores: selectedStores,
          skus: selectedProducts,
          date_after: factStartDate,
          date_before: factEndDate,
        })
      ).then(() => setIsLoaded(true));
    }
  }, []);
  // get days
  let days: number = 0;
  if (forecasts.length > 0) {
    days = Object.keys(forecasts[0].forecast_data[0].data).length;
  }

  if (dataType !== 'fact' && dataType !== 'forecast') return <NotFound404 />;

  if (isLoaded && forecasts.length === 0 && sales.length === 0)
    return <NoResults />;
  if (isForecast) {
    if (
      forecasts.length === 0 ||
      !(
        selectedStores &&
        selectedProducts &&
        forecastStartDate &&
        forecastEndDate
      )
    ) {
      return <Loader />;
    }
  } else {
    if (
      sales.length === 0 ||
      !(selectedStores && selectedProducts && factStartDate && factEndDate)
    ) {
      return <Loader />;
    }
  }

  return (
    <div className={styles.tablePage}>
      <ResultsHeading
        days={days}
        isForecast={isForecast}
        startDate={startSalesDate}
        endDate={endSalesDate}
      />
      <ResultsTabs />
      {isForecast ? (
        <ForecastTable forecasts={forecasts} />
      ) : (
        <FactTable sales={sales} />
      )}
    </div>
  );
}
