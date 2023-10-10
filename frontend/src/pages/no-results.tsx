import {ReactElement} from 'react';
import {useNavigate} from 'react-router-dom';
import ErrorPageComponent from '../components/error-page-component/error-page-component';
import Logo from '../images/logo.png';

export default function NoResults(): ReactElement {
  const navigate = useNavigate();

  const onClick = (): void => {
    navigate('/');
  };

  return (
    <ErrorPageComponent
      headerText='Данные не найдены'
      buttonText='Назад'
      logo={Logo}
      onClick={onClick}
    >
      По установленным фильтрам не нашлось результатов, нужно изменить критерии
      поиска
    </ErrorPageComponent>
  );
}
