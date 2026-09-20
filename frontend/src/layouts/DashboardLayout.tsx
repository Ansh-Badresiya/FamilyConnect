import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Users, FileText, Shield, LogOut, ClipboardList, RefreshCcw } from 'lucide-react';

const DashboardLayout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { label: 'My Family', path: '/dashboard', icon: <Users size={20} /> },
    { label: 'Find Benefits', path: '/schemes', icon: <Shield size={20} /> },
    { label: 'My Applications', path: '/applications', icon: <FileText size={20} /> },
    { label: 'Change Requests', path: '/change-requests', icon: <ClipboardList size={20} /> },
    { label: 'Family Transfers', path: '/family-transfers', icon: <RefreshCcw size={20} /> },
  ];

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-blue-900 text-white shadow-xl flex flex-col">
        <div className="p-6">
          <h1 className="text-2xl font-bold">FamilyConnect</h1>
          <p className="text-blue-200 text-sm mt-1">Gujarat Government</p>
        </div>
        
        <nav className="flex-1 mt-6">
          <ul className="space-y-1 px-3">
            {navItems.map((item) => (
              <li key={item.path}>
                <Link to={item.path} className="flex items-center space-x-3 px-4 py-3 text-blue-100 hover:bg-blue-800 rounded-lg transition-colors">
                  {item.icon}
                  <span>{item.label}</span>
                </Link>
              </li>
            ))}
          </ul>
        </nav>
        
        <div className="p-4 border-t border-blue-800">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-8 h-8 rounded-full bg-blue-700 flex items-center justify-center">
              <span className="font-semibold">{user?.email ? user.email.split('@')[0][0] : 'C'}</span>
            </div>
            <div>
              <p className="text-sm font-medium">{user?.email ? user.email.split('@')[0] : 'Citizen'}</p>
              <p className="text-xs text-blue-300">CITIZEN</p>
            </div>
          </div>
          <button 
            onClick={handleLogout}
            className="flex items-center space-x-2 text-blue-200 hover:text-white transition-colors w-full px-4 py-2"
          >
            <LogOut size={18} />
            <span>Logout</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <header className="bg-white shadow-sm border-b">
          <div className="px-8 py-4">
            <h2 className="text-xl font-semibold text-gray-800">
              Welcome back, Citizen
            </h2>
          </div>
        </header>
        <main className="p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
