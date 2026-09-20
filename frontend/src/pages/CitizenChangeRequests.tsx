import React, { useState, useEffect } from 'react';
import api from '../services/api';
import type { ChangeRequest } from '../types';
import { Clock, CheckCircle, XCircle } from 'lucide-react';

const CitizenChangeRequests = () => {
  const [requests, setRequests] = useState<ChangeRequest[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRequests = async () => {
      try {
        const res = await api.get('/api/change-requests');
        setRequests(res.data);
      } catch (err) {
        console.error("Failed to fetch change requests");
      } finally {
        setLoading(false);
      }
    };
    fetchRequests();
  }, []);

  if (loading) return <div className="flex items-center justify-center p-12"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div></div>;

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">My Change Requests</h2>
      <p className="text-gray-600 mb-6">
        Track the status of your requests to update government-verified information. Verified fields cannot be changed directly and require approval.
      </p>
      
      <div className="bg-white shadow-sm rounded-lg border overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="p-4 font-medium text-gray-600">Field</th>
              <th className="p-4 font-medium text-gray-600">Requested Change</th>
              <th className="p-4 font-medium text-gray-600">Status</th>
              <th className="p-4 font-medium text-gray-600">Submitted On</th>
            </tr>
          </thead>
          <tbody>
            {requests.map(req => (
              <tr key={req.id} className="border-b last:border-b-0 hover:bg-gray-50">
                <td className="p-4 font-medium text-gray-800 capitalize">
                  {req.field_name === 'ADD_MEMBER' ? 'Add Member' : 
                   req.field_name === 'REMOVE_MEMBER' ? 'Remove Member' : 
                   req.field_name.replace('_', ' ')}
                </td>
                <td className="p-4">
                  {req.field_name === 'ADD_MEMBER' ? (
                    <div className="text-sm">
                      <span className="text-green-600 font-medium block">
                        {(() => {
                          try {
                            const data = JSON.parse(req.requested_value);
                            return `${data.name} (${data.relationship})`;
                          } catch (e) {
                            return req.requested_value;
                          }
                        })()}
                      </span>
                    </div>
                  ) : req.field_name === 'REMOVE_MEMBER' ? (
                    <div className="text-sm">
                      <span className="text-red-500 line-through mr-2 font-medium">{req.old_value || '—'}</span>
                    </div>
                  ) : (
                    <div className="text-sm">
                      <span className="text-red-500 line-through mr-2">{req.old_value || '—'}</span>
                      <span className="text-green-600 font-medium">{req.requested_value}</span>
                    </div>
                  )}
                  {req.reason && <p className="text-xs text-gray-500 mt-1">Reason: {req.reason}</p>}
                </td>
                <td className="p-4">
                  <div className={`inline-flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-semibold
                    ${req.verification_status === 'APPROVED' || req.verification_status === 'AUTO_VERIFIED' ? 'bg-green-100 text-green-800' : 
                      req.verification_status === 'REJECTED' ? 'bg-red-100 text-red-800' : 
                      'bg-yellow-100 text-yellow-800'}`}>
                    {req.verification_status === 'PENDING' || req.verification_status === 'MANUAL_REVIEW' ? <Clock size={12} /> : 
                     req.verification_status === 'REJECTED' ? <XCircle size={12} /> : <CheckCircle size={12} />}
                    <span>{req.verification_status.replace('_', ' ')}</span>
                  </div>
                </td>
                <td className="p-4 text-gray-600 text-sm">{new Date(req.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
            {requests.length === 0 && (
              <tr><td colSpan={4} className="p-8 text-center text-gray-500">No change requests found.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CitizenChangeRequests;
