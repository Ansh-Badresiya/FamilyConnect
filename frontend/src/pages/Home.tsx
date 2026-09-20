import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import api from '../services/api';
import { Shield, ArrowRight } from 'lucide-react';

const Home = () => {
  const [aadhaar, setAadhaar] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleAadhaarSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    if (aadhaar.length !== 12 || !/^\d+$/.test(aadhaar)) {
      setError('Please enter a valid 12-digit Aadhaar number');
      setLoading(false);
      return;
    }

    try {
      // In our new flow, we just POST the aadhaar number
      // The backend will verify it, auto-create a user if needed, and return a JWT
      const res = await api.post('/api/auth/login-aadhaar', { aadhaar_number: aadhaar });
      await login(res.data.access_token);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Authentication failed. Please check your Aadhaar number.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <Shield className="mx-auto h-16 w-16 text-blue-600" />
        <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
          FamilyConnect Gujarat
        </h2>
        <p className="mt-2 text-sm text-gray-600">
          Enter your Aadhaar Number to discover eligible schemes and manage your family profile.
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10 border-t-4 border-blue-600">
          
          <form className="space-y-6" onSubmit={handleAadhaarSubmit}>
            <div>
              <label htmlFor="aadhaar" className="block text-sm font-medium text-gray-700">
                Aadhaar Number
              </label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <input
                  id="aadhaar"
                  name="aadhaar"
                  type="text"
                  maxLength={12}
                  required
                  value={aadhaar}
                  onChange={(e) => setAadhaar(e.target.value)}
                  className="appearance-none block w-full px-3 py-3 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-lg text-center tracking-widest font-mono"
                  placeholder="XXXX XXXX XXXX"
                />
              </div>
            </div>

            {error && (
              <div className="text-red-600 text-sm bg-red-50 p-3 rounded">
                {error}
              </div>
            )}

            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-70 items-center transition-colors"
              >
                {loading ? 'Verifying Identity...' : (
                  <>
                    Access Dashboard <ArrowRight className="ml-2" size={16} />
                  </>
                )}
              </button>
            </div>
            
            <p className="text-xs text-center text-gray-500 mt-4 border-t pt-4">
              By proceeding, you consent to Aadhaar-based authentication for the purpose of identifying eligible government benefits for your family.
            </p>
          </form>

        </div>
      </div>
      
      <div className="mt-8 text-center text-gray-400 text-sm">
        <p>Example Hackathon Demo Numbers:</p>
        <p className="font-mono mt-1">482719365041 | 617384920156</p>
      </div>
    </div>
  );
};

export default Home;
