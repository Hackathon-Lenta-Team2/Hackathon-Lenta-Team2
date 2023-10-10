import { ReactElement } from 'react';
import Logo from '../../images/logo.png';
import './loader.scss';

export default function Loader(): ReactElement {
  return (
    <section className='loader'>
      <h1 className='loader__header'>Загружаем данные...</h1>
      <img className='loader__logo' src={Logo} alt='Лого' />
    </section>
  );
}
