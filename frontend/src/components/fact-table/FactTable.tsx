import { ReactElement, useMemo, useState } from 'react';
import { useTable, Column } from 'react-table';
import styles from './FactTable.module.scss';
import ExcelButton from '../excel-button/ExcelButton';
import FiltersButton from '../filters-button/FiltersButton';
import RowOverlay from '../row-overlay/RowOverlay';

type OverlayPosition = {
  x: number;
  y: number;
};

type TableRowData = {
  store_id: string;
  sku_id: string;
  sales_units: number;
  forecast: number;
  wape: number;
};

interface SalesData {
  date: string;
  sales_type: number;
  sales_units: number;
  sales_units_promo: number;
  sales_rub: number;
  sales_run_promo: number;
}

type FactData = {
  store_id: string;
  sku_id: string;
  fact: SalesData[];
};

type IFactTableProps = {
  sales: FactData[];
};

export default function FactTable({ sales }: IFactTableProps): ReactElement {
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

  // table data
  const data = useMemo(() => {
    const flattened = sales.flatMap((item) =>
      item.fact.map((salesItem) => ({
        store_id: item.store_id,
        sku_id: item.sku_id,
        sales_units: salesItem.sales_units,
        forecast: 0,
        wape: 0.45,
      }))
    );
    return flattened;
  }, [sales]);

  // get columns
  const columns: Column<TableRowData>[] = useMemo(() => {
    if (data.length === 0) return [];

    const columnsArray: Column<TableRowData>[] = [
      {
        Header: 'ТК',
        accessor: 'store_id',
      },
      {
        Header: 'Товар',
        accessor: 'sku_id',
      },
      {
        Header: 'Факт продаж',
        accessor: 'sales_units',
      },
      {
        Header: 'Прогноз',
        accessor: 'forecast',
      },
      {
        Header: 'Разница',
        accessor: (row) => row.sales_units - row.forecast,
      },
      {
        Header: 'Качество прогноза по WAPE',
        accessor: 'wape',
      },
    ];

    return columnsArray;
  }, [data]);

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
