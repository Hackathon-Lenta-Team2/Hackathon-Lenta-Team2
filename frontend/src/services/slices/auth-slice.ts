import {createSlice} from '@reduxjs/toolkit';
import {fetchGetUser, fetchLogin, fetchLogout} from '../async-thunk/auth-thunk';
import {deleteCookie, setCookie} from '../../utils/helpers';

interface IAuthSliceState {
  loginError: null | boolean;
  loginLoading: null | boolean;
  logoutError: null | boolean;
  logoutLoading: null | boolean;
  userError: null | boolean;
  userLoading: null | boolean;
  authToken: string;
  user: any;
}

export const authSlice = createSlice({
  name: 'authSlice',
  initialState: {
    loginError: null,
    loginLoading: null,
    logoutError: null,
    logoutLoading: null,
    userError: null,
    userLoading: null,
    authToken: '',
    user: {},
  } as IAuthSliceState,
  reducers: {},
  extraReducers(builder) {
    builder
      .addCase(fetchLogin.pending, (state) => {
        state.loginLoading = true;
        state.loginError = false;
      })
      .addCase(fetchLogin.fulfilled, (state, action) => {
        state.loginError = false;
        state.loginLoading = false;
        state.authToken = action.payload.auth_token;
        if (action.payload.isUserSaved) {
          setCookie('token', action.payload.auth_token, { path: '/' });
        } else {
          window.sessionStorage.setItem('token', action.payload.auth_token);
        }
      })
      .addCase(fetchLogin.rejected, (state) => {
        state.loginLoading = false;
        state.loginError = true;
      })
      .addCase(fetchLogout.pending, (state) => {
        state.logoutLoading = true;
        state.logoutError = false;
      })
      .addCase(fetchLogout.fulfilled, (state) => {
        state.logoutError = false;
        state.logoutLoading = false;
        deleteCookie('token');
        window.sessionStorage.removeItem('token');
      })
      .addCase(fetchLogout.rejected.type, (state) => {
        state.logoutLoading = false;
        state.logoutError = true;
      })
      .addCase(fetchGetUser.pending, (state) => {
        state.userLoading = true;
        state.userError = false;
      })
      .addCase(fetchGetUser.fulfilled, (state, action) => {
        state.userError = false;
        state.userLoading = false;
        state.user = action.payload;
      })
      .addCase(fetchGetUser.rejected, (state) => {
        state.userLoading = false;
        state.userError = true;
      });
  },
});
