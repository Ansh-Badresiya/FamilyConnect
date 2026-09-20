import React, { useState, useEffect } from 'react';
import api from '../services/api';
import type { Family, EligibilityResult, Application } from '../types';
import { Edit2, X, CheckCircle, XCircle, FileText, AlertCircle, Lock, RefreshCcw, UserPlus, UserMinus } from 'lucide-react';

const CitizenDashboard = () => {
  const [family, setFamily] = useState<Family | null>(null);
  const [benefits, setBenefits] = useState<{eligible: EligibilityResult[], not_eligible: EligibilityResult[]}>({eligible: [], not_eligible: []});
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);

  const [resolving, setResolving] = useState(false);
  const [resolveError, setResolveError] = useState('');

  // Change Request State
  const [showChangeRequest, setShowChangeRequest] = useState(false);
  const [changeRequestData, setChangeRequestData] = useState({
    person_id: null as number | null,
    field_name: '',
    requested_value: '',
    reason: ''
  });

  // Add Member State
  const [showAddMember, setShowAddMember] = useState(false);
  const [addMemberData, setAddMemberData] = useState({
    name: '', gender: 'M', date_of_birth: '', relationship: 'SON', reason: ''
  });

  // Remove Member State
  const [showRemoveMember, setShowRemoveMember] = useState(false);
  const [removeMemberData, setRemoveMemberData] = useState({
    person_id: null as number | null,
    reason: ''
  });

  // Edit member state (for unverified fields only)
  const [editingMember, setEditingMember] = useState<any>(null);
  const [editMemberData, setEditMemberData] = useState({ mobile: '', occupation: '', education: '' });

  // Family Transfer State
  const [showTransfer, setShowTransfer] = useState(false);
  const [transferData, setTransferData] = useState({ reason: 'Marriage', spouse_aadhaar: '', person_id: null as number | null });
  const [transferVerifiedTarget, setTransferVerifiedTarget] = useState<{target_family_id: string, target_person_name: string} | null>(null);
  const [transferLoading, setTransferLoading] = useState(false);
  const [transferError, setTransferError] = useState('');

  const fetchFamily = async () => {
    try {
      const res = await api.get('/api/families/me');
      setFamily(res.data);
      
      const [benRes, appRes] = await Promise.all([
        api.get('/api/eligibility/my-benefits'),
        api.get('/api/applications/me')
      ]);
      setBenefits(benRes.data);
      setApplications(appRes.data);
    } catch (e) {
      setFamily(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFamily();
  }, []);

  const handleResolveFamily = async () => {
    setResolving(true);
    setResolveError('');
    try {
      await api.post('/api/families/resolve');
      await fetchFamily();
    } catch (e: any) {
      setResolveError(e.response?.data?.detail || "Failed to resolve family");
    } finally {
      setResolving(false);
    }
  };

  // Direct Edit for UNVERIFIED fields
  const handleEditMemberOpen = (member: any) => {
    setEditingMember(member);
    setEditMemberData({
      mobile: member.person.mobile || '',
      occupation: member.person.occupation || '',
      education: member.person.education || ''
    });
  };

  const handleUpdateMember = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingMember) return;
    try {
      await api.put(`/api/families/persons/${editingMember.person_id}`, editMemberData);
      setEditingMember(null);
      fetchFamily();
    } catch (err) {
      alert("Failed to update member details");
    }
  };

  // Change Request for VERIFIED fields
  const handleOpenChangeRequest = (person_id: number | null) => {
    setChangeRequestData({
      person_id,
      field_name: person_id ? 'name' : 'annual_income', // default selects
      requested_value: '',
      reason: ''
    });
    setShowChangeRequest(true);
  };

  const handleSubmitChangeRequest = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/api/change-requests', changeRequestData);
      setShowChangeRequest(false);
      alert("Change request submitted successfully. You can track it in the 'Change Requests' tab.");
    } catch (err: any) {
      alert(err.response?.data?.detail || "Failed to submit change request");
    }
  };

  // Add Member
  const handleSubmitAddMember = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/api/change-requests', {
        field_name: 'ADD_MEMBER',
        requested_value: JSON.stringify(addMemberData),
        reason: addMemberData.reason
      });
      setShowAddMember(false);
      setAddMemberData({ name: '', gender: 'M', date_of_birth: '', relationship: 'SON', reason: '' });
      alert("Add member request submitted successfully. You can track it in the 'Change Requests' tab.");
    } catch (err: any) {
      alert(err.response?.data?.detail || "Failed to submit request");
    }
  };

  // Remove Member
  const handleOpenRemoveMember = (person_id: number) => {
    setRemoveMemberData({ person_id, reason: '' });
    setShowRemoveMember(true);
  };

  const handleSubmitRemoveMember = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/api/change-requests', {
        person_id: removeMemberData.person_id,
        field_name: 'REMOVE_MEMBER',
        requested_value: 'REMOVE',
        reason: removeMemberData.reason
      });
      setShowRemoveMember(false);
      alert("Remove member request submitted successfully. You can track it in the 'Change Requests' tab.");
    } catch (err: any) {
      alert(err.response?.data?.detail || "Failed to submit request");
    }
  };

  // Family Transfer Methods
  const handleVerifyTransferTarget = async () => {
    setTransferLoading(true);
    setTransferError('');
    try {
      const res = await api.post('/api/family-transfers/verify-target', { spouse_aadhaar: transferData.spouse_aadhaar });
      setTransferVerifiedTarget(res.data);
    } catch (err: any) {
      setTransferError(err.response?.data?.detail || "Failed to verify target Aadhaar/Household");
    } finally {
      setTransferLoading(false);
    }
  };

  const handleSubmitTransfer = async () => {
    setTransferLoading(true);
    try {
      await api.post('/api/family-transfers', transferData);
      setShowTransfer(false);
      alert("Family transfer successful! Your dashboard will now reload with your new family details.");
      setTransferVerifiedTarget(null);
      setTransferData({ reason: 'Marriage', spouse_aadhaar: '', person_id: null });
      await fetchFamily();
    } catch (err: any) {
      alert(err.response?.data?.detail || "Failed to submit family transfer");
    } finally {
      setTransferLoading(false);
    }
  };

  const handleApply = async (schemeId: number) => {
    try {
      await api.post('/api/applications', { scheme_id: schemeId });
      alert("Application submitted successfully!");
      fetchFamily();
    } catch (e: any) {
      alert(e.response?.data?.detail || "Failed to apply");
    }
  };

  if (loading) return <div className="flex items-center justify-center p-12"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div></div>;

  if (!family) {
    return (
      <div className="max-w-2xl mx-auto bg-white p-8 shadow rounded border-t-4 border-blue-600">
        <h2 className="text-2xl font-bold mb-2">Welcome to FamilyConnect</h2>
        <p className="text-gray-600 mb-6">We need to link your Aadhaar identity to your household Ration Card to create your Family Profile.</p>
        
        {resolveError && (
          <div className="bg-red-50 text-red-700 p-4 rounded mb-6 text-sm font-medium border border-red-200">
            {resolveError}
          </div>
        )}

        <button 
          onClick={handleResolveFamily} 
          disabled={resolving}
          className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 font-medium w-full flex justify-center disabled:opacity-70"
        >
          {resolving ? 'Resolving via Government Databases...' : 'Link My Household & Create Family Profile'}
        </button>
        <p className="mt-4 text-xs text-gray-500 text-center">
          By proceeding, you authorize the system to automatically fetch your household records.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto relative">
      {/* Family Details Card */}
      <div className="bg-white p-6 rounded-lg shadow-sm mb-8 border border-blue-100">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Family Details</h2>
            <div className="flex items-center mt-1 space-x-2">
              <p className="text-blue-600 font-mono font-semibold">{family.family_id}</p>
              <span className="flex items-center text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded border">
                <Lock size={12} className="mr-1" /> System Generated
              </span>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <div className="bg-blue-50 px-4 py-2 rounded text-blue-800 font-medium flex flex-col items-end">
              <span>Income: ₹{family.annual_income.toLocaleString()}</span>
              <span className="text-[10px] flex items-center text-green-600 mt-0.5">
                <CheckCircle size={10} className="mr-1" /> Verified Source: Mock Ration Card
              </span>
            </div>
            <button
              onClick={() => handleOpenChangeRequest(null)}
              className="flex items-center space-x-1 text-orange-600 hover:text-orange-800 border border-orange-200 px-3 py-2 rounded hover:bg-orange-50 transition-colors text-sm font-medium"
            >
              <FileText size={14} />
              <span>Request Change</span>
            </button>
            <button
              onClick={() => { setTransferVerifiedTarget(null); setTransferData({ ...transferData, person_id: null }); setShowTransfer(true); }}
              className="flex items-center space-x-1 text-indigo-600 hover:text-indigo-800 border border-indigo-200 px-3 py-2 rounded hover:bg-indigo-50 transition-colors text-sm font-medium"
            >
              <RefreshCcw size={14} />
              <span>Transfer Self</span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 text-sm bg-gray-50 p-4 rounded border">
          <div><span className="text-gray-500 block text-xs">District</span> <span className="font-medium">{family.district || '—'}</span></div>
          <div><span className="text-gray-500 block text-xs">Taluka</span> <span className="font-medium">{family.taluka || '—'}</span></div>
          <div><span className="text-gray-500 block text-xs">Village</span> <span className="font-medium">{family.village || '—'}</span></div>
          <div className="col-span-3 mt-2 flex justify-end">
            <span className="text-[10px] flex items-center text-green-600">
              <CheckCircle size={10} className="mr-1" /> Address Verified Source: Mock Ration Card
            </span>
          </div>
        </div>
      </div>

      {/* Family Members */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-bold text-gray-800">Family Members</h3>
        </div>

        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 text-gray-600 border-b">
              <th className="p-3 font-medium">Name (Verified)</th>
              <th className="p-3 font-medium">Gender</th>
              <th className="p-3 font-medium">Contact & Details</th>
              <th className="p-3 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {family.members?.map(m => (
              <tr key={m.id} className="border-b hover:bg-gray-50">
                <td className="p-3">
                  <div className="font-medium text-gray-800 flex items-center">
                    {m.person.name}
                    {m.is_head && <span className="ml-2 text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded">HEAD</span>}
                  </div>
                  <div className="text-[10px] flex items-center text-green-600 mt-1">
                    <CheckCircle size={10} className="mr-1" /> Source: Mock Aadhaar
                  </div>
                </td>
                <td className="p-3 text-gray-600">{m.person.gender}</td>
                <td className="p-3">
                  <div className="text-xs text-gray-500">Mobile: <span className="text-gray-800">{m.person.mobile || '—'}</span></div>
                  <div className="text-xs text-gray-500 mt-0.5">Occ: <span className="text-gray-800">{m.person.occupation || '—'}</span></div>
                  <div className="text-xs text-blue-600 font-medium mt-1">✓ Citizen Verified</div>
                </td>
                <td className="p-3">
                  <div className="flex flex-col space-y-2 items-end">
                    <button
                      onClick={() => handleOpenRemoveMember(m.person.id!)}
                      className="text-red-600 hover:text-red-800 flex items-center space-x-1 text-xs font-medium border border-red-100 px-2 py-1 rounded hover:bg-red-50"
                    >
                      <UserMinus size={12} />
                      <span>Remove</span>
                    </button>
                    <button
                      onClick={() => { 
                        setTransferVerifiedTarget(null); 
                        setTransferData({ reason: 'Marriage', spouse_aadhaar: '', person_id: m.person.id! }); 
                        setShowTransfer(true); 
                      }}
                      className="text-indigo-600 hover:text-indigo-800 flex items-center space-x-1 text-xs font-medium border border-indigo-100 px-2 py-1 rounded hover:bg-indigo-50"
                    >
                      <RefreshCcw size={12} />
                      <span>Transfer</span>
                    </button>
                    <button
                      onClick={() => handleOpenChangeRequest(m.person.id!)}
                      className="text-orange-600 hover:text-orange-800 flex items-center space-x-1 text-xs font-medium border border-orange-100 px-2 py-1 rounded hover:bg-orange-50"
                    >
                      <FileText size={12} />
                      <span>Request Change</span>
                    </button>
                    <button
                      onClick={() => handleEditMemberOpen(m)}
                      className="text-blue-600 hover:text-blue-800 flex items-center space-x-1 text-xs font-medium border border-blue-100 px-2 py-1 rounded hover:bg-blue-50"
                    >
                      <Edit2 size={12} />
                      <span>Edit Info</span>
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {(!family.members || family.members.length === 0) && (
              <tr><td colSpan={4} className="p-4 text-center text-gray-500">No members found.</td></tr>
            )}
          </tbody>
        </table>

        <div className="mt-6 flex justify-end">
          <button
            onClick={() => setShowAddMember(true)}
            className="flex items-center space-x-1 text-green-700 bg-green-50 border border-green-200 px-4 py-2 rounded-md hover:bg-green-100 transition-colors text-sm font-bold"
          >
            <UserPlus size={16} />
            <span>Add Member (Birth/Adoption)</span>
          </button>
        </div>
      </div>

      {/* Applications Tracking */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 mb-8 mt-8">
        <h3 className="text-xl font-bold text-gray-800 mb-6">My Applications</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 text-gray-600 border-b">
                <th className="p-3 font-medium">Scheme Name</th>
                <th className="p-3 font-medium">Status</th>
                <th className="p-3 font-medium">Submitted On</th>
                <th className="p-3 font-medium">Remarks</th>
              </tr>
            </thead>
            <tbody>
              {applications.map(app => (
                <tr key={app.id} className="border-b hover:bg-gray-50">
                  <td className="p-3 font-medium text-gray-800">{app.scheme?.name}</td>
                  <td className="p-3">
                    <span className={`px-2 py-1 text-xs rounded-full font-medium ${
                      app.status === 'SUBMITTED' ? 'bg-blue-100 text-blue-800' :
                      app.status === 'APPROVED' ? 'bg-green-100 text-green-800' :
                      app.status === 'REJECTED' ? 'bg-red-100 text-red-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {app.status}
                    </span>
                  </td>
                  <td className="p-3 text-gray-600">{new Date(app.submitted_at).toLocaleDateString()}</td>
                  <td className="p-3 text-gray-600">{app.remarks || '—'}</td>
                </tr>
              ))}
              {applications.length === 0 && (
                <tr><td colSpan={4} className="p-4 text-center text-gray-500">No applications found.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Benefit Discovery */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 mb-8 mt-8">
        <h3 className="text-xl font-bold text-gray-800 mb-6">Potential Benefits</h3>
        
        <div className="space-y-6">
          <div>
            <h4 className="flex items-center text-lg font-bold text-green-700 mb-4 border-b pb-2">
              <CheckCircle className="mr-2" size={20} /> Eligible Schemes ({benefits.eligible.length})
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {benefits.eligible.map(ben => (
                <div key={ben.scheme_id} className="border border-green-200 rounded-lg p-4 bg-green-50 shadow-sm flex flex-col justify-between">
                  <div>
                    <h5 className="font-bold text-green-900 mb-1">{ben.scheme_name}</h5>
                    <p className="text-sm text-green-800 mb-3">{ben.description}</p>
                    <div className="mb-3">
                      <p className="text-xs font-semibold text-green-700 uppercase tracking-wider mb-1">Why you are eligible:</p>
                      <ul className="list-disc pl-4 text-sm text-green-800">
                        {ben.matched_rules.map((rule, idx) => <li key={idx}>{rule}</li>)}
                      </ul>
                    </div>
                  </div>
                  <button 
                    onClick={() => handleApply(ben.scheme_id)}
                    disabled={applications.some(a => a.scheme_id === ben.scheme_id)}
                    className="mt-4 w-full bg-green-600 text-white py-2 rounded font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    {applications.some(a => a.scheme_id === ben.scheme_id) ? 'Already Applied' : 'Apply Now'}
                  </button>
                </div>
              ))}
              {benefits.eligible.length === 0 && <p className="text-gray-500 italic p-4">No eligible schemes found.</p>}
            </div>
          </div>
          
          <div className="mt-8">
            <h4 className="flex items-center text-lg font-bold text-gray-500 mb-4 border-b pb-2">
              <XCircle className="mr-2" size={20} /> Not Eligible ({benefits.not_eligible.length})
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 opacity-75">
              {benefits.not_eligible.map(ben => (
                <div key={ben.scheme_id} className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                  <h5 className="font-bold text-gray-700 mb-1">{ben.scheme_name}</h5>
                  <p className="text-sm text-gray-500 mb-3">{ben.description}</p>
                  <div>
                    <p className="text-xs font-semibold text-red-500 uppercase tracking-wider mb-1">Failed Requirements:</p>
                    <ul className="list-disc pl-4 text-sm text-red-600">
                      {ben.failed_rules.map((rule, idx) => <li key={idx}>{rule}</li>)}
                    </ul>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Change Request Modal */}
      {showChangeRequest && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
            <div className="flex justify-between items-center mb-4 border-b pb-2">
              <h3 className="text-xl font-bold text-gray-800 flex items-center">
                <AlertCircle className="mr-2 text-orange-500" size={20} />
                Request Change
              </h3>
              <button onClick={() => setShowChangeRequest(false)} className="text-gray-400 hover:text-gray-700"><X size={20} /></button>
            </div>
            
            <p className="text-sm text-gray-600 mb-4 bg-orange-50 p-3 rounded border border-orange-100">
              You are requesting to change a <strong>Government Verified</strong> field. The change will not take effect until it is approved.
            </p>

            <form onSubmit={handleSubmitChangeRequest} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Field to Change</label>
                <select 
                  className="w-full border p-2 rounded focus:ring-2 focus:ring-blue-500 outline-none"
                  value={changeRequestData.field_name}
                  onChange={e => setChangeRequestData({...changeRequestData, field_name: e.target.value})}
                >
                  {changeRequestData.person_id ? (
                    <>
                      <option value="name">Name</option>
                      <option value="gender">Gender</option>
                      <option value="date_of_birth">Date of Birth</option>
                    </>
                  ) : (
                    <>
                      <option value="annual_income">Annual Income</option>
                      <option value="district">District</option>
                      <option value="taluka">Taluka</option>
                      <option value="village">Village</option>
                    </>
                  )}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Requested New Value</label>
                <input type="text" required className="w-full border p-2 rounded focus:ring-2 focus:ring-blue-500 outline-none"
                  value={changeRequestData.requested_value}
                  onChange={e => setChangeRequestData({...changeRequestData, requested_value: e.target.value})} />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Reason (Optional)</label>
                <textarea className="w-full border p-2 rounded focus:ring-2 focus:ring-blue-500 outline-none" rows={2}
                  value={changeRequestData.reason}
                  onChange={e => setChangeRequestData({...changeRequestData, reason: e.target.value})}></textarea>
              </div>

              <div className="flex justify-end space-x-2 pt-2 border-t mt-4">
                <button type="button" onClick={() => setShowChangeRequest(false)} className="px-4 py-2 text-gray-600 bg-gray-100 rounded hover:bg-gray-200 font-medium">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-orange-600 text-white rounded hover:bg-orange-700 font-medium">Submit Request</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Member Modal (For Citizen fields only) */}
      {editingMember && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold text-gray-800">Update Profile Details</h3>
              <button onClick={() => setEditingMember(null)} className="text-gray-400 hover:text-gray-700"><X size={20} /></button>
            </div>
            <p className="text-sm text-gray-500 mb-4">These fields are self-declared and do not require verification.</p>
            <form onSubmit={handleUpdateMember} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Mobile</label>
                <input type="text" className="w-full border p-2 rounded focus:ring-2 focus:ring-blue-500 outline-none"
                  value={editMemberData.mobile}
                  onChange={e => setEditMemberData({...editMemberData, mobile: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Occupation</label>
                <input type="text" className="w-full border p-2 rounded focus:ring-2 focus:ring-blue-500 outline-none"
                  value={editMemberData.occupation}
                  onChange={e => setEditMemberData({...editMemberData, occupation: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Education</label>
                <input type="text" className="w-full border p-2 rounded focus:ring-2 focus:ring-blue-500 outline-none"
                  value={editMemberData.education}
                  onChange={e => setEditMemberData({...editMemberData, education: e.target.value})} />
              </div>
              <div className="flex justify-end space-x-2 pt-2">
                <button type="button" onClick={() => setEditingMember(null)} className="px-4 py-2 text-gray-600 bg-gray-100 rounded hover:bg-gray-200">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Family Transfer Modal */}
      {showTransfer && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
            <div className="flex justify-between items-center mb-4 border-b pb-2">
              <h3 className="text-xl font-bold text-gray-800 flex items-center">
                <RefreshCcw className="mr-2 text-indigo-500" size={20} />
                Request Family Change
              </h3>
              <button onClick={() => setShowTransfer(false)} className="text-gray-400 hover:text-gray-700"><X size={20} /></button>
            </div>
            
            <p className="text-sm text-gray-600 mb-4 bg-indigo-50 p-3 rounded border border-indigo-100">
              Transfer to a new family profile due to life events like marriage. You will need to verify the target household using Mock Aadhaar.
            </p>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Reason for Transfer</label>
                <select 
                  className="w-full border p-2 rounded focus:ring-2 focus:ring-blue-500 outline-none disabled:bg-gray-100 disabled:text-gray-500"
                  value={transferData.reason}
                  disabled={transferVerifiedTarget !== null}
                  onChange={e => setTransferData({...transferData, reason: e.target.value})}
                >
                  <option value="Marriage">Marriage</option>
                  <option value="Divorce">Divorce</option>
                  <option value="Adoption">Adoption</option>
                  <option value="Relocation">Relocation</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Reference Aadhaar Number (e.g. Spouse)</label>
                <div className="flex space-x-2">
                  <input type="text" required className="flex-1 border p-2 rounded focus:ring-2 focus:ring-blue-500 outline-none disabled:bg-gray-100 disabled:text-gray-500"
                    placeholder="12-digit Aadhaar"
                    value={transferData.spouse_aadhaar}
                    disabled={transferVerifiedTarget !== null}
                    onChange={e => setTransferData({...transferData, spouse_aadhaar: e.target.value})} />
                  {!transferVerifiedTarget && (
                    <button 
                      type="button"
                      onClick={handleVerifyTransferTarget}
                      disabled={transferLoading || !transferData.spouse_aadhaar}
                      className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 disabled:opacity-50"
                    >
                      {transferLoading ? '...' : 'Verify'}
                    </button>
                  )}
                </div>
                {transferError && <p className="text-xs text-red-600 mt-1">{transferError}</p>}
              </div>

              {transferVerifiedTarget && (
                <div className="mt-4 p-4 border rounded-lg bg-green-50 border-green-200">
                  <div className="flex items-center text-green-800 mb-2 font-medium">
                    <CheckCircle size={16} className="mr-1" /> Target Household Found
                  </div>
                  <div className="text-sm text-green-900">
                    <p><strong>Target Family:</strong> <span className="font-mono">{transferVerifiedTarget.target_family_id}</span></p>
                    <p><strong>Target Person:</strong> {transferVerifiedTarget.target_person_name}</p>
                  </div>
                </div>
              )}

              <div className="flex justify-end space-x-2 pt-2 border-t mt-4">
                <button type="button" onClick={() => setShowTransfer(false)} className="px-4 py-2 text-gray-600 bg-gray-100 rounded hover:bg-gray-200 font-medium">Cancel</button>
                {transferVerifiedTarget && (
                  <button onClick={handleSubmitTransfer} disabled={transferLoading} className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 font-medium disabled:opacity-50 flex items-center">
                    {transferLoading ? 'Submitting...' : 'Submit Transfer Request'}
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Add Member Modal */}
      {showAddMember && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
            <div className="flex justify-between items-center mb-4 border-b pb-2">
              <h3 className="text-xl font-bold text-gray-800 flex items-center">
                <UserPlus className="mr-2 text-green-600" size={20} />
                Add Member Request
              </h3>
              <button onClick={() => setShowAddMember(false)} className="text-gray-400 hover:text-gray-700"><X size={20} /></button>
            </div>
            
            <p className="text-sm text-gray-600 mb-4 bg-green-50 p-3 rounded border border-green-100">
              Submit a request to add a new member to your family profile. The request will be reviewed by officials.
            </p>

            <form onSubmit={handleSubmitAddMember} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                <input type="text" required className="w-full border p-2 rounded focus:ring-2 focus:ring-green-500 outline-none"
                  value={addMemberData.name}
                  onChange={e => setAddMemberData({...addMemberData, name: e.target.value})} />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Gender</label>
                  <select 
                    className="w-full border p-2 rounded focus:ring-2 focus:ring-green-500 outline-none"
                    value={addMemberData.gender}
                    onChange={e => setAddMemberData({...addMemberData, gender: e.target.value})}
                  >
                    <option value="M">Male</option>
                    <option value="F">Female</option>
                    <option value="O">Other</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Date of Birth</label>
                  <input type="date" required className="w-full border p-2 rounded focus:ring-2 focus:ring-green-500 outline-none"
                    value={addMemberData.date_of_birth}
                    onChange={e => setAddMemberData({...addMemberData, date_of_birth: e.target.value})} />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Relationship to Head</label>
                <select 
                  className="w-full border p-2 rounded focus:ring-2 focus:ring-green-500 outline-none"
                  value={addMemberData.relationship}
                  onChange={e => setAddMemberData({...addMemberData, relationship: e.target.value})}
                >
                  <option value="SON">Son</option>
                  <option value="DAUGHTER">Daughter</option>
                  <option value="SPOUSE">Spouse</option>
                  <option value="FATHER">Father</option>
                  <option value="MOTHER">Mother</option>
                  <option value="OTHER">Other</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Reason (Birth, Adoption, etc.)</label>
                <input type="text" required className="w-full border p-2 rounded focus:ring-2 focus:ring-green-500 outline-none"
                  placeholder="e.g. Newborn child"
                  value={addMemberData.reason}
                  onChange={e => setAddMemberData({...addMemberData, reason: e.target.value})} />
              </div>

              <div className="flex justify-end space-x-2 pt-2 border-t mt-4">
                <button type="button" onClick={() => setShowAddMember(false)} className="px-4 py-2 text-gray-600 bg-gray-100 rounded hover:bg-gray-200 font-medium">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 font-medium">Submit Request</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Remove Member Modal */}
      {showRemoveMember && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
            <div className="flex justify-between items-center mb-4 border-b pb-2">
              <h3 className="text-xl font-bold text-gray-800 flex items-center">
                <UserMinus className="mr-2 text-red-600" size={20} />
                Remove Member Request
              </h3>
              <button onClick={() => setShowRemoveMember(false)} className="text-gray-400 hover:text-gray-700"><X size={20} /></button>
            </div>
            
            <p className="text-sm text-gray-600 mb-4 bg-red-50 p-3 rounded border border-red-100">
              Submit a request to remove this member from your family profile (e.g. due to death). This action will be verified before taking effect.
            </p>

            <form onSubmit={handleSubmitRemoveMember} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Reason for Removal</label>
                <select 
                  className="w-full border p-2 rounded focus:ring-2 focus:ring-red-500 outline-none"
                  value={removeMemberData.reason}
                  onChange={e => setRemoveMemberData({...removeMemberData, reason: e.target.value})}
                  required
                >
                  <option value="" disabled>Select a reason...</option>
                  <option value="Death">Death</option>
                  <option value="Moved Out">Moved Out</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              
              {removeMemberData.reason === 'Other' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Specify Reason</label>
                  <input type="text" required className="w-full border p-2 rounded focus:ring-2 focus:ring-red-500 outline-none"
                    placeholder="Enter details"
                    onChange={e => setRemoveMemberData({...removeMemberData, reason: e.target.value})} />
                </div>
              )}

              <div className="flex justify-end space-x-2 pt-2 border-t mt-4">
                <button type="button" onClick={() => setShowRemoveMember(false)} className="px-4 py-2 text-gray-600 bg-gray-100 rounded hover:bg-gray-200 font-medium">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 font-medium">Submit Request</button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};

export default CitizenDashboard;
