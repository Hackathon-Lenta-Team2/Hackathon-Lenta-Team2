import { useEffect, useState } from 'react';
import { BrowserRouter } from 'react-router-dom';
import './app.css';
import RoutesComponent from '../routes-component/routes-component';
import AppHeader from '../app-header/app-header';
import { useDispatch } from '../../services/hooks/useDispatch';
import {
  fetchGetCategories,
  fetchGetGroups,
  fetchGetProducts,
  fetchGetStores,
  fetchGetSubcategories,
} from '../../services/async-thunk/filter-thunk';
import { getToken } from '../../utils/helpers';
import { fetchGetUser } from '../../services/async-thunk/auth-thunk';
import { filterSlice } from '../../services/slices/filter-slice';
import Loader from '../loader/loader';

export default function App() {
  const dispatch = useDispatch();

  const [isUserLoaded, setUserLoaded] = useState<boolean>(false);

  function loadLocalStorage() {
    dispatch(
      filterSlice.actions.selectStores(
        JSON.parse(window.localStorage.getItem('stores') || '[]')
      )
    );
    dispatch(
      filterSlice.actions.selectGroups(
        JSON.parse(window.localStorage.getItem('groups') || '[]')
      )
    );
    dispatch(
      filterSlice.actions.selectCategories(
        JSON.parse(window.localStorage.getItem('categories') || '[]')
      )
    );
    dispatch(
      filterSlice.actions.selectSubcategories(
        JSON.parse(window.localStorage.getItem('subcategories') || '[]')
      )
    );
    dispatch(
      filterSlice.actions.selectProducts(
        JSON.parse(window.localStorage.getItem('products') || '[]')
      )
    );
    const factStartDate = window.localStorage.getItem('factStartDate');
    const factEndDate = window.localStorage.getItem('factEndDate');
    if (factStartDate) {
      dispatch(filterSlice.actions.selectFactStartDate(new Date(factStartDate)));
    }
    if (factEndDate) {
      dispatch(filterSlice.actions.selectFactEndDate(new Date(factEndDate)));
    }
    const forecastStartDate = window.localStorage.getItem('forecastStartDate');
    const forecastEndDate = window.localStorage.getItem('forecastEndDate');
    if (forecastStartDate) {
      dispatch(filterSlice.actions.selectForecastStartDate(new Date(forecastStartDate)));
    }
    if (forecastEndDate) {
      dispatch(filterSlice.actions.selectForecastEndDate(new Date(forecastEndDate)));
    }
  }

  const init = async () => {
    if (!getToken()) {
      setUserLoaded(true);
      return;
    }
    await dispatch(fetchGetUser());
    await dispatch(fetchGetStores());
    await dispatch(fetchGetGroups());
    await dispatch(fetchGetCategories());
    await dispatch(fetchGetSubcategories());
    await dispatch(fetchGetProducts());
    loadLocalStorage();
    setUserLoaded(true);
  };

  useEffect(() => {
    init();
  }, []);

  /*  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        <Route path='/login' element={<LoginPage />} />
        <Route path='/' element={<ProtectedRoute element={<FilterPage />} />} />
        <Route
          path='results/dashboard'
          element={<ProtectedRoute element={<DashboardPage />} />}
        />
        <Route
          path='results/table'
          element={<ProtectedRoute element={<TablePage />} />}
        />
        <Route
          path='/no-results'
          element={<ProtectedRoute element={<NoResults />} />}
        />
        <Route path='*' element={<NotFound404 />} />
      </>
    )
  );  */

  return (
    /*    <RouterProvider router={router} />  */
    <BrowserRouter>
      <AppHeader />
      {!isUserLoaded ? <Loader /> : <RoutesComponent />}
    </BrowserRouter>
  );
}
