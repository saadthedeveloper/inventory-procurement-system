import { useEffect, useState } from 'react';
import api from '../api/client';
import DataTable from '../components/DataTable';
import FormRenderer from '../components/FormRenderer';
import { useAuth } from '../context/AuthContext';

const getProductSchema = (categories, units) => ({
  fields: [
    { name: 'name', label: 'Name', type: 'text', required: true },
    { name: 'sku', label: 'SKU', type: 'text', required: false },
    {
      name: 'category_id', label: 'Category', type: 'select', required: true,
      options: categories.map(c => ({ value: c.id, label: c.name }))
    },
    {
      name: 'unit_id', label: 'Unit', type: 'select', required: true,
      options: units.map(u => ({ value: u.id, label: u.name }))
    },
    { name: 'quantity', label: 'Quantity', type: 'number', required: false },
    { name: 'reorder_level', label: 'Reorder Level', type: 'number', required: true },
    { name: 'unit_price', label: 'Unit Price', type: 'number', required: true },
  ]
});

const columns = [
  { accessor: 'id', label: 'ID' },
  { accessor: 'name', label: 'Name' },
  { accessor: 'sku', label: 'SKU' },
  { accessor: 'quantity', label: 'Qty' },
  { accessor: 'unit_price', label: 'Price' },
  { accessor: 'reorder_level', label: 'Reorder' },
];

export default function Products() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [units, setUnits] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [error, setError] = useState('');
  const { user } = useAuth();
  const isAdmin = user?.role_id === 1;

  const fetchData = async () => {
    try {
      const [prodRes, catRes, unitRes] = await Promise.all([
        api.get('/products'),
        api.get('/categories'),
        api.get('/units'),
      ]);
      setProducts(prodRes.data);
      setCategories(catRes.data);
      setUnits(unitRes.data);
    } catch (err) {
      setError('Failed to load products');
    }
  };

  useEffect(() => { fetchData(); }, []);

  const handleCreate = () => { setEditing(null); setShowForm(true); };
  const handleEdit = (row) => { setEditing(row); setShowForm(true); };
  const handleDelete = async (row) => {
    if (window.confirm(`Delete product "${row.name}"?`)) {
      try {
        await api.delete(`/products/${row.id}`);
        fetchData();
      } catch (err) {
        setError('Failed to delete product');
      }
    }
  };

  const handleSubmit = async (formData) => {
    try {
      if (editing) {
        await api.put(`/products/${editing.id}`, formData);
      } else {
        await api.post('/products', formData);
      }
      setShowForm(false);
      fetchData();
    } catch (err) {
      setError('Failed to save product');
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-gray-100">Products</h1>
        {isAdmin && (
          <button
            onClick={handleCreate}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            + New Product
          </button>
        )}
      </div>
      {error && (
        <div className="text-red-400 text-sm mb-4 p-3 bg-red-900/20 rounded-lg border border-red-800">
          {error}
        </div>
      )}
      <DataTable
        columns={columns}
        data={products}
        actions={isAdmin}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
      {showForm && (
        <FormRenderer
          schema={getProductSchema(categories, units)}
          initialValues={editing || {}}
          onSubmit={handleSubmit}
          onCancel={() => setShowForm(false)}
          title={editing ? 'Edit Product' : 'Create Product'}
        />
      )}
    </div>
  );
}
