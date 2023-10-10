import {store} from './store';

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export type TUser = {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
};
export type TStore = {
  id: string;
  title: string;
  is_active: boolean;
  city: string;
  division: string;
  type_format: number;
  loc: number;
  size: number;
};
export type TGroup = {
  id: string;
};
export type TCategory = {
  id: string;
  group_id: string;
};
export type TSubcategory = {
  id: string;
  category_id: string;
};
export type TProduct = {
  id: string;
  title: string;
  group_id: string;
  cat_id: string;
  subcat_id: string;
  uom_id: number;
};
