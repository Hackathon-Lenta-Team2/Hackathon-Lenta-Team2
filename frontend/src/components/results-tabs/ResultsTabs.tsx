import { ReactElement } from 'react';
import { useNavigate, useLocation, useParams } from 'react-router-dom';
import styles from './ResultsTabs.module.scss';

export default function ResultsTabs(): ReactElement {
  const { dataType } = useParams();
  const navigate = useNavigate();
  const location = useLocation();

  const activeTableBtnClass = location.pathname.includes('/results/table')
    ? styles.resultsTabs__btn_active
    : '';
  const activeDashboardBtbClass = location.pathname.includes('/results/dashboard')
    ? styles.resultsTabs__btn_active
    : '';

  const handleTableBtnClick = (): void => {
    navigate(`/results/table/${dataType}`);
  };

  const handleDashboardBtnClick = (): void => {
    navigate(`/results/dashboard/${dataType}`);
  };

  return (
    <div className={styles.resultsTabs}>
      <button
        className={`${styles.resultsTabs__btn} ${activeTableBtnClass}`}
        type='button'
        onClick={handleTableBtnClick}
      >
        Таблица
      </button>
      <button
        className={`${styles.resultsTabs__btn} ${activeDashboardBtbClass}`}
        type='button'
        onClick={handleDashboardBtnClick}
      >
        Дашборд
      </button>
    </div>
  );
}
