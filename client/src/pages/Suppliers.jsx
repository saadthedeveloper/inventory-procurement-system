import { useEffect, useState } from 'react';
import api from '../api/client';
import DataTable from '../components/DataTable';
import FormRenderer from '../components/FormRenderer';
import { useAuth } from '../context/AuthContext';

const supplierSchema = {
  fields: [
    { name: 'name', label: 'Name', type: 'text', required: true },
    { name: 'contact_person', label: 'Contact Person', type: 'text', required: true },
    { name: 'email', label: 'Email', type: 'email', required: true },
    { name: 'phone', label: 'Phone', type: 'text', required: true },
    { name: 'payment_terms', label: 'Payment Terms', type: 'text', required: false },
  ]
};

const columns = [
  { accessor: 'id', label: 'ID' },
  { accessor: 'name', label: 'Name' },
  { accessor: 'contact_person', label: 'Contact' },
  { accessor: 'email', label: 'Email' },
  { accessor: 'phone', label: 'Phone' },
];

export default function Suppliers() {
  const [suppliers, setSuppliers] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [error, setError] = useState('');
  const { user } = useAuth();
  const isAdmin = user?.role_id === 1;

  const fetchData = async () => {
    try {
      const res = await api.get('/suppliers');
      setSuppliers(res.data);
    } catch (err) {
      setError('Failed to load suppliers');
    }
  };

  useEffect(() => { fetchData(); }, []);

  const handleCreate = () => { setEditing(null); setShowForm(true); };
  const handleEdit = (row) => { setEditing(row); setShowForm(true); };
  const handleDelete = async (row) => {
    if (window.confirm(`Delete supplier "${row.name}"?`)) {
      try {
        await api.delete(`/suppliers/${row.id}`);
        fetchData();
      } catch (err) {
        setError('Failed to delete supplier');
      }
    }
  };

  const handleSubmit = async (formData) => {
    try {
      if (editing) {
        await api.put(`/suppliers/${editing.id}`, formData);
      } else {
        await api.post('/suppliers', formData);
      }
      setShowForm(false);
      fetchData();
    } catch (err) {
      setError('Failed to save supplier');
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-gray-100">Suppliers</h1>
        {isAdmin && (
          <button
            onClick={handleCreate}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            + New Supplier
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
        data={suppliers}
        actions={isAdmin}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
      {showForm && (
        <FormRenderer
          schema={supplierSchema}
          initialValues={editing || {}}
          onSubmit={handleSubmit}
          onCancel={() => setShowForm(false)}
          title={editing ? 'Edit Supplier' : 'Create Supplier'}
        />
      )}
    </div>
  );
}
