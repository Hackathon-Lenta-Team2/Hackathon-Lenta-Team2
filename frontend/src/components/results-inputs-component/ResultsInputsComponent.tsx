/* eslint-disable react/jsx-no-bind */
/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-shadow */
import { ReactElement } from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import FilterInput from '../filter-input/filter-input';
import '../input.scss';
import { useSelector } from '../../services/hooks/useSelector';
import { useDispatch } from '../../services/hooks/useDispatch';
import { filterSlice } from '../../services/slices/filter-slice';

export default function ResultsInputsComponent({
  isSubmitClicked,
}: {
  isSubmitClicked: boolean;
}): ReactElement {
  const stores = useSelector((store) => store.filter.stores);
  const groups = useSelector((store) => store.filter.groups);
  const categories = useSelector((store) => store.filter.categories);
  const subcategories = useSelector((store) => store.filter.subcategories);
  const products = useSelector((store) => store.filter.products);

  const selectedStores = useSelector((store) => store.filter.selectedStores);
  const selectedGroups = useSelector((store) => store.filter.selectedGroups);
  const selectedCategories = useSelector(
    (store) => store.filter.selectedCategories
  );
  const selectedSubcategories = useSelector(
    (store) => store.filter.selectedSubcategories
  );
  const selectedProducts = useSelector(
    (store) => store.filter.selectedProducts
  );

  const dispatch = useDispatch();

  function handleStoreFilterOption(candidate: any, input: any) {
    return (
      candidate.data.id.includes(input) ||
      candidate.data.city.includes(input) ||
      candidate.data.division.includes(input)
    );
  }

  const dispatchStores = (selectedStores: Array<string>) =>
    dispatch(filterSlice.actions.selectStores(selectedStores));
  const dispatchGroups = (selectedGroups: Array<string>) =>
    dispatch(filterSlice.actions.selectGroups(selectedGroups));

  function handleCategoryFilterOption(candidate: any, input: any) {
    return (
      candidate.data.id.includes(input) &&
      ((selectedGroups.length === 0 && true) ||
        selectedGroups.includes(candidate.data.group_id))
    );
  }
  const dispatchCategories = (selectedCategories: Array<string>) =>
    dispatch(filterSlice.actions.selectCategories(selectedCategories));

  function handleSubcategoryFilterOption(candidate: any, input: any) {
    return (
      candidate.data.id.includes(input) &&
      ((selectedCategories.length === 0 && true) ||
        selectedCategories.includes(candidate.data.category_id))
    );
  }
  const dispatchSubcategories = (selectedSubcategories: Array<string>) =>
    dispatch(filterSlice.actions.selectSubcategories(selectedSubcategories));

  function handleProductFilterOption(candidate: any, input: any) {
    return (
      candidate.data.id.includes(input) &&
      ((selectedSubcategories.length === 0 && true) ||
        selectedSubcategories.includes(candidate.data.subcat_id)) &&
      ((selectedCategories.length === 0 && true) ||
        selectedCategories.includes(candidate.data.cat_id)) &&
      ((selectedGroups.length === 0 && true) ||
        selectedGroups.includes(candidate.data.group_id))
    );
  }
  const dispatchProducts = (selectedProducts: Array<string>) =>
    dispatch(filterSlice.actions.selectProducts(selectedProducts));

  if (stores.length === 0 || groups.length === 0) {
    return <p className=''>Загрузка...</p>;
  }

  return (
    <>
      <FilterInput
        isRequired
        isSubmitClicked={isSubmitClicked}
        data={stores}
        selectedOptions={selectedStores}
        dispatchSelectedOption={dispatchStores}
        filterOptionFunction={handleStoreFilterOption}
      >
        Номер ТК
      </FilterInput>
      <FilterInput
        data={groups}
        selectedOptions={selectedGroups}
        dispatchSelectedOption={dispatchGroups}
      >
        Группа товаров
      </FilterInput>
      <FilterInput
        data={categories}
        selectedOptions={selectedCategories}
        dispatchSelectedOption={dispatchCategories}
        filterOptionFunction={handleCategoryFilterOption}
      >
        Категория
      </FilterInput>
      <FilterInput
        data={subcategories}
        selectedOptions={selectedSubcategories}
        dispatchSelectedOption={dispatchSubcategories}
        filterOptionFunction={handleSubcategoryFilterOption}
      >
        Подкатегория
      </FilterInput>
      <FilterInput
        isRequired
        isSubmitClicked={isSubmitClicked}
        data={products}
        selectedOptions={selectedProducts}
        dispatchSelectedOption={dispatchProducts}
        filterOptionFunction={handleProductFilterOption}
      >
        Товар
      </FilterInput>
    </>
  );
}
