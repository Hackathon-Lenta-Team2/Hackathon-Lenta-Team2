import { ReactElement, ReactNode } from 'react';
import Button from '../button/button';
import './error-page-component.scss';

interface IErrorPageComponentProps {
  logo: string;
  headerText: string;
  children: string | ReactNode;
  buttonText: string;
  onClick: () => void;
}
export default function ErrorPageComponent({
  logo,
  headerText,
  buttonText,
  children,
  onClick,
}: IErrorPageComponentProps): ReactElement {
  return (
    <section className='error-section'>
      <div className='error-section__text-container'>
        <h1 className='error-section__header'>{headerText}</h1>
        <p className='error-section__text'>{children}</p>
        <Button type='button' onClick={onClick}>
          {buttonText}
        </Button>
      </div>
      <img src={logo} alt='Лого' />
    </section>
  );
}
