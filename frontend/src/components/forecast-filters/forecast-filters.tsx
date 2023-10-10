import { ChangeEvent, FormEvent, ReactElement, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { addDays } from 'date-fns';
import Checkbox from '../checkbox/checkbox';
import Button from '../button/button';
import './forecast-filters.scss';
import '../input.scss';
import FilterInputsComponent from '../filter-inputs-component/filter-inputs-component';
import { filterSlice } from '../../services/slices/filter-slice';
import { fetchGetForecasts } from '../../services/async-thunk/filter-thunk';
import { store } from '../../services/store';
import { useDispatch } from '../../services/hooks/useDispatch';
import { useSelector } from '../../services/hooks/useSelector';

export default function ForecastFilters(): ReactElement {
  const [isDaysNumberValid, setDaysNumberValidation] = useState(true);
  const [daysNumberError, setDaysNumberError] = useState('От 1 до 14 дней');
  const [isSubmitClicked, setIsSubmitClicked] = useState(false);
  const [isChecked, setChecked] = useState<boolean>(false);
  const [form, setValue] = useState({ daysNumber: '' });

  const selectedStores = useSelector((state) => state.filter.selectedStores);
  const selectedProducts = useSelector((state) => state.filter.selectedProducts);
  // const startDate = useSelector((state) => state.filter.forecastStartDate);
  // const endDate = useSelector((state) => state.filter.forecastEndDate);

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const isFormValid = !isSubmitClicked ||
    (selectedStores.length > 0 && selectedProducts.length > 0 && isDaysNumberValid);

  const setFormValues = (e: ChangeEvent<HTMLInputElement>) => {
    setValue({ ...form, [e.target.name]: e.target.value });
  };

  function onFormChange(e: ChangeEvent<HTMLInputElement>) {
    setFormValues(e);
    if (!e.target.validity.valid) {
      setDaysNumberValidation(false);
      setDaysNumberError(e.target.validationMessage);
    } else if (Number(e.target.value) > 14) {
      setDaysNumberValidation(false);
      setDaysNumberError('Количество дней не может быть больше 14');
    } else if (Number(e.target.value) < 1) {
      setDaysNumberValidation(false);
      setDaysNumberError('Количество дней не может быть меньше 1');
    } else {
      setDaysNumberValidation(true);
      setDaysNumberError('От 1 до 14 дней');
    }
  }

  function onCheckboxChange() {
    setChecked(!isChecked);
  }

  function handleForecastFiltersSubmit(e: FormEvent<HTMLFormElement>): void {
    e.preventDefault();
    setIsSubmitClicked(true);
    if (isChecked) {
      dispatch(filterSlice.actions.saveToLocalStorage());
      const startDate = new Date('2023-07-18');
      const endDate = addDays(new Date('2023-07-18'), Number(form.daysNumber));
      dispatch(filterSlice.actions.saveForecastDatesToLocalStorage({ startDate, endDate }));
      dispatch(filterSlice.actions.selectForecastStartDate(startDate));
      dispatch(filterSlice.actions.selectForecastEndDate(endDate));
    }
    dispatch(
      fetchGetForecasts({
        stores: selectedStores,
        skus: selectedProducts,
        start_date: new Date('2023-07-18'),
        end_date: addDays(new Date('2023-07-18'), Number(form.daysNumber)),
      })
    ).then(() => {
      const { getForecastsError } = store.getState().filter;
      if (getForecastsError) {
        console.log('Get forecasts error');
      } else {
        navigate('/results/table/forecast');
      }
    });
  }

  return (
    <form
      name='forecast-filters'
      className='form'
      onSubmit={handleForecastFiltersSubmit}
    >
      <FilterInputsComponent isSubmitClicked={isSubmitClicked} />
      <div className='input-container input-container__number-input'>
        <input
          className={`input ${(!isDaysNumberValid && 'input__error') || ''}`}
          type='number'
          name='daysNumber'
          required
          placeholder='10'
          onChange={(e) => onFormChange(e)}
        />
        <label className='label'>Количество дней прогноза</label>
        <span
          className={`message ${
            (!isDaysNumberValid && 'message__error') || ''
          }`}
        >
          {daysNumberError}
        </span>
      </div>
      <Checkbox onChange={onCheckboxChange}>
        Сохранить настройки фильтров
      </Checkbox>
      <Button type='submit' disabled={!isFormValid}>
        Сформировать
      </Button>
    </form>
  );
}
