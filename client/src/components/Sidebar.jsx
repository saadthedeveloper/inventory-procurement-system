import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard, Package, Users, Layers, ShoppingCart,
  FileText, LogOut
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const navItems = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, roles: [1, 2, 3] },
  { to: '/products', label: 'Products', icon: Package, roles: [1, 2, 3] },
  { to: '/suppliers', label: 'Suppliers', icon: Users, roles: [1, 2, 3] },
  { to: '/categories', label: 'Categories', icon: Layers, roles: [1, 2, 3] },
  { to: '/purchase-orders', label: 'Purchase Orders', icon: ShoppingCart, roles: [1, 2, 3] },
  { to: '/reports', label: 'Reports', icon: FileText, roles: [1, 2, 3] },
];

export default function Sidebar() {
  const { user, logout } = useAuth();
  const roleId = user?.role_id;

  const filtered = navItems.filter(item => item.roles.includes(roleId));

  const roleName =
    user?.role_id === 1 ? 'Admin' :
    user?.role_id === 2 ? 'Manager' : 'Staff';

  return (
    <div className="w-64 bg-gray-900 text-gray-100 flex flex-col h-screen fixed left-0 top-0 shadow-xl">
      <div className="p-4 border-b border-gray-800">
        <h1 className="text-xl font-bold">Inventory Pro</h1>
        <p className="text-xs text-gray-400 mt-1">Role: {roleName}</p>
      </div>
      <nav className="flex-1 p-3 space-y-1">
        {filtered.map(item => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                isActive ? 'bg-gray-800 text-white' : 'text-gray-300 hover:bg-gray-800'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="p-3 border-t border-gray-800">
        <button
          onClick={logout}
          className="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-gray-300 hover:bg-gray-800 transition-colors"
        >
          <LogOut className="w-5 h-5" />
          <span>Logout</span>
        </button>
      </div>
    </div>
  );
}
