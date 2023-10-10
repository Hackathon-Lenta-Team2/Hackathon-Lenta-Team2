import { Link, useLocation } from 'react-router-dom';
import { ReactElement, useEffect, useState } from 'react';
import './add-header.scss';
import headerLogo from '../../images/header-logo.png';
import LogoutModal from '../logout-modal/logout-modal';

export default function AppHeader(): ReactElement {
  const [areLinksHidden, setLinksHidden] = useState(true);
  const [isModalOpened, setModalOpened] = useState(false);

  const location = useLocation();
  useEffect(() => {
    if (location.pathname === '/login') {
      setLinksHidden(true);
    } else {
      setLinksHidden(false);
    }
  }, [location.pathname]);

  function onProfileClick() {
    setModalOpened(true);
  }

  return (
    <header className='header'>
      <div>
        <Link to='/'>
          <img src={headerLogo} alt='Логотип' />
        </Link>
      </div>
      {!areLinksHidden && (
        <>
          <LogoutModal opened={isModalOpened} setModalOpened={setModalOpened}/>
          <div className='header__link-container'>
            <Link to='/' className='header__link'>
              Главная
            </Link>
            <button
              type='button'
              className='header__link'
              onClick={onProfileClick}
            >
              Иванов А. А.
            </button>
          </div>
        </>
      )}
    </header>
  );
}
