/* eslint-disable no-console */
import { ReactElement } from 'react';
import { useSelector } from 'react-redux';
import axios, { AxiosResponse } from 'axios';
import Cookies from 'js-cookie';
import { RootState } from '../../services/types';
import styles from './ExcelButton.module.scss';
import { baseAuth } from '../../utils/constants';

interface SaleItem {
  store_id: string;
  sku_id: string;
  fact: {
    date: string;
    sales_type: number;
    sales_units: number;
    sales_units_promo: number;
    sales_rub: number;
    sales_run_promo: number;
  }[];
}

export default function ExcelButton(): ReactElement {
  const sales = useSelector((store: RootState) => store.filter.sales);
  const stores = sales.map((sale: SaleItem) => sale.store_id);
  const skus = sales.map((sale: SaleItem) => sale.sku_id);

  const handleExportExcel = async () => {
    try {
      const token =
        Cookies.get('token') || window.sessionStorage.getItem('token');

      if (!token) {
        console.error('Token not found in cookies');
        return;
      }

      const storeParams = stores
        .map((store: string) => `store=${store}`)
        .join('&');
      const skuParams = skus.map((sku: string) => `sku=${sku}`).join('&');
      const queryParams = `export=true&${storeParams}&${skuParams}`;

      const requestHeaders = {
        Authorization: `Token ${token}`,
      };

      const response: AxiosResponse<Blob> = await axios.get(
        `${baseAuth}/sales/export/?${queryParams}`,
        {
          responseType: 'blob',
          headers: requestHeaders,
        }
      );

      const blob = new Blob([response.data], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      });
      const url = window.URL.createObjectURL(blob);

      // link element and trigger to download the file
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'exported-data.xlsx';
      document.body.appendChild(a);
      a.click();

      // revoke the temp URL
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting Excel:', error);
    }
  };

  return (
    <button type='button' className={styles.btn} onClick={handleExportExcel}>
      Выгрузить в Excel
    </button>
  );
}
/* eslint-enable no-console */
