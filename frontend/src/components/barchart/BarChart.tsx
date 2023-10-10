import { ReactElement } from 'react';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';
import * as forecastData from '../../utils/mock-forecast.json';
import * as actualData from '../../utils/mock-actual.json';
import styles from './BarChart.module.scss';
import ExcelButton from '../excel-button/ExcelButton';
import FiltersButton from '../filters-button/FiltersButton';

export default function BarChart(): ReactElement {
  // extracting sku and forecast values
  const forecastSkus = forecastData.data.map((data) => data.sku);
  const forecastValues = forecastData.data.map((data) => data.forecast);
  const forecastSums = forecastValues.map((forecasts) => {
    return Object.values(forecasts).reduce((acc, value) => acc + value, 0);
  });

  // extracting actual sales values for each sku (in the same order as in forecastSkus)
  const actualValues = forecastSkus.map((sku) => {
    const storeData = actualData.data.find((data) => data.sku_id === sku);
    if (storeData) {
      return storeData.fact.map((fact) => fact.sales_units);
    }
    return [];
  });
  const actualSums = actualValues.map((sales) => {
    return Object.values(sales).reduce((acc, value) => acc + value, 0);
  });

  const chartData = {
    labels: forecastSkus,
    datasets: [
      {
        label: 'Факт продажи, шт.',
        data: actualSums,
        backgroundColor: 'rgba(0, 190, 100, 1)',
        barThickness: 15,
      },
      {
        label: 'Прогноз. шт.',
        data: forecastSums,
        backgroundColor: 'rgba(255, 185, 0, 1)',
        barPercentage: 0.35,
      },
    ],
  };

  const chartOptions = {
    font: {
      size: 30,
    },
    indexAxis: 'y' as const,
    elements: {
      bar: {
        borderWidth: 0,
      },
    },
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: 3,
    plugins: {
      legend: {
        position: 'bottom' as const,
        align: 'center' as const,
        labels: {
          boxWidth: 25,
          boxHeight: 25,
          padding: 32,
          font: {
            family: 'Futura',
            size: 20,
            weight: '450',
          },
        },
      },
    },
    scales: {
      x: {
        border: {
          display: false,
        },
        grid: {
          display: true,
          lineWidth: 4,
        },
        ticks: {
          font: {
            family: 'Futura',
            size: 20,
            weight: '450',
          },
          padding: 8,
        },
      },
      y: {
        border: {
          display: false,
        },
        grid: {
          display: false,
        },
        ticks: {
          font: {
            family: 'Futura',
            size: 20,
            weight: '450',
          },
          padding: 24,
          // callback(value: number): string {
          //   const newthis = this as any;
          //   if (newthis.getLabelForValue(value).length > 50) {
          //     return `${newthis.getLabelForValue(value).substring(0, 45)}...`;
          //   }
          //   return newthis.getLabelForValue(value);
          // },
        },
      },
    },
  };

  return (
    <div className={styles.chartContainer}>
      <div className={styles.controls}>
        <ExcelButton />
        <FiltersButton />
      </div>
      <div className={styles.chartContainer__title}>
        ТК - {forecastData.data[0].store}
      </div>
      <div className={styles.chartContainer__chart}>
        <Bar data={chartData} options={chartOptions} />
      </div>
    </div>
  );
}
