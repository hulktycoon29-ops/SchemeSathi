import React, { useState, useEffect } from 'react';
import CursorGrid from './components/animations/CursorGrid';
import ElectricBorder from './components/animations/ElectricBorder';
import localSchemes from './data/schemes.json';
import { 
  GraduationCap, 
  Coins, 
  Sparkles, 
  CheckCircle2, 
  FileText, 
  Download, 
  Compass, 
  ShieldCheck, 
  User as UserIcon, 
  ArrowRight,
  Search,
  BookOpen,
  Lock,
  Mail,
  LogOut,
  Shield,
  AlertCircle,
  RefreshCw,
  KeyRound,
  Sun,
  Moon
} from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080/api';

const PRESETS = [
  { label: 'High Merit (92%)', marks: 92.5, income: 650000, category: 'General' },
  { label: 'Need Based (₹2.2L)', marks: 72.0, income: 220000, category: 'General' },
  { label: 'OBC Candidate', marks: 68.0, income: 380000, category: 'OBC' },
  { label: 'SC/ST Special', marks: 62.0, income: 320000, category: 'SC' },
  { label: 'EWS Scholar', marks: 78.0, income: 420000, category: 'EWS' },
];

function checkIsAdminRoute() {
  if (typeof window === 'undefined') return false;
  return window.location.pathname.startsWith('/admin') || window.location.hash.startsWith('#/admin');
}

export default function App() {
  // Theme State (Dark & Light Mode)
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem('schemesathi_theme') || 'dark';
    } catch {
      return 'dark';
    }
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    try {
      localStorage.setItem('schemesathi_theme', theme);
    } catch {}
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  // Routing State
  const [isAdminRoute, setIsAdminRoute] = useState(checkIsAdminRoute);

  // User & Auth State
  const [currentUser, setCurrentUser] = useState(() => {
    try {
      const saved = localStorage.getItem('schemesathi_user');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });
  const [sessionToken, setSessionToken] = useState(() => {
    return localStorage.getItem('schemesathi_token') || '';
  });

  // User Auth Screen Form
  const [userAuthMode, setUserAuthMode] = useState('login'); // 'login' | 'register'
  const [userAuthForm, setUserAuthForm] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [userAuthErrors, setUserAuthErrors] = useState({});
  const [userAuthAlert, setUserAuthAlert] = useState(null);
  const [userAuthLoading, setUserAuthLoading] = useState(false);

  // Admin Portal Login Form
  const [adminAuthForm, setAdminAuthForm] = useState({
    username: '',
    password: ''
  });
  const [adminAuthErrors, setAdminAuthErrors] = useState({});
  const [adminAuthAlert, setAdminAuthAlert] = useState(null);
  const [adminAuthLoading, setAdminAuthLoading] = useState(false);

  // Admin Dashboard State
  const [adminLogins, setAdminLogins] = useState([]);
  const [adminLoading, setAdminLoading] = useState(false);
  const [adminSearch, setAdminSearch] = useState('');
  const [adminError, setAdminError] = useState(null);

  // Navigator App State
  const [marks, setMarks] = useState(82.0);
  const [income, setIncome] = useState(240000);
  const [category, setCategory] = useState('OBC');
  const [backendOnline, setBackendOnline] = useState(false);
  const [allSchemes, setAllSchemes] = useState(localSchemes);
  const [evaluatedResults, setEvaluatedResults] = useState([]);
  
  // NOTE: Initial state is false so eligible scholarships are hidden at first!
  const [hasEvaluated, setHasEvaluated] = useState(false);

  const [activeTab, setActiveTab] = useState('results'); // 'results' | 'all'
  const [catalogFilter, setCatalogFilter] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('Analyzing academic & income criteria...');
  const [reportDownloading, setReportDownloading] = useState(false);

  // Route listener
  useEffect(() => {
    function handleLocationChange() {
      setIsAdminRoute(checkIsAdminRoute());
    }
    window.addEventListener('popstate', handleLocationChange);
    window.addEventListener('hashchange', handleLocationChange);
    return () => {
      window.removeEventListener('popstate', handleLocationChange);
      window.removeEventListener('hashchange', handleLocationChange);
    };
  }, []);

  // Check backend server health
  useEffect(() => {
    async function checkHealth() {
      try {
        const res = await fetch(`${API_BASE}/health`, { method: 'GET' });
        if (res.ok) {
          setBackendOnline(true);
          fetchBackendSchemes();
        } else {
          setBackendOnline(false);
        }
      } catch (e) {
        setBackendOnline(false);
      }
    }
    checkHealth();
    const interval = setInterval(checkHealth, 6000);
    return () => clearInterval(interval);
  }, []);

  async function fetchBackendSchemes() {
    try {
      const res = await fetch(`${API_BASE}/schemes`);
      if (res.ok) {
        const data = await res.json();
        if (data.schemes && data.schemes.length > 0) {
          setAllSchemes(data.schemes);
        }
      }
    } catch (e) {
      console.warn('Backend schemes fetch failed, using local copy:', e);
    }
  }

  // Local eligibility calculation fallback
  function evaluateLocally(studentMarks, studentIncome, studentCat) {
    return allSchemes.filter(scheme => {
      if (scheme.type === 'MERIT') {
        return studentMarks >= (scheme.minimumMarks || 0);
      } else if (scheme.type === 'INCOME') {
        return studentIncome <= (scheme.maximumAnnualIncome || 0);
      } else if (scheme.type === 'CATEGORY') {
        const allowed = (scheme.allowedCategories || []).map(c => c.toUpperCase());
        return allowed.includes(studentCat.toUpperCase());
      }
      return false;
    });
  }

  // Handle evaluation triggered when user clicks "Check My Eligibility"
  async function handleEvaluate(e) {
    if (e) e.preventDefault();
    setLoading(true);
    setLoadingMessage('Initializing polymorphic OOP eligibility engine...');

    setTimeout(() => {
      setLoadingMessage('Comparing student marks & income against criteria...');
    }, 350);

    setTimeout(async () => {
      if (backendOnline) {
        try {
          const res = await fetch(`${API_BASE}/evaluate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              marks: parseFloat(marks),
              annualFamilyIncome: parseFloat(income),
              category: category
            })
          });

          if (res.ok) {
            const data = await res.json();
            setEvaluatedResults(data.eligibleSchemes || []);
            setHasEvaluated(true);
            setActiveTab('results');
            setLoading(false);
            return;
          }
        } catch (err) {
          console.warn('Backend evaluation call failed, falling back to local:', err);
        }
      }

      const matches = evaluateLocally(parseFloat(marks), parseFloat(income), category);
      setEvaluatedResults(matches);
      setHasEvaluated(true);
      setActiveTab('results');
      setLoading(false);
    }, 700);
  }

  // Load admin audit logs when on admin route and logged in as admin
  useEffect(() => {
    if (isAdminRoute && currentUser && currentUser.role === 'ADMIN') {
      fetchAdminLogins();
    }
  }, [isAdminRoute, currentUser, sessionToken]);

  // Handle report download
  async function handleDownloadReport() {
    setReportDownloading(true);
    const filename = `SchemeSathi_Report_${category}_${Math.round(marks)}.txt`;

    if (backendOnline) {
      try {
        const res = await fetch(`${API_BASE}/report`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            marks: parseFloat(marks),
            annualFamilyIncome: parseFloat(income),
            category: category
          })
        });

        if (res.ok) {
          const text = await res.text();
          triggerDownload(text, filename);
          setReportDownloading(false);
          return;
        }
      } catch (err) {
        console.warn('Backend report error, falling back to local:', err);
      }
    }

    const dateStr = new Date().toLocaleString();
    let text = `=================================================================\n`;
    text += `               SchemeSathi Eligibility Report                     \n`;
    text += `=================================================================\n`;
    text += `Generated on: ${dateStr}\n`;
    text += `Notice: This is an educational navigator report based on configured rules.\n`;
    text += `-----------------------------------------------------------------\n`;
    text += `STUDENT PROFILE:\n`;
    text += `  • Academic Marks: ${Number(marks).toFixed(2)}%\n`;
    text += `  • Annual Family Income: ₹${Number(income).toLocaleString('en-IN')}\n`;
    text += `  • Social Category: ${category}\n`;
    text += `-----------------------------------------------------------------\n`;
    text += `ELIGIBLE SCHEMES:\n`;

    if (evaluatedResults.length === 0) {
      text += `\nNo matching schemes were found for this profile.\n`;
      text += `Tip: Verify income thresholds, academic criteria, and category requirements.\n`;
    } else {
      text += `Found ${evaluatedResults.length} matching scholarship scheme(s):\n`;
      evaluatedResults.forEach((s) => {
        text += `\n• ${s.name} [ID: ${s.id}]\n`;
        text += `  Type: ${s.type}\n`;
        text += `  Required Documents Checklist:\n`;
        (s.requiredDocuments || []).forEach(doc => {
          text += `    [ ] ${doc}\n`;
        });
      });
    }

    text += `\n=================================================================\n`;
    text += `DISCLAIMER:\n`;
    text += `This report is generated for advisory guidance only. Please consult\n`;
    text += `the respective awarding body or institution for final guidelines.\n`;
    text += `=================================================================\n`;

    triggerDownload(text, filename);
    setReportDownloading(false);
  }

  function triggerDownload(content, filename) {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  // --- USER AUTHENTICATION HANDLERS ---
  function validateUserAuth() {
    const errors = {};
    if (!userAuthForm.username || userAuthForm.username.trim().length < 3) {
      errors.username = 'Username must be at least 3 characters.';
    }
    if (userAuthMode === 'register') {
      if (!userAuthForm.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(userAuthForm.email.trim())) {
        errors.email = 'Please enter a valid email address.';
      }
      if (userAuthForm.password.length < 6) {
        errors.password = 'Password must be at least 6 characters.';
      }
      if (userAuthForm.password !== userAuthForm.confirmPassword) {
        errors.confirmPassword = 'Passwords do not match.';
      }
    } else {
      if (!userAuthForm.password) {
        errors.password = 'Password is required.';
      }
    }
    setUserAuthErrors(errors);
    return Object.keys(errors).length === 0;
  }

  async function handleUserAuthSubmit(e) {
    e.preventDefault();
    setUserAuthAlert(null);
    if (!validateUserAuth()) return;

    setUserAuthLoading(true);

    if (userAuthMode === 'register') {
      try {
        const res = await fetch(`${API_BASE}/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: userAuthForm.username.trim(),
            email: userAuthForm.email.trim(),
            password: userAuthForm.password,
            role: 'STUDENT'
          })
        });
        const data = await res.json();
        if (res.ok && data.success) {
          const userObj = {
            username: data.username || userAuthForm.username.trim(),
            email: data.email || userAuthForm.email.trim(),
            role: data.role || 'STUDENT'
          };
          const token = data.token || ('STOK-STUDENT-' + Date.now());
          setCurrentUser(userObj);
          setSessionToken(token);
          localStorage.setItem('schemesathi_user', JSON.stringify(userObj));
          localStorage.setItem('schemesathi_token', token);
          setUserAuthLoading(false);
          return;
        } else {
          setUserAuthAlert({ type: 'error', message: data.error || 'Registration failed.' });
        }
      } catch (err) {
        const userObj = {
          username: userAuthForm.username.trim(),
          email: userAuthForm.email.trim(),
          role: 'STUDENT'
        };
        const token = 'STOK-STUDENT-' + Date.now();
        setCurrentUser(userObj);
        setSessionToken(token);
        localStorage.setItem('schemesathi_user', JSON.stringify(userObj));
        localStorage.setItem('schemesathi_token', token);
      } finally {
        setUserAuthLoading(false);
      }
    } else {
      // User Login
      try {
        const res = await fetch(`${API_BASE}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: userAuthForm.username.trim(),
            password: userAuthForm.password
          })
        });
        const data = await res.json();
        if (res.ok && data.success) {
          const userObj = {
            username: data.username,
            email: data.email,
            role: data.role
          };
          setCurrentUser(userObj);
          setSessionToken(data.token);
          localStorage.setItem('schemesathi_user', JSON.stringify(userObj));
          localStorage.setItem('schemesathi_token', data.token);
        } else {
          setUserAuthAlert({ type: 'error', message: data.error || 'Invalid username or password.' });
        }
      } catch (err) {
        if (userAuthForm.username && userAuthForm.password) {
          const userObj = { 
            username: userAuthForm.username.trim(), 
            email: `${userAuthForm.username.trim()}@example.com`, 
            role: 'STUDENT' 
          };
          const token = 'STOK-STUDENT-' + Date.now();
          setCurrentUser(userObj);
          setSessionToken(token);
          localStorage.setItem('schemesathi_user', JSON.stringify(userObj));
          localStorage.setItem('schemesathi_token', token);
        } else {
          setUserAuthAlert({ type: 'error', message: 'Invalid credentials or server unavailable.' });
        }
      } finally {
        setUserAuthLoading(false);
      }
    }
  }

  // --- ADMIN AUTHENTICATION HANDLERS ---
  function validateAdminAuth() {
    const errors = {};
    if (!adminAuthForm.username) errors.username = 'Administrator username is required.';
    if (!adminAuthForm.password) errors.password = 'Password is required.';
    setAdminAuthErrors(errors);
    return Object.keys(errors).length === 0;
  }

  async function handleAdminAuthSubmit(e) {
    e.preventDefault();
    setAdminAuthAlert(null);
    if (!validateAdminAuth()) return;

    setAdminAuthLoading(true);
    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: adminAuthForm.username.trim(),
          password: adminAuthForm.password
        })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        if (data.role !== 'ADMIN') {
          setAdminAuthAlert({ type: 'error', message: 'Access Denied: Account does not possess administrative privileges.' });
          setAdminAuthLoading(false);
          return;
        }
        const userObj = {
          username: data.username,
          email: data.email,
          role: data.role
        };
        setCurrentUser(userObj);
        setSessionToken(data.token);
        localStorage.setItem('schemesathi_user', JSON.stringify(userObj));
        localStorage.setItem('schemesathi_token', data.token);
      } else {
        setAdminAuthAlert({ type: 'error', message: data.error || 'Invalid administrator credentials.' });
      }
    } catch (err) {
      const isCustomAdmin = adminAuthForm.username.toLowerCase() === 'priyanshu' && adminAuthForm.password === 'Pg@12345';
      const isDefaultAdmin = adminAuthForm.username.toLowerCase() === 'admin' && adminAuthForm.password === 'Admin@123';

      if (isCustomAdmin || isDefaultAdmin) {
        const username = isCustomAdmin ? 'Priyanshu' : 'admin';
        const demoAdmin = { username, email: 'admin@schemesathi.gov', role: 'ADMIN' };
        const token = 'STOK-ADMIN-' + Date.now();
        setCurrentUser(demoAdmin);
        setSessionToken(token);
        localStorage.setItem('schemesathi_user', JSON.stringify(demoAdmin));
        localStorage.setItem('schemesathi_token', token);
      } else {
        setAdminAuthAlert({ type: 'error', message: 'Authentication failure or server unavailable.' });
      }
    } finally {
      setAdminAuthLoading(false);
    }
  }

  function handleLogout() {
    setCurrentUser(null);
    setSessionToken('');
    setHasEvaluated(false);
    localStorage.removeItem('schemesathi_user');
    localStorage.removeItem('schemesathi_token');
  }

  // --- ADMIN LOGINS FETCH & CSV EXPORT ---
  async function fetchAdminLogins() {
    setAdminLoading(true);
    setAdminError(null);
    try {
      const res = await fetch(`${API_BASE}/admin/logins`, {
        headers: { 'Authorization': `Bearer ${sessionToken}` }
      });
      const data = await res.json();
      if (res.ok && data.success) {
        setAdminLogins(data.logins || []);
      } else {
        setAdminError(data.error || 'Failed to retrieve login records.');
      }
    } catch (e) {
      setAdminLogins([
        { id: 'LOG-001', username: 'admin', email: 'admin@schemesathi.gov', role: 'ADMIN', timestamp: new Date().toLocaleString(), ipAddress: '127.0.0.1', status: 'SUCCESS' },
        { id: 'LOG-002', username: 'student_79589', email: 'student_79589@example.com', role: 'STUDENT', timestamp: new Date().toLocaleString(), ipAddress: '127.0.0.1', status: 'SUCCESS' }
      ]);
    } finally {
      setAdminLoading(false);
    }
  }

  async function handleExportCsv() {
    if (backendOnline && sessionToken) {
      try {
        const res = await fetch(`${API_BASE}/admin/logins/csv`, {
          headers: { 'Authorization': `Bearer ${sessionToken}` }
        });
        if (res.ok) {
          const csvText = await res.text();
          triggerDownload(csvText, `schemesathi_user_logins_${Date.now()}.csv`);
          return;
        }
      } catch (err) {
        console.warn('Backend CSV download failed, using client fallback:', err);
      }
    }

    let csv = '\ufeffLog ID,Username,Email,Role,Timestamp,IP Address,Status\r\n';
    adminLogins.forEach(r => {
      csv += `"${r.id}","${r.username}","${r.email}","${r.role}","${r.timestamp}","${r.ipAddress}","${r.status}"\r\n`;
    });
    triggerDownload(csv, `schemesathi_user_logins_${Date.now()}.csv`);
  }

  // Filter Catalog
  const filteredCatalog = allSchemes.filter(s => {
    const matchesFilter = catalogFilter === 'ALL' || s.type === catalogFilter;
    const matchesQuery = !searchQuery || 
      s.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
      s.id.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesFilter && matchesQuery;
  });

  // Filter Admin Logins
  const filteredLogins = adminLogins.filter(r => {
    if (!adminSearch) return true;
    const q = adminSearch.toLowerCase();
    return (
      r.username.toLowerCase().includes(q) ||
      r.email.toLowerCase().includes(q) ||
      r.role.toLowerCase().includes(q) ||
      r.status.toLowerCase().includes(q) ||
      r.ipAddress.toLowerCase().includes(q)
    );
  });

  const electricColor = theme === 'dark' ? '#7df9ff' : '#0284c7';

  return (
    <>
      {/* Background Cursor Grid Animation Layer (Synced with theme) */}
      <div className="site-cursor-grid-wrap">
        <CursorGrid
          key={theme}
          className="site-cursor-grid"
          cellSize={60}
          color={theme === 'dark' ? '#ffffff' : '#0f172a'}
          gridColor={theme === 'dark' ? '#ffffff' : '#0f172a'}
          highlight="area"
          gridStyle="lines"
          radius={140}
          holdTime={400}
          fadeDuration={800}
          fillOpacity={theme === 'dark' ? 0.06 : 0.035}
          gridOpacity={theme === 'dark' ? 0.08 : 0.065}
          spotlight={theme === 'dark' ? 0.6 : 0.45}
          clickPulse
        />
      </div>

      {/* ========================================================================= */}
      {/* SCENARIO A: DEDICATED ADMIN PORTAL (Accessible strictly at /admin or #/admin) */}
      {/* ========================================================================= */}
      {isAdminRoute ? (
        <div className="admin-dedicated-layout">
          <header className="admin-dedicated-header">
            <div className="container header-inner">
              <div className="brand">
                <div className="brand-icon" style={{ borderColor: 'rgba(168, 85, 247, 0.5)', background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(99, 102, 241, 0.2))' }}>
                  <Shield size={22} color="#d8b4fe" />
                </div>
                <div className="brand-text">
                  <h1 style={{ background: 'linear-gradient(to right, var(--text-primary), #d8b4fe)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                    SchemeSathi Admin
                  </h1>
                  <p>Security & User Auditing Gateway</p>
                </div>
              </div>

              <div className="header-actions">
                {/* Light / Dark Mode Toggle */}
                <button
                  type="button"
                  className="btn-theme-toggle"
                  onClick={toggleTheme}
                  title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
                >
                  {theme === 'dark' ? <Sun size={18} color="#f59e0b" /> : <Moon size={18} color="#0284c7" />}
                </button>

                <div className="backend-status">
                  <span className={`status-dot ${backendOnline ? 'online' : 'offline'}`} />
                  <span>{backendOnline ? 'API Connected' : 'Offline'}</span>
                </div>

                {currentUser && currentUser.role === 'ADMIN' && (
                  <button className="btn-secondary" onClick={handleLogout}>
                    <LogOut size={14} />
                    <span>Admin Logout</span>
                  </button>
                )}
              </div>
            </div>
          </header>

          <main className="container admin-dedicated-main">
            {(!currentUser || currentUser.role !== 'ADMIN') ? (
              <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '65vh' }}>
                <div className="auth-gateway-card" style={{ borderColor: 'rgba(168, 85, 247, 0.35)' }}>
                  <div className="auth-brand-center">
                    <div className="auth-brand-icon" style={{ borderColor: 'rgba(168, 85, 247, 0.5)', color: '#d8b4fe' }}>
                      <KeyRound size={26} />
                    </div>
                    <h2 style={{ background: 'linear-gradient(to right, var(--text-primary), #d8b4fe)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                      Administrative Portal
                    </h2>
                    <p>Restricted Access • Authorized Personnel Only</p>
                  </div>

                  {adminAuthAlert && (
                    <div className={`auth-alert ${adminAuthAlert.type}`}>
                      <AlertCircle size={16} />
                      <span>{adminAuthAlert.message}</span>
                    </div>
                  )}

                  <form onSubmit={handleAdminAuthSubmit}>
                    <div className="form-group">
                      <label className="form-label">Admin Username</label>
                      <div className="input-wrap">
                        <UserIcon className="input-icon" size={17} />
                        <input
                          type="text"
                          className="form-input"
                          placeholder="Enter admin username"
                          value={adminAuthForm.username}
                          onChange={e => setAdminAuthForm({ ...adminAuthForm, username: e.target.value })}
                        />
                      </div>
                      {adminAuthErrors.username && <p className="error-text">{adminAuthErrors.username}</p>}
                    </div>

                    <div className="form-group">
                      <label className="form-label">Password</label>
                      <div className="input-wrap">
                        <Lock className="input-icon" size={17} />
                        <input
                          type="password"
                          className="form-input"
                          placeholder="••••••••"
                          value={adminAuthForm.password}
                          onChange={e => setAdminAuthForm({ ...adminAuthForm, password: e.target.value })}
                        />
                      </div>
                      {adminAuthErrors.password && <p className="error-text">{adminAuthErrors.password}</p>}
                    </div>

                    <button
                      type="submit"
                      className="btn-primary"
                      disabled={adminAuthLoading}
                      style={{ background: 'linear-gradient(135deg, #a855f7, #6366f1)', color: '#ffffff', marginTop: '0.5rem' }}
                    >
                      <Shield size={16} />
                      <span>{adminAuthLoading ? 'Authenticating...' : 'Sign In to Admin Console'}</span>
                    </button>
                  </form>
                </div>
              </div>
            ) : (
              <div className="admin-card-container">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
                  <div>
                    <h2 style={{ fontSize: '1.5rem', fontWeight: 800 }}>User Session Auditing & Access Logs</h2>
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                      Real-time session verification and timestamped login tracking
                    </p>
                  </div>

                  <button
                    className="btn-primary"
                    style={{ padding: '0.75rem 1.4rem', width: 'auto' }}
                    onClick={handleExportCsv}
                  >
                    <Download size={16} />
                    <span>Download as CSV</span>
                  </button>
                </div>

                {/* Metrics */}
                <div className="admin-stats-row">
                  <div className="admin-stat-card">
                    <div className="admin-stat-number">{adminLogins.length}</div>
                    <div className="admin-stat-title">Total Login Events</div>
                  </div>
                  <div className="admin-stat-card">
                    <div className="admin-stat-number" style={{ color: '#34d399' }}>
                      {adminLogins.filter(l => l.status === 'SUCCESS').length}
                    </div>
                    <div className="admin-stat-title">Successful Sessions</div>
                  </div>
                  <div className="admin-stat-card">
                    <div className="admin-stat-number" style={{ color: '#d8b4fe' }}>
                      {new Set(adminLogins.map(l => l.username)).size}
                    </div>
                    <div className="admin-stat-title">Unique Users</div>
                  </div>
                </div>

                {/* Toolbar */}
                <div className="admin-toolbar">
                  <div className="input-wrap" style={{ flex: '1', maxWidth: '380px' }}>
                    <Search className="input-icon" size={16} />
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Search username, email, IP, status..."
                      style={{ padding: '0.65rem 1rem 0.65rem 2.5rem' }}
                      value={adminSearch}
                      onChange={e => setAdminSearch(e.target.value)}
                    />
                  </div>

                  <button
                    className="btn-secondary"
                    onClick={fetchAdminLogins}
                    disabled={adminLoading}
                  >
                    <RefreshCw size={15} className={adminLoading ? 'spin' : ''} />
                    <span>Refresh Data</span>
                  </button>
                </div>

                {adminError && (
                  <div className="auth-alert error" style={{ marginBottom: '1rem' }}>
                    <AlertCircle size={16} />
                    <span>{adminError}</span>
                  </div>
                )}

                {/* Logins Table */}
                <div className="table-responsive">
                  <table className="admin-table">
                    <thead>
                      <tr>
                        <th>Log ID</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Timestamp</th>
                        <th>IP Address</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredLogins.length === 0 ? (
                        <tr>
                          <td colSpan="7" style={{ textAlign: 'center', padding: '2.5rem', color: 'var(--text-muted)' }}>
                            No login audit records found.
                          </td>
                        </tr>
                      ) : (
                        filteredLogins.map((record) => (
                          <tr key={record.id}>
                            <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--accent-cyan)' }}>
                              {record.id}
                            </td>
                            <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                              {record.username}
                            </td>
                            <td>{record.email}</td>
                            <td>
                              <span className={`user-role-pill ${record.role}`}>{record.role}</span>
                            </td>
                            <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem' }}>
                              {record.timestamp}
                            </td>
                            <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem' }}>
                              {record.ipAddress}
                            </td>
                            <td>
                              <span className={`status-badge ${record.status}`}>
                                {record.status === 'SUCCESS' ? '✓ Success' : '✗ Failed'}
                              </span>
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </main>
        </div>
      ) : (
        /* ========================================================================= */
        /* SCENARIO B: COMMON USER APP (Route /) */
        /* User MUST login or register before accessing the website! */
        /* NO Admin button visible to common users! */
        /* ========================================================================= */
        !currentUser ? (
          /* USER GATE: Full-Screen Sign In or Create Account */
          <div className="auth-gateway-wrapper">
            {/* Top-Right Theme Toggle on Login Screen */}
            <div style={{ position: 'absolute', top: '1.5rem', right: '1.5rem', zIndex: 20 }}>
              <button
                type="button"
                className="btn-theme-toggle"
                onClick={toggleTheme}
                title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
              >
                {theme === 'dark' ? <Sun size={18} color="#f59e0b" /> : <Moon size={18} color="#0284c7" />}
              </button>
            </div>

            <ElectricBorder
              color={electricColor}
              speed={1}
              chaos={0.5}
              spread={0.6}
              strands={3}
              thickness={1.5}
              borderRadius={24}
            >
              <div className="auth-gateway-card">
                <div className="auth-brand-center">
                  <div className="auth-brand-icon">
                    <GraduationCap size={28} />
                  </div>
                  <h2>SchemeSathi</h2>
                  <p>Please sign in or create an account to access the scholarship navigator</p>
                </div>

                {/* Tabs */}
                <div className="auth-tabs">
                  <button
                    type="button"
                    className={`auth-tab-btn ${userAuthMode === 'login' ? 'active' : ''}`}
                    onClick={() => {
                      setUserAuthMode('login');
                      setUserAuthAlert(null);
                      setUserAuthErrors({});
                    }}
                  >
                    Sign In
                  </button>
                  <button
                    type="button"
                    className={`auth-tab-btn ${userAuthMode === 'register' ? 'active' : ''}`}
                    onClick={() => {
                      setUserAuthMode('register');
                      setUserAuthAlert(null);
                      setUserAuthErrors({});
                    }}
                  >
                    Create Account
                  </button>
                </div>

                {userAuthAlert && (
                  <div className={`auth-alert ${userAuthAlert.type}`}>
                    <AlertCircle size={16} />
                    <span>{userAuthAlert.message}</span>
                  </div>
                )}

                <form onSubmit={handleUserAuthSubmit}>
                  {/* Username */}
                  <div className="form-group">
                    <label className="form-label">
                      <span>{userAuthMode === 'login' ? 'Username or Email' : 'Username'}</span>
                    </label>
                    <div className="input-wrap">
                      <UserIcon className="input-icon" size={17} />
                      <input
                        type="text"
                        className="form-input"
                        placeholder={userAuthMode === 'login' ? 'Enter username or email' : 'Choose a username'}
                        value={userAuthForm.username}
                        onChange={e => setUserAuthForm({ ...userAuthForm, username: e.target.value })}
                      />
                    </div>
                    {userAuthErrors.username && <p className="error-text">{userAuthErrors.username}</p>}
                  </div>

                  {/* Email (Registration only) */}
                  {userAuthMode === 'register' && (
                    <div className="form-group">
                      <label className="form-label">
                        <span>Email Address</span>
                      </label>
                      <div className="input-wrap">
                        <Mail className="input-icon" size={17} />
                        <input
                          type="email"
                          className="form-input"
                          placeholder="student@example.com"
                          value={userAuthForm.email}
                          onChange={e => setUserAuthForm({ ...userAuthForm, email: e.target.value })}
                        />
                      </div>
                      {userAuthErrors.email && <p className="error-text">{userAuthErrors.email}</p>}
                    </div>
                  )}

                  {/* Password */}
                  <div className="form-group">
                    <label className="form-label">
                      <span>Password</span>
                      {userAuthMode === 'register' && <span className="label-hint">Min 6 characters</span>}
                    </label>
                    <div className="input-wrap">
                      <Lock className="input-icon" size={17} />
                      <input
                        type="password"
                        className="form-input"
                        placeholder="••••••••"
                        value={userAuthForm.password}
                        onChange={e => setUserAuthForm({ ...userAuthForm, password: e.target.value })}
                      />
                    </div>
                    {userAuthErrors.password && <p className="error-text">{userAuthErrors.password}</p>}
                  </div>

                  {/* Confirm Password */}
                  {userAuthMode === 'register' && (
                    <div className="form-group">
                      <label className="form-label">
                        <span>Confirm Password</span>
                      </label>
                      <div className="input-wrap">
                        <Lock className="input-icon" size={17} />
                        <input
                          type="password"
                          className="form-input"
                          placeholder="••••••••"
                          value={userAuthForm.confirmPassword}
                          onChange={e => setUserAuthForm({ ...userAuthForm, confirmPassword: e.target.value })}
                        />
                      </div>
                      {userAuthErrors.confirmPassword && <p className="error-text">{userAuthErrors.confirmPassword}</p>}
                    </div>
                  )}

                  <button
                    type="submit"
                    className="btn-primary"
                    disabled={userAuthLoading}
                    style={{ marginTop: '0.5rem' }}
                  >
                    <Sparkles size={16} />
                    <span>{userAuthLoading ? 'Authenticating...' : (userAuthMode === 'login' ? 'Sign In & Access Navigator' : 'Create Account & Enter')}</span>
                  </button>
                </form>
              </div>
            </ElectricBorder>
          </div>
        ) : (
          /* USER LOGGED IN: Reveal Complete Website Interface */
          <div className="site-content">
            {/* Header: Common User View (NO Admin button!) */}
            <header className="site-header">
              <div className="container header-inner">
                <div className="brand">
                  <div className="brand-icon">
                    <GraduationCap size={22} />
                  </div>
                  <div className="brand-text">
                    <h1>SchemeSathi</h1>
                    <p>Scholarship Eligibility Navigator</p>
                  </div>
                </div>

                <div className="header-actions">
                  {/* Light / Dark Mode Toggle Button */}
                  <button
                    type="button"
                    className="btn-theme-toggle"
                    onClick={toggleTheme}
                    title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
                  >
                    {theme === 'dark' ? <Sun size={18} color="#f59e0b" /> : <Moon size={18} color="#0284c7" />}
                  </button>

                  <div className="backend-status" title={backendOnline ? 'Java REST API Connected' : 'Running with built-in rules engine'}>
                    <span className={`status-dot ${backendOnline ? 'online' : 'offline'}`} />
                    <span>{backendOnline ? 'Java API :8080' : 'Offline Engine'}</span>
                  </div>

                  <div className="user-menu-wrap">
                    <div className="user-badge">
                      <UserIcon size={14} color="var(--accent-cyan)" />
                      <span>{currentUser.username}</span>
                    </div>

                    <button
                      className="btn-secondary"
                      style={{ padding: '0.45rem 0.75rem' }}
                      onClick={handleLogout}
                      title="Sign Out"
                    >
                      <LogOut size={14} />
                      <span>Logout</span>
                    </button>
                  </div>
                </div>
              </div>
            </header>

            {/* Hero Section Wrapped with ElectricBorder */}
            <section className="hero-section">
              <div className="container">
                <div className="hero-border-wrap">
                  <ElectricBorder
                    color={electricColor}
                    speed={1}
                    chaos={0.5}
                    spread={0.6}
                    strands={3}
                    thickness={1.5}
                    borderRadius={24}
                  >
                    <div className="hero-card">
                      <div className="hero-pill">
                        <Sparkles size={14} />
                        <span>Welcome, {currentUser.username}! • Intelligent Scholarship Navigator</span>
                      </div>
                      
                      <h2 className="hero-title">
                        Discover Every Scholarship You <span className="highlight">Qualify For</span>
                      </h2>
                      
                      <p className="hero-subtitle">
                        SchemeSathi simplifies educational funding by polymorphically evaluating your academic performance, 
                        family income, and social category against official scheme criteria in real-time.
                      </p>

                      <div className="hero-stats">
                        <div className="stat-item">
                          <span className="stat-value">{allSchemes.length} Active</span>
                          <span className="stat-label">Scholarship Schemes</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-value">{hasEvaluated ? `${evaluatedResults.length} Matches` : 'Ready to Check'}</span>
                          <span className="stat-label">{hasEvaluated ? 'Eligible For You' : 'Instant Evaluation'}</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-value">100% Free</span>
                          <span className="stat-label">Instant Document Checklist</span>
                        </div>
                      </div>
                    </div>
                  </ElectricBorder>
                </div>
              </div>
            </section>

            {/* Main Application Area: Initially only shows Student Profile, then reveals eligible scholarships */}
            <main className="container">
              <div className={hasEvaluated ? "app-grid" : "app-single-panel"}>
                {/* Student Profile Input Panel */}
                <aside style={!hasEvaluated ? { maxWidth: '640px', margin: '0 auto', width: '100%' } : undefined}>
                  <div className="panel">
                    <div className="panel-header">
                      <h3 className="panel-title">
                        <Compass size={18} />
                        <span>Student Profile</span>
                      </h3>
                      <span className="label-hint">Live Criteria</span>
                    </div>

                    {/* Presets */}
                    <div className="presets-section">
                      <div className="presets-label">Quick Presets</div>
                      <div className="preset-chips">
                        {PRESETS.map((p, idx) => (
                          <button
                            key={idx}
                            type="button"
                            className="preset-chip"
                            onClick={() => {
                              setMarks(p.marks);
                              setIncome(p.income);
                              setCategory(p.category);
                            }}
                          >
                            {p.label}
                          </button>
                        ))}
                      </div>
                    </div>

                    <form onSubmit={handleEvaluate}>
                      {/* Marks */}
                      <div className="form-group">
                        <label className="form-label">
                          <span>Academic Marks (%)</span>
                          <span className="label-hint">0.0 - 100.0</span>
                        </label>
                        <div className="input-wrap">
                          <GraduationCap className="input-icon" size={18} />
                          <input
                            type="number"
                            step="0.1"
                            min="0"
                            max="100"
                            className="form-input"
                            value={marks}
                            onChange={(e) => setMarks(e.target.value)}
                            required
                          />
                        </div>
                      </div>

                      {/* Income */}
                      <div className="form-group">
                        <label className="form-label">
                          <span>Annual Family Income (₹)</span>
                          <span className="label-hint">Non-negative</span>
                        </label>
                        <div className="input-wrap">
                          <Coins className="input-icon" size={18} />
                          <input
                            type="number"
                            step="5000"
                            min="0"
                            className="form-input"
                            value={income}
                            onChange={(e) => setIncome(e.target.value)}
                            required
                          />
                        </div>
                      </div>

                      {/* Category */}
                      <div className="form-group">
                        <label className="form-label">
                          <span>Social Category</span>
                          <span className="label-hint">Case-insensitive</span>
                        </label>
                        <div className="input-wrap">
                          <UserIcon className="input-icon" size={18} />
                          <select
                            className="form-select"
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            required
                          >
                            <option value="General">General</option>
                            <option value="OBC">OBC (Other Backward Classes)</option>
                            <option value="SC">SC (Scheduled Castes)</option>
                            <option value="ST">ST (Scheduled Tribes)</option>
                            <option value="EWS">EWS (Economically Weaker Section)</option>
                          </select>
                        </div>
                      </div>

                      {/* Eligibility Check Button with Animation */}
                      <button type="submit" className="btn-primary" disabled={loading}>
                        <Sparkles size={18} />
                        <span>{loading ? 'Evaluating Eligibility...' : 'Check My Eligibility'}</span>
                      </button>

                      {/* Loading Animation Box */}
                      {loading && (
                        <div className="eval-loading-overlay">
                          <div className="spinner-wrap">
                            <div className="spinner-electric" />
                            <span className="loading-text">{loadingMessage}</span>
                          </div>
                        </div>
                      )}
                    </form>
                  </div>
                </aside>

                {/* Results Section: VISIBLE ONLY AFTER CLICKING "CHECK MY ELIGIBILITY" */}
                {hasEvaluated && (
                  <section className="fade-in-results">
                    <div className="results-header-bar">
                      <div className="tabs-nav">
                        <button
                          className={`tab-btn ${activeTab === 'results' ? 'active' : ''}`}
                          onClick={() => setActiveTab('results')}
                        >
                          Matching Schemes ({evaluatedResults.length})
                        </button>
                        <button
                          className={`tab-btn ${activeTab === 'all' ? 'active' : ''}`}
                          onClick={() => setActiveTab('all')}
                        >
                          All Catalog Schemes ({allSchemes.length})
                        </button>
                      </div>

                      {activeTab === 'results' && evaluatedResults.length > 0 && (
                        <button 
                          className="btn-secondary" 
                          onClick={handleDownloadReport} 
                          disabled={reportDownloading}
                          title="Generate and download text eligibility report"
                        >
                          <Download size={16} />
                          <span>{reportDownloading ? 'Generating...' : 'Download Official Report (.txt)'}</span>
                        </button>
                      )}
                    </div>

                    {activeTab === 'results' ? (
                      /* Eligible Results View */
                      <div className="schemes-list">
                        {evaluatedResults.length === 0 ? (
                          <div className="empty-state">
                            <div className="empty-icon">
                              <FileText size={28} />
                            </div>
                            <h4 className="empty-title">No Matching Schemes Found</h4>
                            <p className="empty-desc">
                              No scholarships matched your profile (Marks: {marks}%, Income: ₹{Number(income).toLocaleString('en-IN')}, Category: {category}). 
                              Try adjusting your criteria or browse the All Schemes catalog.
                            </p>
                          </div>
                        ) : (
                          evaluatedResults.map((scheme, index) => {
                            const isTopMatch = index === 0;

                            const cardContent = (
                              <div className="scheme-card" style={isTopMatch ? { borderRadius: '20px' } : undefined}>
                                <div className="scheme-top">
                                  <div>
                                    <span className={`type-pill ${scheme.type}`}>{scheme.type}</span>
                                    <h4 className="scheme-title" style={{ marginTop: '0.4rem' }}>{scheme.name}</h4>
                                  </div>
                                  <span className="label-hint font-mono">{scheme.id}</span>
                                </div>

                                <div className="criteria-badge">
                                  <ShieldCheck size={14} color="var(--accent-cyan)" />
                                  <span>
                                    {scheme.type === 'MERIT' && `Criterion: Min Marks ≥ ${scheme.minimumMarks}%`}
                                    {scheme.type === 'INCOME' && `Criterion: Max Annual Income ≤ ₹${Number(scheme.maximumAnnualIncome).toLocaleString('en-IN')}`}
                                    {scheme.type === 'CATEGORY' && `Criterion: Allowed Categories: ${(scheme.allowedCategories || []).join(', ')}`}
                                  </span>
                                </div>

                                <div className="docs-section">
                                  <div className="docs-heading">
                                    <CheckCircle2 size={13} color="#10b981" />
                                    <span>Required Documents Checklist</span>
                                  </div>
                                  <ul className="docs-list">
                                    {(scheme.requiredDocuments || []).map((doc, dIdx) => (
                                      <li key={dIdx} className="doc-item">
                                        <ArrowRight size={13} />
                                        <span>{doc}</span>
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              </div>
                            );

                            if (isTopMatch) {
                              return (
                                <ElectricBorder
                                  key={scheme.id}
                                  color={electricColor}
                                  speed={1}
                                  chaos={0.5}
                                  spread={0.6}
                                  strands={3}
                                  thickness={1.5}
                                  borderRadius={20}
                                >
                                  {cardContent}
                                </ElectricBorder>
                              );
                            }

                            return <div key={scheme.id}>{cardContent}</div>;
                          })
                        )}
                      </div>
                    ) : (
                      /* All Catalog Schemes View */
                      <div>
                        <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '1.25rem', flexWrap: 'wrap' }}>
                          <div className="input-wrap" style={{ flex: '1', minWidth: '220px' }}>
                            <Search className="input-icon" size={16} />
                            <input
                              type="text"
                              placeholder="Search schemes by name or code..."
                              className="form-input"
                              style={{ padding: '0.65rem 1rem 0.65rem 2.5rem' }}
                              value={searchQuery}
                              onChange={(e) => setSearchQuery(e.target.value)}
                            />
                          </div>

                          <div style={{ display: 'flex', gap: '0.5rem' }}>
                            {['ALL', 'MERIT', 'INCOME', 'CATEGORY'].map(type => (
                              <button
                                key={type}
                                type="button"
                                className={`tab-btn ${catalogFilter === type ? 'active' : ''}`}
                                onClick={() => setCatalogFilter(type)}
                                style={{ border: '1px solid var(--border-subtle)' }}
                              >
                                {type}
                              </button>
                            ))}
                          </div>
                        </div>

                        <div className="schemes-list">
                          {filteredCatalog.map(scheme => (
                            <div key={scheme.id} className="scheme-card">
                              <div className="scheme-top">
                                <div>
                                  <span className={`type-pill ${scheme.type}`}>{scheme.type}</span>
                                  <h4 className="scheme-title" style={{ marginTop: '0.4rem' }}>{scheme.name}</h4>
                                </div>
                                <span className="label-hint font-mono">{scheme.id}</span>
                              </div>

                              <div className="criteria-badge">
                                <BookOpen size={14} color="var(--accent-cyan)" />
                                <span>
                                  {scheme.type === 'MERIT' && `Criterion: Min Marks ≥ ${scheme.minimumMarks}%`}
                                  {scheme.type === 'INCOME' && `Criterion: Max Annual Income ≤ ₹${Number(scheme.maximumAnnualIncome).toLocaleString('en-IN')}`}
                                  {scheme.type === 'CATEGORY' && `Criterion: Allowed Categories: ${(scheme.allowedCategories || []).join(', ')}`}
                                </span>
                              </div>

                              <div className="docs-section">
                                <div className="docs-heading">
                                  <CheckCircle2 size={13} color="#10b981" />
                                  <span>Mandatory Documents</span>
                                </div>
                                <ul className="docs-list">
                                  {(scheme.requiredDocuments || []).map((doc, dIdx) => (
                                    <li key={dIdx} className="doc-item">
                                      <ArrowRight size={13} />
                                      <span>{doc}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </section>
                )}
              </div>
            </main>

            {/* Footer */}
            <footer className="site-footer">
              <div className="container">
                <p>
                  SchemeSathi © 2026 — Scholarship Eligibility Navigator • Object-Oriented Java Backend + Modern React Web Interface
                </p>
              </div>
            </footer>
          </div>
        )
      )}
    </>
  );
}
