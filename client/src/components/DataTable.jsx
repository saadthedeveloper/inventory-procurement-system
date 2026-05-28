import { useState } from 'react';

export default function DataTable({ columns, data, actions, onEdit, onDelete, onView }) {
  const [search, setSearch] = useState('');

  const filtered = data.filter(row =>
    columns.some(col =>
      String(row[col.accessor] || '').toLowerCase().includes(search.toLowerCase())
    )
  );

  return (
    <div className="bg-gray-900 rounded-xl border border-gray-800 overflow-hidden">
      <div className="p-4 border-b border-gray-800">
        <input
          type="text"
          placeholder="Search..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="w-full max-w-sm px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-600"
        />
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead className="bg-gray-800 text-gray-300">
            <tr>
              {columns.map(col => (
                <th key={col.accessor} className="px-4 py-3 font-semibold text-sm">{col.label}</th>
              ))}
              {actions && <th className="px-4 py-3 font-semibold text-sm">Actions</th>}
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={columns.length + (actions ? 1 : 0)} className="px-4 py-8 text-center text-gray-500">
                  No records found
                </td>
              </tr>
            ) : (
              filtered.map((row, idx) => (
                <tr key={idx} className="border-t border-gray-800 hover:bg-gray-800/50 transition-colors">
                  {columns.map(col => (
                    <td key={col.accessor} className="px-4 py-3 text-gray-200 text-sm">{row[col.accessor]}</td>
                  ))}
                  {actions && (
                    <td className="px-4 py-3 space-x-3">
                      {onView && (
                        <button onClick={() => onView(row)} className="text-blue-400 hover:text-blue-300 text-sm font-medium">View</button>
                      )}
                      {onEdit && (
                        <button onClick={() => onEdit(row)} className="text-yellow-400 hover:text-yellow-300 text-sm font-medium">Edit</button>
                      )}
                      {onDelete && (
                        <button onClick={() => onDelete(row)} className="text-red-400 hover:text-red-300 text-sm font-medium">Delete</button>
                      )}
                    </td>
                  )}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
