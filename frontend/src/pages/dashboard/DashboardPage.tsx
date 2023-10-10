import {ReactElement, useEffect, useState} from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../../services/types';
import ResultsHeading from '../../components/results-heading/ResultsHeading';
import ResultsTabs from '../../components/results-tabs/ResultsTabs';
import DoughnutChart from '../../components/doughnut-chart/DoughnutChart';
import BarChart from '../../components/barchart/BarChart';
import styles from './DashboardPage.module.scss';
import * as forecastData from '../../utils/mock-forecast.json';
import {useParams} from "react-router-dom";
import {useDispatch} from "../../services/hooks/useDispatch";
import {fetchGetForecasts, fetchGetSales} from "../../services/async-thunk/filter-thunk";
import NotFound404 from "../not-found";
import Loader from "../../components/loader/loader";
import NoResults from "../no-results";
// import * as salesData from '../../utils/mock-actual.json';

export default function DashboardPage(): ReactElement {
  const { dataType } = useParams();
  const [isLoaded, setIsLoaded] = useState<boolean>(false);
  const sales = useSelector((state: RootState) => state.filter.sales);
  const startSalesDate = sales.length !== 0 ? sales[0].fact[0].date : '';
  const endSalesDate =
    sales.length !== 0 ? sales[0].fact[sales[0].fact.length - 1].date : '';

  const isForecast = dataType === 'forecast';
  const selectedStores = useSelector((store: RootState) => store.filter.selectedStores);
  const selectedProducts = useSelector((store: RootState) => store.filter.selectedProducts);
  const factStartDate = useSelector((store: RootState) => store.filter.factStartDate);
  const factEndDate = useSelector((store: RootState) => store.filter.factEndDate);
  const forecasts = useSelector((store: RootState) => store.filter.forecasts);
  const forecastStartDate = useSelector((store: RootState) => store.filter.forecastStartDate);
  const forecastEndDate = useSelector((store: RootState) => store.filter.forecastEndDate);

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
  const days: number = Object.keys(forecastData.data[0].forecast).length;

  if (dataType !== 'fact' && dataType !== 'forecast') return <NotFound404 />;

  if (isLoaded && (forecasts.length === 0 && sales.length === 0)) return <NoResults />;

  if (isForecast) {
    if (forecasts.length === 0 || !(selectedStores && selectedProducts && forecastStartDate  && forecastEndDate)) {
      return <Loader />;
    }
  } else {
    if (sales.length === 0 || !(selectedStores && selectedProducts && factStartDate && factEndDate)) {
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
        <DoughnutChart forecasts={forecastData.data} />
      ) : (
        <BarChart />
      )}
    </div>
  );
}
