import { Navigate } from 'react-router-dom';
import { ReactElement } from 'react';
import { useSelector } from '../../services/hooks/useSelector';
import { isUserAuthorized } from '../../utils/helpers';

type TProtectedRouteProps = {
  element: ReactElement;
};

export default function ProtectedRoute({
  element,
}: TProtectedRouteProps): ReactElement {
  const user = useSelector((store) => store.profile.user);

  return isUserAuthorized(user) ? element : <Navigate to='/login' />;
}
