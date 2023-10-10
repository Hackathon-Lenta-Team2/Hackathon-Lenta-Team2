import { ReactElement } from 'react';
import './checkbox.scss';
import { useLocation } from 'react-router-dom';

interface ICheckboxProps {
  children: string;
  onChange: () => void;
}
export default function Checkbox({ children, onChange }: ICheckboxProps): ReactElement {
  let className = 'checkbox ';
  const { pathname } = useLocation();
  if (pathname === '/') {
    className += 'checkbox_on-filter-page';
  }
  return (
    <label className={className}>
      {children}
      <input
        className='checkbox_real'
        type='checkbox'
        name='loginSave'
        onChange={onChange}
      />
      <span className='checkbox_fake' />
    </label>
  );
}
