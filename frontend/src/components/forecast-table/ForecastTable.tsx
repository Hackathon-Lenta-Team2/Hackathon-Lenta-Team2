import { ReactElement, useMemo, useState } from 'react';
import { useTable, Column } from 'react-table';
import { formatDate, calculateColumnsPerPage } from '../../utils/helpers';
import styles from './ForecastTable.module.scss';
import ExcelButton from '../excel-button/ExcelButton';
import FiltersButton from '../filters-button/FiltersButton';
import RowOverlay from '../row-overlay/RowOverlay';

type OverlayPosition = {
  x: number;
  y: number;
};

type Forecasts = {
  data: Record<string, number>[]
}

interface ForecastData {
  store: string;
  sku: string;
  forecast_date: string;
  forecast_data: Forecasts[];
}

type IForecastTableProps = {
  forecasts: ForecastData[];
};

export default function ForecastTable({
  forecasts,
}: IForecastTableProps): ReactElement {
  const data = useMemo(() => forecasts, [forecasts]);
  const [currentPage, setCurrentPage] = useState(0);
  console.log(`forecasts=${JSON.stringify(data)}`);

  // click on row
  const [isOverlayOpen, setIsOverlayOpen] = useState<boolean>(false);
  const [overlayPosition, setOverlayPosition] =
    useState<OverlayPosition | null>(null);

  const handleRowClick = (event: React.MouseEvent<HTMLTableRowElement>) => {
    const x = event.clientX;
    const y = event.clientY - 220;

    setOverlayPosition({ x, y });
    setIsOverlayOpen(true);
  };

  const closeOverlay = () => {
    setIsOverlayOpen(false);
    setOverlayPosition(null);
  };

  // calculate columns per page
  const forecastDays: number = Object.keys(data[0].forecast_data).length;
  const columnsPerPage = calculateColumnsPerPage(forecastDays);

  // get columns
  const columns: Column[] = useMemo(() => {
    if (data.length === 0) return [];

    const forecastDates = Object.keys(data[0].forecast_data[0].data);

    const columnsArray: Column[] = [
      {
        Header: 'ТК',
        accessor: 'store',
      },
      {
        Header: 'SKU',
        accessor: 'sku',
      },
    ];

    const startIndex = currentPage * columnsPerPage;
    const endIndex = startIndex + columnsPerPage;

    const forecastColumns: Column[] = forecastDates
      .slice(startIndex, endIndex) // Slice columns based on the current page
      .map((date) => ({
        Header: formatDate(date),
        accessor: `forecast_data[0].data.${date}`,
      }));

    return columnsArray.concat(forecastColumns);
  }, [data, currentPage, columnsPerPage]);

  // pagination variables
  const nextPage = () => {
    if (currentPage < Math.ceil(columns.length / columnsPerPage) - 1) {
      setCurrentPage(currentPage + 1);
    }
  };

  const prevPage = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
  };

  // disabled button classes
  const backBtnDisabledClass =
    currentPage === 0 ? styles.pagination__bkBtnDisabled : '';
  const fwdBtnDisabledClass =
    currentPage === Math.ceil(columns.length / columnsPerPage) - 1
      ? styles.pagination__fwdBtnDisabled
      : '';

  // get table props from useTable
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable({ columns, data });

  return (
    /* eslint-disable react/jsx-props-no-spreading */
    <div className={styles.tableContainer}>
      <div className={styles.tableWrapper}>
        <div className={styles.controls}>
          <ExcelButton />
          <FiltersButton />
          <div className={styles.pagination}>
            <button
              onClick={prevPage}
              disabled={currentPage === 0}
              type='button'
              className={`${styles.pagination__backBtn} ${backBtnDisabledClass}`}
              aria-label='backBtn'
            />
            <button
              onClick={nextPage}
              disabled={
                currentPage === Math.ceil(columns.length / columnsPerPage) - 1
              }
              type='button'
              className={`${styles.pagination__fwdBtn} ${fwdBtnDisabledClass}`}
              aria-label='fwdBtn'
            />
          </div>
        </div>

        <table {...getTableProps()} className={styles.table}>
          <thead>
            {headerGroups.map((headerGroup) => {
              const { key: headerKey, ...restHeaderProps } =
                headerGroup.getHeaderGroupProps();

              return (
                <tr
                  key={headerKey}
                  {...restHeaderProps}
                  className={styles.table__headerRow}
                >
                  {headerGroup.headers.map((column) => {
                    const { key: columnKey, ...restColumnProps } =
                      column.getHeaderProps();

                    return (
                      <th
                        key={columnKey}
                        {...restColumnProps}
                        className={styles.table__headerCell}
                      >
                        {column.render('Header')}
                      </th>
                    );
                  })}
                </tr>
              );
            })}
          </thead>
          <tbody {...getTableBodyProps()} className={styles.table__body}>
            {rows.map((row) => {
              prepareRow(row);
              return (
                <tr
                  {...row.getRowProps()}
                  className={styles.table__bodyRow}
                  key={row.id}
                  onClick={handleRowClick}
                >
                  {row.cells.map((cell) => {
                    const { key, ...restCellProps } = cell.getCellProps();
                    return (
                      <td
                        key={key}
                        {...restCellProps}
                        className={styles.table__bodyCell}
                      >
                        {cell.render('Cell')}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
        {isOverlayOpen && overlayPosition && (
          <RowOverlay
            onClose={closeOverlay}
            style={{
              position: 'absolute',
              top: `${overlayPosition.y}px`,
              left: `${overlayPosition.x}px`,
            }}
          />
        )}
      </div>
    </div>
    /* eslint-enable react/jsx-props-no-spreading */
  );
}
