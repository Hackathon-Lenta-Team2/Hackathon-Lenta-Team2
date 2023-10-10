import { ReactElement } from 'react';

type PaginationProps = {
  currentPage: number;
  totalPages: number;
  onNextPage: () => void;
  onPrevPage: () => void;
};

function Pagination({
  currentPage,
  totalPages,
  onNextPage,
  onPrevPage,
}: PaginationProps): ReactElement {
  return (
    <div>
      <button onClick={onPrevPage} disabled={currentPage === 0} type='button'>
        Previous
      </button>
      <button
        onClick={onNextPage}
        disabled={currentPage === totalPages - 1}
        type='button'
      >
        Next
      </button>
    </div>
  );
}

export default Pagination;
