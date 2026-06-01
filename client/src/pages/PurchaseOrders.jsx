import { useEffect, useState } from 'react';
import api from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function PurchaseOrders() {
  const [orders, setOrders] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [products, setProducts] = useState([]);
  const [showCreate, setShowCreate] = useState(false);
  const [newOrder, setNewOrder] = useState({ supplier_id: '', items: [], notes: '' });
  const [error, setError] = useState('');
  const [orderItems, setOrderItems] = useState({}); // { orderId: [items] }
  const { user } = useAuth();
  const isAdmin = user?.role_id === 1;
  const isManager = user?.role_id === 2;
  const canCreate = isAdmin || isManager;

  const fetchData = async () => {
    try {
      const [ordersRes, supRes, prodRes] = await Promise.all([
        api.get('/purchase-orders/'),
        api.get('/suppliers'),
        api.get('/products'),
      ]);
      setOrders(ordersRes.data);
      setSuppliers(supRes.data);
      setProducts(prodRes.data);
    } catch (err) {
      setError('Failed to load purchase orders');
    }
  };

  useEffect(() => { fetchData(); }, []);

  const loadOrderItems = async (orderId) => {
    if (orderItems[orderId]) {
      // Already loaded, remove to hide
      setOrderItems(prev => {
        const newState = { ...prev };
        delete newState[orderId];
        return newState;
      });
      return;
    }
    try {
      const res = await api.get(`/purchase-orders/${orderId}`);
      setOrderItems(prev => ({ ...prev, [orderId]: res.data.items || [] }));
    } catch (err) {
      setError('Failed to load order items');
    }
  };

  const handleApprove = async (orderId) => {
    try {
      await api.put(`/purchase-orders/${orderId}/approve`);
      fetchData();
    } catch (err) {
      setError('Failed to approve order');
    }
  };

  const handleCancel = async (orderId) => {
    try {
      await api.put(`/purchase-orders/${orderId}/cancel`);
      fetchData();
    } catch (err) {
      setError('Failed to cancel order');
    }
  };

  const handleReceive = async (orderId) => {
    try {
      // Fetch full order details including items
      const orderRes = await api.get(`/purchase-orders/${orderId}`);
      const order = orderRes.data;
      const items = (order.items || []).map(i => ({
        product_id: i.product_id,
        quantity_received: i.quantity_ordered,
      }));
      await api.put(`/purchase-orders/${orderId}/receive`, { items });
      fetchData();
    } catch (err) {
      setError('Failed to receive order');
    }
  };

  const addItem = () => {
    setNewOrder({
      ...newOrder,
      items: [...newOrder.items, { product_id: '', quantity_ordered: 1, unit_cost: 0 }],
    });
  };

  const updateItem = (idx, field, value) => {
    const items = [...newOrder.items];
    items[idx][field] = value;
    setNewOrder({ ...newOrder, items });
  };

  const removeItem = (idx) => {
    const items = newOrder.items.filter((_, i) => i !== idx);
    setNewOrder({ ...newOrder, items });
  };

  const submitOrder = async () => {
    try {
      await api.post('/purchase-orders', newOrder);
      setShowCreate(false);
      setNewOrder({ supplier_id: '', items: [], notes: '' });
      fetchData();
    } catch (err) {
      setError('Failed to create purchase order');
    }
  };

  const statusColor = (status) => {
    if (status === 'pending') return 'text-yellow-400';
    if (status === 'approved') return 'text-green-400';
    if (status === 'received') return 'text-blue-400';
    return 'text-gray-400';
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-gray-100">Purchase Orders</h1>
        {canCreate && (
          <button
            onClick={() => setShowCreate(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            + Create PO
          </button>
        )}
      </div>

      {error && (
        <div className="text-red-400 text-sm mb-4 p-3 bg-red-900/20 rounded-lg border border-red-800">
          {error}
        </div>
      )}

      {orders.length === 0 ? (
        <div className="bg-gray-900 rounded-xl border border-gray-800 p-8 text-center text-gray-500">
          No purchase orders found
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map(order => (
            <div key={order.id} className="bg-gray-900 rounded-xl border border-gray-800 p-4">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <span className="text-gray-500 text-xs">PO #{order.id}</span>
                  <div className="text-gray-200 font-medium">Supplier: {order.supplier_name}</div>
                  <div className="text-white">
                    Status:{' '}
                    <span className={`font-semibold ${statusColor(order.status)}`}>
                      {order.status}
                    </span>
                  </div>
                  {order.notes && (
                    <div className="text-gray-500 text-xs mt-1">Notes: {order.notes}</div>
                  )}
                </div>
                <div className="flex gap-2 flex-shrink-0">
                  {isAdmin && order.status === 'pending' && (
                    <button
                      onClick={() => handleApprove(order.id)}
                      className="px-3 py-1.5 bg-green-700 hover:bg-green-600 rounded-lg text-white text-sm transition-colors"
                    >
                      Approve
                    </button>
                  )}
                  {order.status === 'approved' && (
                    <button
                      onClick={() => handleReceive(order.id)}
                      className="px-3 py-1.5 bg-blue-700 hover:bg-blue-600 rounded-lg text-white text-sm transition-colors"
                    >
                      Mark Received
                    </button>
                  )}
                  {order.status === 'pending' && (isAdmin || order.created_by === user?.id) && (
                    <button
                      onClick={() => handleCancel(order.id)}
                      className="px-3 py-1.5 bg-red-700 hover:bg-red-600 rounded-lg text-white text-sm transition-colors"
                    >
                      Cancel
                    </button>
                  )}
                </div>
              </div>

              {/* Show/Hide Items Button */}
              <button
                onClick={() => loadOrderItems(order.id)}
                className="text-xs text-gray-400 hover:text-gray-300 mt-2 focus:outline-none"
              >
                {orderItems[order.id] ? 'Hide Items' : 'Show Items'}
              </button>

              {/* Items List */}
              {orderItems[order.id] && (
                <div className="mt-2 border-t border-gray-800 pt-2">
                  <div className="text-xs text-gray-400 mb-1">Ordered Items:</div>
                  {orderItems[order.id].map((item, idx) => (
                    <div key={idx} className="text-xs text-gray-300 flex justify-between">
                      <span>{item.product_name} (ID: {item.product_id})</span>
                      <span>
                        Ordered: {item.quantity_ordered} | Received: {item.quantity_received || 0}
                      </span>
                    </div>
                  ))}
                </div>
              )}

              <div className="text-xs text-gray-500 mt-2">
                Created: {new Date(order.created_at).toLocaleString()}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create PO Modal */}
      {showCreate && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-gray-900 rounded-xl shadow-2xl w-full max-w-2xl border border-gray-700">
            <div className="p-4 border-b border-gray-800">
              <h3 className="text-xl font-bold text-gray-100">Create Purchase Order</h3>
            </div>
            <div className="p-4 space-y-4 max-h-[70vh] overflow-y-auto">
              <div>
                <label className="block text-gray-300 mb-1 text-sm font-medium">Supplier</label>
                <select
                  value={newOrder.supplier_id}
                  onChange={e => setNewOrder({ ...newOrder, supplier_id: e.target.value })}
                  className="w-full p-2 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-600"
                >
                  <option value="">Select supplier</option>
                  {suppliers.map(s => (
                    <option key={s.id} value={s.id}>{s.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-gray-300 mb-1 text-sm font-medium">Notes</label>
                <textarea
                  value={newOrder.notes}
                  onChange={e => setNewOrder({ ...newOrder, notes: e.target.value })}
                  rows={2}
                  className="w-full p-2 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-600"
                />
              </div>
              <div>
                <label className="block text-gray-300 mb-2 text-sm font-medium">Items</label>
                {newOrder.items.map((item, idx) => (
                  <div key={idx} className="flex gap-2 mb-2">
                    <select
                      value={item.product_id}
                      onChange={e => updateItem(idx, 'product_id', e.target.value)}
                      className="flex-1 p-2 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 text-sm"
                    >
                      <option value="">Product</option>
                      {products.map(p => (
                        <option key={p.id} value={p.id}>{p.name}</option>
                      ))}
                    </select>
                    <input
                      type="number"
                      placeholder="Qty"
                      value={item.quantity_ordered}
                      onChange={e => updateItem(idx, 'quantity_ordered', e.target.value)}
                      className="w-20 p-2 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 text-sm"
                    />
                    <input
                      type="number"
                      step="0.01"
                      placeholder="Cost"
                      value={item.unit_cost}
                      onChange={e => updateItem(idx, 'unit_cost', e.target.value)}
                      className="w-28 p-2 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 text-sm"
                    />
                    <button
                      onClick={() => removeItem(idx)}
                      className="px-3 py-1 bg-red-800 hover:bg-red-700 rounded-lg text-white text-sm"
                    >
                      ✕
                    </button>
                  </div>
                ))}
                <button
                  type="button"
                  onClick={addItem}
                  className="text-blue-400 hover:text-blue-300 text-sm mt-1"
                >
                  + Add item
                </button>
              </div>
            </div>
            <div className="flex justify-end gap-3 p-4 border-t border-gray-800">
              <button
                onClick={() => setShowCreate(false)}
                className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-gray-200 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={submitOrder}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white transition-colors"
              >
                Submit Order
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}