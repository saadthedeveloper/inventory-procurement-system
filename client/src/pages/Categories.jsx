import { useEffect, useState } from 'react';
import api from '../api/client';
import DataTable from '../components/DataTable';
import FormRenderer from '../components/FormRenderer';
import { useAuth } from '../context/AuthContext';

const categorySchema = {
  fields: [
    { name: 'name', label: 'Name', type: 'text', required: true },
  ]
};

const columns = [
  { accessor: 'id', label: 'ID' },
  { accessor: 'name', label: 'Name' },
];

export default function Categories() {
  const [categories, setCategories] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [error, setError] = useState('');
  const { user } = useAuth();
  const isAdmin = user?.role_id === 1;

  const fetchData = async () => {
    try {
      const res = await api.get('/categories');
      setCategories(res.data);
    } catch (err) {
      setError('Failed to load categories');
    }
  };

  useEffect(() => { fetchData(); }, []);

  const handleCreate = () => { setEditing(null); setShowForm(true); };
  const handleEdit = (row) => { setEditing(row); setShowForm(true); };
  const handleDelete = async (row) => {
    if (window.confirm(`Delete category "${row.name}"?`)) {
      try {
        await api.delete(`/categories/${row.id}`);
        fetchData();
      } catch (err) {
        setError('Failed to delete category');
      }
    }
  };

  const handleSubmit = async (formData) => {
    try {
      if (editing) {
        await api.put(`/categories/${editing.id}`, formData);
      } else {
        await api.post('/categories', formData);
      }
      setShowForm(false);
      fetchData();
    } catch (err) {
      setError('Failed to save category');
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-gray-100">Categories</h1>
        {isAdmin && (
          <button
            onClick={handleCreate}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            + New Category
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
        data={categories}
        actions={isAdmin}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
      {showForm && (
        <FormRenderer
          schema={categorySchema}
          initialValues={editing || {}}
          onSubmit={handleSubmit}
          onCancel={() => setShowForm(false)}
          title={editing ? 'Edit Category' : 'Create Category'}
        />
      )}
    </div>
  );
}
