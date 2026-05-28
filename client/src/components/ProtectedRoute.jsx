import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children, allowedRoles = [] }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="p-4 text-center text-gray-300">Loading...</div>;
  if (!user) return <Navigate to="/login" />;
  if (allowedRoles.length && !allowedRoles.includes(user.role_id)) {
    return <div className="p-4 text-red-500">Access denied</div>;
  }
  return children;
}
