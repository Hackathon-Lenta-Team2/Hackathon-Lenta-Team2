import React from 'react';
import styles from './RowOverlay.module.scss';

type OverlayProps = {
  onClose: () => void;
  style: React.CSSProperties;
};

function RowOverlay({ onClose, style }: OverlayProps): React.ReactElement {
  return (
    <div className={styles.overlayContainer} style={style}>
      <div className={styles.overlayContent}>
        <p className={styles.overlayContent__text}>
          Наименование и описание товара
        </p>
        <div>
          <p className={styles.overlayContent__text}>Группа:</p>
          <p className={styles.overlayContent__subtitle}>
            Название группы товара
          </p>
        </div>
        <div>
          <p className={styles.overlayContent__text}>Категория:</p>
          <p className={styles.overlayContent__subtitle}>
            Название категории товара
          </p>
        </div>
        <div>
          <p className={styles.overlayContent__text}>Подкатегория:</p>
          <p className={styles.overlayContent__subtitle}>
            Название подкатегории товара
          </p>
        </div>
        <button
          className={styles.overlayContent__btn}
          onClick={onClose}
          type='button'
          aria-label='close-overlay'
        />
      </div>
    </div>
  );
}

export default RowOverlay;
