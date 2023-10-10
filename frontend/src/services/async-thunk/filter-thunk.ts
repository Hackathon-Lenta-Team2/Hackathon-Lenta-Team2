import axios from 'axios';
import {createAsyncThunk} from '@reduxjs/toolkit';
import {baseAuth} from '../../utils/constants';
import {checkAnswer, getToken, serializeDate} from '../../utils/helpers';


export const getStores = async () => {
  try {
    const res = await axios({
      method: 'GET',
      url: `${baseAuth}/stores`,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${getToken()}`,
      },
    });
    return checkAnswer(res);
  } catch (err) {
    if (axios.isAxiosError(err)) {
      return Promise.reject(err.message);
    }
    return Promise.reject(err);
  }
};

export const fetchGetStores = createAsyncThunk(
  'filters/fetchGetStores',
  async (_, thunkApi) => {
    try {
      const res = await getStores();
      return res.data;
    } catch (err) {
      if (axios.isAxiosError(err)) {
        return thunkApi.rejectWithValue(err.message);
      }
      return thunkApi.rejectWithValue(err);
    }
  }
);

export const getGroups = async () => {
  try {
    const res = await axios({
      method: 'GET',
      url: `${baseAuth}/groups`,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${getToken()}`,
      },
    });
    return checkAnswer(res);
  } catch (err) {
    if (axios.isAxiosError(err)) {
      return Promise.reject(err.message);
    }
    return Promise.reject(err);
  }
};

export const fetchGetGroups = createAsyncThunk(
  'filters/fetchGetGroups',
  async (_, thunkApi) => {
    try {
      const res = await getGroups();
      return res.data;
    } catch (err) {
      if (axios.isAxiosError(err)) {
        return thunkApi.rejectWithValue(err.message);
      }
      return thunkApi.rejectWithValue(err);
    }
  }
);

export const getCategories = async () => {
  try {
    const res = await axios({
      method: 'GET',
      url: `${baseAuth}/categories`,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${getToken()}`,
      },
    });
    return checkAnswer(res);
  } catch (err) {
    if (axios.isAxiosError(err)) {
      return Promise.reject(err.message);
    }
    return Promise.reject(err);
  }
};

export const fetchGetCategories = createAsyncThunk(
  'filters/fetchGetCategories',
  async (_, thunkApi) => {
    try {
      const res = await getCategories();
      return res.data;
    } catch (err) {
      if (axios.isAxiosError(err)) {
        return thunkApi.rejectWithValue(err.message);
      }
      return thunkApi.rejectWithValue(err);
    }
  }
);

export const getSubcategories = async () => {
  try {
    const res = await axios({
      method: 'GET',
      url: `${baseAuth}/subcategories`,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${getToken()}`,
      },
    });
    return checkAnswer(res);
  } catch (err) {
    if (axios.isAxiosError(err)) {
      return Promise.reject(err.message);
    }
    return Promise.reject(err);
  }
};

export const fetchGetSubcategories = createAsyncThunk(
  'filters/fetchGetSubcategories',
  async (_, thunkApi) => {
    try {
      const res = await getSubcategories();
      return res.data;
    } catch (err) {
      if (axios.isAxiosError(err)) {
        return thunkApi.rejectWithValue(err.message);
      }
      return thunkApi.rejectWithValue(err);
    }
  }
);

export const getProducts = async () => {
  try {
    const res = await axios({
      method: 'GET',
      url: `${baseAuth}/products`,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${getToken()}`,
      },
    });
    return checkAnswer(res);
  } catch (err) {
    if (axios.isAxiosError(err)) {
      return Promise.reject(err.message);
    }
    return Promise.reject(err);
  }
};

export const fetchGetProducts = createAsyncThunk(
  'filters/fetchGetProducts',
  async (_, thunkApi) => {
    try {
      const res = await getProducts();
      return res.data;
    } catch (err) {
      if (axios.isAxiosError(err)) {
        return thunkApi.rejectWithValue(err.message);
      }
      return thunkApi.rejectWithValue(err);
    }
  }
);

export const getSales = async ({
  stores,
  skus,
  date_after,
  date_before,
}: {
  stores: Array<string>;
  skus: Array<string>;
  date_after: Date | null;
  date_before: Date | null;
}) => {
  try {
    const res = await axios({
      method: 'GET',
      url: `${baseAuth}/sales`,
      params: {
        store: stores,
        sku: skus,
        date_after: serializeDate(date_after),
        date_before: serializeDate(date_before),
      },
      paramsSerializer: {
        indexes: null,
      },
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${getToken()}`,
      },
    });
    return checkAnswer(res);
  } catch (err) {
    if (axios.isAxiosError(err)) {
      return Promise.reject(err.message);
    }
    return Promise.reject(err);
  }
};

export const fetchGetSales = createAsyncThunk(
  'filters/fetchGetSales',
  async (
    {
      stores,
      skus,
      date_after,
      date_before,
    }: {
      stores: Array<string>;
      skus: Array<string>;
      date_after: Date | null;
      date_before: Date | null;
    },
    thunkApi
  ) => {
    try {
      const res = await getSales({
        stores,
        skus,
        date_after,
        date_before,
      });
      return res.data;
    } catch (err) {
      if (axios.isAxiosError(err)) {
        return thunkApi.rejectWithValue(err.message);
      }
      return thunkApi.rejectWithValue(err);
    }
  }
);

export const getForecasts = async ({
  stores,
  skus,
  start_date,
  end_date,
}: {
  stores: Array<string>;
  skus: Array<string>;
  start_date: Date | null;
  end_date: Date | null;
}) => {
  try {
    const res = await axios({
      method: 'GET',
      url: `${baseAuth}/forecasts`,
      params: {
        store: stores,
        sku: skus,
        start_date: serializeDate(start_date),
        end_date: serializeDate(end_date),
      },
      paramsSerializer: {
        indexes: null,
      },
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${getToken()}`,
      },
    });
    return checkAnswer(res);
  } catch (err) {
    if (axios.isAxiosError(err)) {
      return Promise.reject(err.message);
    }
    return Promise.reject(err);
  }
};

export const fetchGetForecasts = createAsyncThunk(
  'filters/fetchGetForecasts',
  async (
    {
      stores,
      skus,
      start_date,
      end_date,
    }: {
      stores: Array<string>;
      skus: Array<string>;
      start_date: Date | null;
      end_date: Date | null;
    },
    thunkApi
  ) => {
    try {
      const res = await getForecasts({
        stores,
        skus,
        start_date,
        end_date,
      });
      return res.data;
    } catch (err) {
      if (axios.isAxiosError(err)) {
        return thunkApi.rejectWithValue(err.message);
      }
      return thunkApi.rejectWithValue(err);
    }
  }
);
