import React, { useState, useEffect } from 'react';
import api from '../services/api';
import type { FamilyTransferRequest } from '../types';
import { Clock, CheckCircle, XCircle } from 'lucide-react';

const CitizenFamilyTransfers = () => {
  const [transfers, setTransfers] = useState<FamilyTransferRequest[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTransfers = async () => {
      try {
        const res = await api.get('/api/family-transfers');
        setTransfers(res.data);
      } catch (err) {
        console.error("Failed to fetch family transfers");
      } finally {
        setLoading(false);
      }
    };
    fetchTransfers();
  }, []);

  if (loading) return <div className="flex items-center justify-center p-12"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div></div>;

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Family Transfer Requests</h2>
      <p className="text-gray-600 mb-6">
        Track your requests to move to a different family profile due to marriage, adoption, or relocation.
      </p>
      
      <div className="bg-white shadow-sm rounded-lg border overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="p-4 font-medium text-gray-600">Reason</th>
              <th className="p-4 font-medium text-gray-600">Spouse Aadhaar</th>
              <th className="p-4 font-medium text-gray-600">Status</th>
              <th className="p-4 font-medium text-gray-600">Submitted On</th>
            </tr>
          </thead>
          <tbody>
            {transfers.map(t => (
              <tr key={t.id} className="border-b last:border-b-0 hover:bg-gray-50">
                <td className="p-4 font-medium text-gray-800 capitalize">
                  {t.reason}
                </td>
                <td className="p-4 text-gray-600 font-mono text-sm">
                  {t.spouse_aadhaar ? `XXXX-XXXX-${t.spouse_aadhaar.slice(-4)}` : '—'}
                </td>
                <td className="p-4">
                  <div className={`inline-flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-semibold
                    ${t.status === 'APPROVED' || t.status === 'COMPLETED' ? 'bg-green-100 text-green-800' : 
                      t.status === 'REJECTED' ? 'bg-red-100 text-red-800' : 
                      'bg-yellow-100 text-yellow-800'}`}>
                    {t.status === 'PENDING' || t.status === 'MANUAL_REVIEW' ? <Clock size={12} /> : 
                     t.status === 'REJECTED' ? <XCircle size={12} /> : <CheckCircle size={12} />}
                    <span>{t.status.replace('_', ' ')}</span>
                  </div>
                  {t.remarks && <p className="text-xs text-gray-500 mt-1 max-w-xs">{t.remarks}</p>}
                </td>
                <td className="p-4 text-gray-600 text-sm">{new Date(t.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
            {transfers.length === 0 && (
              <tr><td colSpan={4} className="p-8 text-center text-gray-500">No transfer requests found.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CitizenFamilyTransfers;
