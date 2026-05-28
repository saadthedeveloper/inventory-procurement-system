import { useState } from 'react';

export default function FormRenderer({ schema, initialValues, onSubmit, onCancel, title }) {
  const [form, setForm] = useState(initialValues || {});
  const [errors, setErrors] = useState({});

  const handleChange = (field, value) => {
    setForm({ ...form, [field]: value });
    if (errors[field]) setErrors({ ...errors, [field]: null });
  };

  const validate = () => {
    const newErrors = {};
    schema.fields.forEach(field => {
      if (field.required && !form[field.name]) {
        newErrors[field.name] = `${field.label} is required`;
      }
    });
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) onSubmit(form);
  };

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
      <div className="bg-gray-900 rounded-xl shadow-2xl w-full max-w-md border border-gray-700">
        <div className="p-4 border-b border-gray-800">
          <h3 className="text-xl font-bold text-gray-100">{title}</h3>
        </div>
        <form onSubmit={handleSubmit} className="p-4 space-y-4 max-h-[70vh] overflow-y-auto">
          {schema.fields.map(field => (
            <div key={field.name}>
              <label className="block text-gray-300 mb-1 text-sm font-medium">{field.label}</label>
              {field.type === 'select' ? (
                <select
                  value={form[field.name] || ''}
                  onChange={e => handleChange(field.name, e.target.value)}
                  className="w-full px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-600"
                >
                  <option value="">Select...</option>
                  {field.options.map(opt => (
                    <option key={opt.value} value={opt.value}>{opt.label}</option>
                  ))}
                </select>
              ) : field.type === 'textarea' ? (
                <textarea
                  value={form[field.name] || ''}
                  onChange={e => handleChange(field.name, e.target.value)}
                  rows={3}
                  className="w-full px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-600"
                />
              ) : (
                <input
                  type={field.type || 'text'}
                  value={form[field.name] || ''}
                  onChange={e => handleChange(field.name, e.target.value)}
                  className="w-full px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-600"
                />
              )}
              {errors[field.name] && (
                <p className="text-red-500 text-sm mt-1">{errors[field.name]}</p>
              )}
            </div>
          ))}
          <div className="flex justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 rounded-lg bg-gray-700 hover:bg-gray-600 text-gray-200 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white transition-colors"
            >
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
