import { useEffect, useState } from 'react';
import api from '../api/client';
import DataTable from '../components/DataTable';

const valuationColumns = [
  { accessor: 'id', label: 'ID' },
  { accessor: 'name', label: 'Product' },
  { accessor: 'quantity', label: 'Qty' },
  { accessor: 'unit_price', label: 'Unit Price' },
  { accessor: 'total_value', label: 'Total Value' },
];

const movementColumns = [
  { accessor: 'product_name', label: 'Product' },
  { accessor: 'quantity_before', label: 'Before' },
  { accessor: 'quantity_after', label: 'After' },
  { accessor: 'reason', label: 'Reason' },
  { accessor: 'changed_at', label: 'Date' },
];

export default function Reports() {
  const [valuation, setValuation] = useState([]);
  const [movements, setMovements] = useState([]);
  const [filterProduct, setFilterProduct] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [error, setError] = useState('');

  const fetchValuation = async () => {
    try {
      const res = await api.get('/reports/stock-valuation');
      setValuation(res.data);
    } catch (err) {
      setError('Failed to load stock valuation');
    }
  };

  const fetchMovements = async () => {
    try {
      let url = '/reports/movement-history';
      const params = [];
      if (filterProduct) params.push(`product_id=${filterProduct}`);
      if (startDate) params.push(`start_date=${startDate}`);
      if (endDate) params.push(`end_date=${endDate}`);
      if (params.length) url += '?' + params.join('&');
      const res = await api.get(url);
      setMovements(res.data);
    } catch (err) {
      setError('Failed to load movement history');
    }
  };

  useEffect(() => {
    fetchValuation();
    fetchMovements();
  }, []);

  return (
    <div className="p-6 space-y-8">
      {error && (
        <div className="text-red-400 text-sm p-3 bg-red-900/20 rounded-lg border border-red-800">
          {error}
        </div>
      )}

      <div>
        <h2 className="text-xl font-bold text-gray-100 mb-4">Stock Valuation</h2>
        <DataTable columns={valuationColumns} data={valuation} />
      </div>

      <div>
        <h2 className="text-xl font-bold text-gray-100 mb-4">Movement History</h2>
        <div className="bg-gray-900 p-4 rounded-xl border border-gray-800 mb-4 flex flex-wrap gap-3 items-end">
          <div>
            <label className="block text-gray-400 text-xs mb-1">Product ID</label>
            <input
              type="text"
              placeholder="Filter by product ID"
              value={filterProduct}
              onChange={e => setFilterProduct(e.target.value)}
              className="px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>
          <div>
            <label className="block text-gray-400 text-xs mb-1">Start Date</label>
            <input
              type="date"
              value={startDate}
              onChange={e => setStartDate(e.target.value)}
              className="px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>
          <div>
            <label className="block text-gray-400 text-xs mb-1">End Date</label>
            <input
              type="date"
              value={endDate}
              onChange={e => setEndDate(e.target.value)}
              className="px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>
          <button
            onClick={fetchMovements}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white text-sm transition-colors"
          >
            Apply Filters
          </button>
        </div>
        <DataTable columns={movementColumns} data={movements} />
      </div>
    </div>
  );
}
