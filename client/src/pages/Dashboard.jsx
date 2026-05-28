import { useEffect, useState } from 'react';
import api from '../api/client';
import { useAuth } from '../context/AuthContext';
import { Package, Users, ShoppingCart, AlertTriangle } from 'lucide-react';

export default function Dashboard() {
  const [lowStock, setLowStock] = useState([]);
  const [stats, setStats] = useState({ products: 0, suppliers: 0, pendingPOs: 0 });
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [productsRes, suppliersRes, poRes, lowRes] = await Promise.all([
          api.get('/products'),
          api.get('/suppliers'),
          api.get('/purchase-orders'),
          api.get('/products/low-stock'),
        ]);
        setStats({
          products: productsRes.data.length,
          suppliers: suppliersRes.data.length,
          pendingPOs: poRes.data.filter(p => p.status === 'pending').length,
        });
        setLowStock(lowRes.data);
      } catch (err) {
        console.error('Failed to load dashboard data', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="p-6 flex items-center justify-center h-64">
        <div className="text-gray-400">Loading dashboard...</div>
      </div>
    );
  }

  const cards = [
    { label: 'Total Products', value: stats.products, icon: Package, color: 'text-blue-400' },
    { label: 'Total Suppliers', value: stats.suppliers, icon: Users, color: 'text-green-400' },
    { label: 'Pending POs', value: stats.pendingPOs, icon: ShoppingCart, color: 'text-yellow-400' },
  ];

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-100">Dashboard</h1>
        <p className="text-gray-400 text-sm mt-1">Welcome back, {user?.name}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {cards.map(card => (
          <div key={card.label} className="bg-gray-900 rounded-xl p-5 border border-gray-800 shadow flex items-center gap-4">
            <card.icon className={`w-10 h-10 ${card.color}`} />
            <div>
              <div className="text-gray-400 text-sm">{card.label}</div>
              <div className="text-3xl font-bold text-gray-100">{card.value}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-gray-900 rounded-xl border border-gray-800 p-5">
        <div className="flex items-center gap-2 mb-4">
          <AlertTriangle className="w-5 h-5 text-red-400" />
          <h2 className="text-lg font-semibold text-gray-100">Low Stock Alerts</h2>
        </div>
        {lowStock.length === 0 ? (
          <div className="text-gray-500 text-sm py-4 text-center">No low stock items. All good!</div>
        ) : (
          <div className="space-y-2">
            {lowStock.map(item => (
              <div key={item.id} className="flex justify-between items-center border-b border-gray-800 py-3">
                <span className="text-gray-200 font-medium">{item.name}</span>
                <span className="text-red-400 text-sm">
                  Qty: {item.quantity} &lt; Reorder: {item.reorder_level}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
