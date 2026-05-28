import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user } = useAuth();
  return (
    <header className="bg-gray-900 border-b border-gray-800 py-3 px-6 flex justify-between items-center">
      <div className="text-gray-100">Welcome, {user?.name}</div>
      <div className="text-gray-400 text-sm">Inventory System</div>
    </header>
  );
}
