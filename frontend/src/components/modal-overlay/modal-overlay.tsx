import { MouseEvent, ReactElement, useEffect, useState } from 'react';
import './modal-overlay.scss';

type TModalProps = {
  opened: boolean;
  onModalClose: (
    evt: MouseEvent<HTMLButtonElement> | KeyboardEvent | MouseEvent<HTMLElement>
  ) => void;
  children: ReactElement;
};

export default function ModalOverlay({
  opened,
  onModalClose,
  children,
}: TModalProps): ReactElement {
  const [className, setClassName] = useState<string>('overlay');

  const createClassName = () => {
    if (!opened) {
      return 'overlay';
    }
    return 'overlay overlay_opened';
  };

  function closeByEsc(evt: KeyboardEvent) {
    if (evt.key === 'Escape') {
      onModalClose(evt);
    }
  }

  useEffect(() => {
    setClassName(createClassName());
    document.addEventListener('keydown', closeByEsc);
    return () => {
      document.removeEventListener('keydown', closeByEsc);
    };
  }, []);

  const onClose = (evt: MouseEvent<HTMLElement>) => {
    evt.stopPropagation();
    onModalClose(evt);
  };

  function closeFromOutside(evt: MouseEvent<HTMLElement>) {
    const { classList } = evt.target as Element;
    if (classList.contains('overlay')) {
      onClose(evt);
    }
  }

  return (
    <div className={className} onClick={closeFromOutside}>
      {children}
    </div>
  );
}
