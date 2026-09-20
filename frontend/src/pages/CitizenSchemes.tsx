import { useState } from 'react';
import api from '../services/api';
import type { EligibilityResult } from '../types';
import { CheckCircle, XCircle } from 'lucide-react';

const CitizenSchemes = () => {
  const [results, setResults] = useState<EligibilityResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchEligibility = async () => {
    setLoading(true);
    try {
      const res = await api.get('/api/eligibility/my-benefits');
      // combine eligible and not_eligible into a single array for rendering
      const combined = [
        ...res.data.eligible,
        ...res.data.not_eligible
      ];
      setResults(combined);
    } catch (err) {
      setError("Failed to fetch eligibility. Have you created your family profile?");
    } finally {
      setLoading(false);
    }
  };

  const handleApply = async (schemeId: number) => {
    try {
      const famRes = await api.get('/api/families/me');
      await api.post('/api/applications', {
        family_id: famRes.data.id,
        scheme_id: schemeId
      });
      alert("Application submitted successfully!");
    } catch(err) {
      alert("Failed to submit application");
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Find Benefits</h2>
          <p className="text-gray-600 mt-1">Discover government schemes your family is eligible for.</p>
        </div>
        <button onClick={fetchEligibility} className="bg-blue-600 text-white px-6 py-2 rounded shadow hover:bg-blue-700 transition-colors">
          Check Eligibility
        </button>
      </div>

      {error && <div className="bg-red-50 text-red-700 p-4 rounded mb-6">{error}</div>}
      
      {loading ? (
        <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div></div>
      ) : (
        <div className="space-y-6">
          {results.map(res => (
            <div key={res.scheme_id} className={`bg-white rounded-lg shadow-sm border-l-4 p-6 ${res.eligible ? 'border-green-500' : 'border-red-500'}`}>
              <div className="flex justify-between items-start">
                <div className="flex items-start space-x-4">
                  {res.eligible ? <CheckCircle className="text-green-500 mt-1" size={24} /> : <XCircle className="text-red-500 mt-1" size={24} />}
                  <div>
                    <h3 className="text-xl font-bold text-gray-800">{res.scheme_name}</h3>
                    <p className="text-gray-600 mt-2">{res.description}</p>
                    
                    <div className="mt-4">
                      {res.matched_rules.length > 0 && (
                        <div className="mb-2">
                          <p className="text-sm font-semibold text-green-700 mb-1">Matched Rules:</p>
                          <ul className="list-disc pl-5 text-sm text-gray-600">
                            {res.matched_rules.map((rule, idx) => <li key={idx}>{rule}</li>)}
                          </ul>
                        </div>
                      )}
                      {res.failed_rules.length > 0 && (
                        <div>
                          <p className="text-sm font-semibold text-red-700 mb-1">Failed Rules:</p>
                          <ul className="list-disc pl-5 text-sm text-gray-600">
                            {res.failed_rules.map((rule, idx) => <li key={idx}>{rule}</li>)}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
                
                {res.eligible && (
                  <button onClick={() => handleApply(res.scheme_id)} className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded text-sm transition-colors">
                    Apply Now
                  </button>
                )}
              </div>
            </div>
          ))}
          {results.length === 0 && !loading && !error && (
            <div className="text-center p-12 bg-gray-50 rounded text-gray-500">
              Click 'Check Eligibility' to evaluate your family's profile against all schemes.
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CitizenSchemes;
