import React from 'react';
import { Provider } from 'react-redux';
import ReactDOM from 'react-dom/client';
import App from './components/app/app';
import './index.css';
import { store } from './services/store';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
);
