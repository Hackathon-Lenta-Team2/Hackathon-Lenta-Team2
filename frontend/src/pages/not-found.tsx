import {ReactElement} from 'react';
import {useNavigate} from 'react-router-dom';
import ErrorPageComponent from '../components/error-page-component/error-page-component';
import Logo404 from '../images/404-logo.png';

export default function NotFound404(): ReactElement {
  const navigate = useNavigate();

  const onClick = (): void => {
    navigate('/');
  };

  return (
    <ErrorPageComponent
      headerText='Страница не найдена'
      buttonText='Главная'
      logo={Logo404}
      onClick={onClick}
    >
      <p style={{ margin: 0 }}>
        Страница, которую вы запрашиваете, не существует.
      </p>
      <p style={{ margin: 0 }}>
        Возможно, она была удалена, или вы набрали неверный адрес.
      </p>
      <p style={{ margin: 0 }}>
        Всю информацию можно получить на Главной странице
      </p>
    </ErrorPageComponent>
  );
}
