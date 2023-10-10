import { ReactElement } from 'react';
import { formatDaysWord, formatDate } from '../../utils/helpers';
import styles from './ResultsHeading.module.scss';

type IResultsHeadingProps = {
  days: number;
  isForecast: boolean;
  startDate: string;
  endDate: string;
};

export default function ResultsHeading({
  days,
  isForecast,
  startDate,
  endDate,
}: IResultsHeadingProps): ReactElement {
  const heading: string = isForecast
    ? `Прогноз спроса на ${days} ${formatDaysWord(days)}`
    : `Качество прогноза спроса за период с ${formatDate(
        startDate
      )} по ${formatDate(endDate)}`;

  return <h2 className={styles.heading}>{heading}</h2>;
}
