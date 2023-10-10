import {ChangeEvent, FormEvent, ReactElement, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import Button from '../components/button/button';
import './login.scss';
import '../components/input.scss';
import Checkbox from '../components/checkbox/checkbox';
import {useDispatch} from '../services/hooks/useDispatch';
import {fetchGetUser, fetchLogin} from '../services/async-thunk/auth-thunk';
import {useSelector} from '../services/hooks/useSelector';
import {store} from '../services/store';

interface IFormValue {
  email: string;
  password: string;
}
export default function LoginPage(): ReactElement {
  const [isEmailValid, setEmailValidation] = useState<boolean>(true);
  const [emailError, setEmailError] = useState<string>(' ');
  const [isPasswordValid, setPasswordValidation] = useState<boolean>(true);
  const [passwordError, setPasswordError] = useState<string>(' ');
  const [form, setValue] = useState<IFormValue>({ email: '', password: '' });
  const [isChecked, setChecked] = useState<boolean>(false);

  const loginError = useSelector((state) => state.profile.loginError);

  const isFormInvalid = !isEmailValid || !emailError;

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const setFormValues = (e: ChangeEvent<HTMLInputElement>) => {
    setValue({ ...form, [e.target.name]: e.target.value });
  };

  function onFormChange(
    e: ChangeEvent<HTMLInputElement>,
    setValidation: (newValue: boolean) => void,
    setErrorMessage: (newValue: string) => void
  ) {
    setFormValues(e);
    if (!e.target.validity.valid) {
      setValidation(false);
      setErrorMessage(e.target.validationMessage);
    } else {
      setValidation(true);
      setErrorMessage(' ');
    }
  }

  function onCheckboxChange() {
    setChecked(!isChecked);
  }

  const onSubmit = (e: FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    dispatch(
      fetchLogin({
        email: form.email,
        password: form.password,
        isUserSaved: isChecked,
      })
    ).then(() => {
      const isLoginCorrect = store.getState().profile.loginError;
      if (isLoginCorrect) {
        console.log('Login error');
      } else {
        dispatch(fetchGetUser()).then(() => navigate('/'));
      }
    });
  };

  return (
    <div className='login'>
      <h2 className='login__header'>Войти</h2>
      <form name='loginForm' onSubmit={onSubmit}>
        <div className='input-container'>
          <input
            className={`input ${((!isEmailValid || loginError) && 'input__error') || ''}`}
            type='email'
            name='email'
            required
            minLength={2}
            maxLength={40}
            placeholder='info@lenta.com'
            onChange={(e) => onFormChange(e, setEmailValidation, setEmailError)}
          />
          <label className='label'>Электронная почта</label>
          <span
            className={`message ${(!isEmailValid && 'message__error') || ''}`}
          >
            {emailError}
          </span>
        </div>
        <div className='input-container'>
          <input
            className={`input ${((!isPasswordValid || loginError) && 'input__error') || ''}`}
            type='password'
            name='password'
            required
            minLength={5}
            maxLength={20}
            placeholder='*****'
            onChange={(e) =>
              onFormChange(e, setPasswordValidation, setPasswordError)
            }
          />
          <label className='label'>Пароль</label>
          <span
            className={`message ${
              (!isPasswordValid && 'message__error') || ''
            }`}
          >
            {passwordError}
          </span>
        </div>
        <Checkbox onChange={onCheckboxChange}>Запомнить меня</Checkbox>
        {loginError && (
          <span className='login__error'>Неверный логин или пароль</span>
        )}
        <Button type='submit' disabled={isFormInvalid}>
          Войти
        </Button>
      </form>
    </div>
  );
}
