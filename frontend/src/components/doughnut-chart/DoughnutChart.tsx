import { ReactElement } from 'react';
import { Doughnut } from 'react-chartjs-2';
import styles from './DoughnutChart.module.scss';
import ExcelButton from '../excel-button/ExcelButton';
import FiltersButton from '../filters-button/FiltersButton';

type SkuSumEntry = {
  sku: string;
  sum: number;
};

interface ForecastData {
  store: string;
  sku: string;
  forecast_date: string;
  forecast: Record<string, number>;
}

type IDoughnutChartProps = {
  forecasts: ForecastData[];
};

export default function DoughnutChart({
  forecasts,
}: IDoughnutChartProps): ReactElement {
  // Calculate the sum of forecasts for each SKU
  const skuSumMap: Record<string, number> = {};

  forecasts.forEach((forecast) => {
    const { sku, forecast: forecastData } = forecast;
    const sum = Object.values(forecastData).reduce(
      (acc, value) => acc + value,
      0
    );
    skuSumMap[sku] = sum;
  });

  // Convert into an array of objects
  const skuArr: SkuSumEntry[] = Object.entries(skuSumMap).map(([sku, sum]) => ({
    sku,
    sum,
  }));

  // Sort the array (descending order by sum)
  skuArr.sort((a, b) => b.sum - a.sum);

  // Check if the length of skuArr is greater than 5
  if (skuArr.length > 5) {
    const restSum = skuArr.slice(4).reduce((acc, entry) => acc + entry.sum, 0);

    const newSkuMap: Record<string, number> = {};
    skuArr.slice(0, 4).forEach((entry) => {
      newSkuMap[entry.sku] = entry.sum;
    });
    newSkuMap.rest = restSum;

    skuArr.length = 0;
    skuArr.push(
      ...Object.entries(newSkuMap).map(([sku, sum]) => ({ sku, sum }))
    );
  }

  const chartData = {
    labels: skuArr.map((entry) => entry.sku),
    datasets: [
      {
        data: skuArr.map((entry) => entry.sum),
        backgroundColor: [
          '#FFB900',
          '#003C96',
          '#2FCBFF',
          '#00BE64',
          '#4D4D4D',
        ],
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: 1,
    cutout: '70%',
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  return (
    <div className={styles.chartsContainer}>
      <div className={styles.controls}>
        <ExcelButton />
        <FiltersButton />
      </div>
      <div className={styles.chartsContainer__chart}>
        <p className={styles.chartsContainer__tk}>ТК - id111</p>
        <div className={styles.chartsContainer__chartWrapper}>
          <Doughnut data={chartData} options={chartOptions} />
        </div>
        <div className={styles.legend}>
          {skuArr.map((entry) => (
            <div className={styles.legend__row} key={entry.sku}>
              <div className={styles.legend__colorBox} />
              <p className={styles.legend__label}>{entry.sku}</p>
              <p className={styles.legend__value}>{entry.sum}</p>
            </div>
          ))}
        </div>
      </div>
      <div className={styles.chartsContainer__chart}>
        <p className={styles.chartsContainer__tk}>ТК - id111</p>
        <div className={styles.chartsContainer__chartWrapper}>
          <Doughnut data={chartData} options={chartOptions} />
        </div>
        <div className={styles.legend}>
          {skuArr.map((entry) => (
            <div className={styles.legend__row} key={entry.sku}>
              <div className={styles.legend__colorBox} />
              <p className={styles.legend__label}>{entry.sku}</p>
              <p className={styles.legend__value}>{entry.sum}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
