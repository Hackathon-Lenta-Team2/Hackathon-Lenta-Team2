import {configureStore} from '@reduxjs/toolkit';
import {authSlice} from './slices/auth-slice';
import {filterSlice} from './slices/filter-slice';

const reducer = {
  profile: authSlice.reducer,
  filter: filterSlice.reducer,
};

export const store = configureStore({
  reducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});
