import { ReactElement, useState } from 'react';
import styles from './FiltersButton.module.scss';
import ResultsFiltersFact from '../results-filters/ResultsFiltersFact';
import ModalOverlay from '../modal-overlay/modal-overlay';

export default function FiltersButton(): ReactElement {
  const [modalOpened, setModalOpened] = useState(false);

  const openModal = () => {
    setModalOpened(true);
  };

  const closeModal = () => {
    setModalOpened(false);
  };

  return (
    <div className={styles.сontainer}>
      <div>
        <button type='button' className={styles.btn} onClick={openModal}>
          <div className={styles.btn__arrow} />
          Фильтры
          <div className={styles.btn__jar} />
        </button>
      </div>
      {modalOpened && (
        <div className={styles.filters}>
          <ModalOverlay opened={modalOpened} onModalClose={closeModal}>
            <ResultsFiltersFact isCalled={modalOpened} />
          </ModalOverlay>
        </div>
      )}
    </div>
  );
}
