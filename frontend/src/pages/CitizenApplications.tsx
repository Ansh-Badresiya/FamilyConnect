import React, { useState, useEffect } from 'react';
import api from '../services/api';
import type { Application, Scheme } from '../types';

const CitizenApplications = () => {
  const [applications, setApplications] = useState<(Application & { scheme?: Scheme })[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchApps = async () => {
      try {
        const res = await api.get('/api/applications/me');
        setApplications(res.data);
      } catch (err) {
        console.error("Failed to fetch applications");
      } finally {
        setLoading(false);
      }
    };
    fetchApps();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">My Applications</h2>
      
      <div className="bg-white shadow-sm rounded-lg border overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="p-4 font-medium text-gray-600">Application ID</th>
              <th className="p-4 font-medium text-gray-600">Scheme</th>
              <th className="p-4 font-medium text-gray-600">Status</th>
              <th className="p-4 font-medium text-gray-600">Submitted Date</th>
              <th className="p-4 font-medium text-gray-600">Remarks</th>
            </tr>
          </thead>
          <tbody>
            {applications.map(app => (
              <tr key={app.id} className="border-b last:border-b-0 hover:bg-gray-50">
                <td className="p-4 font-mono text-sm text-gray-500">APP-{app.id.toString().padStart(4, '0')}</td>
                <td className="p-4 font-medium text-gray-800">{app.scheme?.name}</td>
                <td className="p-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold
                    ${app.status === 'APPROVED' ? 'bg-green-100 text-green-800' : 
                      app.status === 'REJECTED' ? 'bg-red-100 text-red-800' : 
                      'bg-yellow-100 text-yellow-800'}`}>
                    {app.status}
                  </span>
                </td>
                <td className="p-4 text-gray-600 text-sm">{new Date(app.submitted_at).toLocaleDateString()}</td>
                <td className="p-4 text-gray-600 text-sm">{app.remarks || '-'}</td>
              </tr>
            ))}
            {applications.length === 0 && (
              <tr><td colSpan={5} className="p-8 text-center text-gray-500">No applications found.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CitizenApplications;
