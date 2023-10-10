import { MouseEvent, ReactElement } from 'react';
import ReactDOM from 'react-dom';
import { useNavigate } from 'react-router-dom';
import ModalOverlay from '../modal-overlay/modal-overlay';
import './logout-modal.scss';
import CloseIcon from '../../images/multi-val-delete-icon.svg';
import Button from '../button/button';
import { useDispatch } from '../../services/hooks/useDispatch';
import { fetchLogout } from '../../services/async-thunk/auth-thunk';

type TModalProps = {
  opened: boolean;
  setModalOpened: (state: boolean) => void;
};

const modalRoot: HTMLElement | null = document.getElementById('modal-root');

export default function LogoutModal({
  opened,
  setModalOpened,
}: TModalProps): ReactElement | null {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const onClose = (evt: MouseEvent<HTMLButtonElement, globalThis.MouseEvent> | KeyboardEvent | MouseEvent<HTMLElement, globalThis.MouseEvent>) => {
    evt.stopPropagation();
    setModalOpened(false);
  };

  function onLogoutClick() {
    dispatch(fetchLogout()).then(() => navigate('/login'));
  }

  if (!opened) return null;
  if (modalRoot === null) return null;

  return ReactDOM.createPortal(
    <ModalOverlay opened={opened} onModalClose={onClose}>
      <div className='popup'>
        <div className='popup__text-container'>
          <p className='popup__text'>Сменить пользователя?</p>
          <button
            className='popup__close-button'
            onClick={onClose}
            type='button'
          >
            <img src={CloseIcon} alt='Закрыть' />
          </button>
        </div>
        <Button type='button' onClick={onLogoutClick}>
          Выйти
        </Button>
      </div>
    </ModalOverlay>,
    modalRoot
  );
}
