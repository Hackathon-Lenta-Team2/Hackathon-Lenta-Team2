import { ReactElement } from 'react';
import '../checkbox/checkbox.scss';
import makeAnimated from 'react-select/animated';
import { components, default as ReactSelect } from 'react-select';
import searchIcon from '../../images/search-icon.svg';
import downIcon from '../../images/indicator-icon-down.svg';
import upIcon from '../../images/indicator-icon-up.svg';
import deleteIcon from '../../images/multi-val-delete-icon.svg';
import '../input.scss';

type TStyles = {
  [name: string]: string;
};

type TItem = {
  id: string;
};

type TProps = any;
const filterStyles: any = {
  control: (styles: TStyles) => ({
    ...styles,
    backgroundColor: '#F0FBFF',
    border: 0,
    borderRadius: 0,
    padding: '0 16px 0 8px',
    height: '56px',
    boxShadow: 'none',
    borderBottom: '1px solid #003C96',
  }),

  placeholder: (styles: TStyles) => ({
    ...styles,
    color: '#003C96',
    fontSize: '20px',
  }),

  indicatorSeparator: (styles: TStyles) => ({
    ...styles,
    backgroundColor: 0,
    width: '4px',
  }),

  menu: (styles: TStyles) => ({
    ...styles,
    margin: 0,
    border: 0,
    backgroundColor: '#F0FBFF',
    boxShadow: 0,
  }),

  menuList: (styles: TStyles) => ({
    ...styles,
    margin: 0,
    border: 0,
    backgroundColor: '#F0FBFF',
    maxHeight: '280px',
  }),

  option: (styles: TStyles) => ({
    ...styles,
    backgroundColor: '#F0FBFF',
    color: 'black',
    ':active': {
      backgroundColor: 'transparent',
    },
  }),

  multiValue: (styles: TStyles) => ({
    ...styles,
    backgroundColor: 'white',
    borderRadius: 0,
    boxShadow: '0 0 10px #173C9126',
    maxWidth: '140px',
  }),

  multiValueRemove: (styles: TStyles) => ({
    ...styles,
    borderRadius: 0,
    padding: '0 6px',
    ':hover': {
      backgroundColor: 'rgba(0, 60, 150, 0.2)',
    },
  }),

  input: (styles: TStyles) => ({
    ...styles,
    fontSize: '20px',
    cursor: 'pointer',
  }),
};

function Placeholder(props: TProps) {
  const { selectProps } = props;
  const { menuIsOpen } = selectProps;
  return (
    <components.Placeholder {...props}>
      <div className='placeholder'>
        <img src={searchIcon} alt='Поиск' width='18px' height='18px' />
        {!menuIsOpen && <span>084a8a9aa8cced9175bd07bc44998e75</span>}
      </div>
    </components.Placeholder>
  );
}

function MySelect(props: TProps) {
  return (
    <ReactSelect
      {...props}
      options={[...props.options]}
      onChange={(selected) => props.onChange(selected)}
      styles={props.styles}
      {...{
        filterOption: props.filterOptionFunction,
      }}
      getOptionValue={(option: TItem) => option.id}
    />
  );
}

function Option(props: TProps) {
  return (
    <div>
      <components.Option {...props}>
        <div className='option-container'>
          <label className='checkbox-filter'>
            <input
              className='checkbox_real'
              type='checkbox'
              name='loginSave'
              checked={props.isSelected}
              onChange={() => null}
            />
            <span className='checkbox_fake' />
            <label>{props.data.id}</label>
          </label>
        </div>
      </components.Option>
    </div>
  );
}

function MultiValueRemove(props: TProps) {
  return (
    <components.MultiValueRemove {...props}>
      <img
        src={deleteIcon}
        alt='Удалить'
        width='10px'
        height='10px'
        className='icon'
      />
    </components.MultiValueRemove>
  );
}

function ClearIndicator(props: TProps) {
  return (
    <components.ClearIndicator {...props}>
      <img
        src={deleteIcon}
        alt='Удалить все'
        width='14px'
        height='14px'
        className='icon'
      />
    </components.ClearIndicator>
  );
}

function DropdownIndicator(props: TProps) {
  const { selectProps } = props;
  const { menuIsOpen } = selectProps;
  return menuIsOpen ? (
    <components.DropdownIndicator {...props}>
      <img src={upIcon} alt='Раскрыть' className='icon' />
    </components.DropdownIndicator>
  ) : (
    <components.DropdownIndicator {...props}>
      <img src={downIcon} alt='Скрыть' className='icon' />
    </components.DropdownIndicator>
  );
}

function MultiValue(props: TProps) {
  return (
    <components.MultiValue {...props}>
      <span>{props.data.id}</span>
    </components.MultiValue>
  );
}

const animatedComponents = makeAnimated();

type TFilterInputProps = {
  children: string;
  data: Array<any>;
  selectedOptions: Array<string>;
  filterOptionFunction?: (candidate: any, input: any) => void;
  dispatchSelectedOption?: any;
  isRequired?: boolean;
  isSubmitClicked?: boolean;
};
export default function FilterInput({
  children,
  isRequired,
  data,
  selectedOptions,
  filterOptionFunction,
  dispatchSelectedOption,
  isSubmitClicked,
}: TFilterInputProps): ReactElement {
  function handleChange(selected: Array<TItem>) {
    dispatchSelectedOption(selected.map((item) => item.id));
  }

  const styles = { ...filterStyles };
  if (isSubmitClicked && isRequired && selectedOptions.length === 0) {
    styles.control = (styles: TStyles) => ({
      ...styles,
      backgroundColor: '#F0FBFF',
      border: 0,
      borderRadius: 0,
      padding: '0 16px 0 8px',
      height: '56px',
      boxShadow: 'none',
      borderBottom: '1px solid #B9002B',
    });
  }
  return (
    <div className='filter-container'>
      <span className='label'>{children}</span>
      <MySelect
        styles={styles}
        options={data}
        isMulti
        closeMenuOnSelect={false}
        hideSelectedOptions={false}
        components={{
          Option,
          MultiValue,
          MultiValueRemove,
          DropdownIndicator,
          ClearIndicator,
          Placeholder,
          animatedComponents,
        }}
        onChange={handleChange}
        value={data.filter((item) => (selectedOptions || []).includes(item.id))}
        filterOptionFunction={filterOptionFunction}
      />
    </div>
  );
}
