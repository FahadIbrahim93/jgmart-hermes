/**
 * JG Mart — Authentication Module
 *
 * Unified auth for admin panel and dashboard.
 * Uses Supabase for authentication with localStorage fallback for offline mode.
 */

import { supabase } from '../supabase/client.js';

const SESSION_KEY = 'jgmart_session';
const PIN_KEY = 'jgmart_auth_pin';

// ============================================
// AUTH STATE
// ============================================
let currentUser = null;
let authListeners = [];

// ============================================
// AUTH LISTENERS
// ============================================
function onAuthStateChange(callback) {
  authListeners.push(callback);
  return () => {
    authListeners = authListeners.filter(l => l !== callback);
  };
}

function notifyAuthListeners(user) {
  authListeners.forEach(cb => {
    try { cb(user); } catch (e) { console.error('Auth listener error:', e); }
  });
}

// ============================================
// SUPABASE AUTH
// ============================================
export async function signUp(email, password, metadata = {}) {
  try {
    const { data, error } = await supabase.signUp(email, password, {
      full_name: metadata.full_name || '',
      role: metadata.role || 'customer'
    });

    if (error) throw error;

    currentUser = data.user;
    notifyAuthListeners(currentUser);

    return { success: true, user: data.user };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

export async function signIn(email, password) {
  try {
    const { data, error } = await supabase.signIn(email, password);

    if (error) throw error;

    currentUser = data.user;
    notifyAuthListeners(currentUser);

    return { success: true, user: data.user, session: data };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

export async function signOut() {
  try {
    await supabase.signOut();
    currentUser = null;
    notifyAuthListeners(null);

    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

export async function getCurrentUser() {
  if (currentUser) return currentUser;

  try {
    const session = await supabase.getSession();
    if (session?.user) {
      currentUser = session.user;
      return currentUser;
    }
  } catch (e) {
    console.error('Failed to get current user:', e);
  }

  return null;
}

export async function resetPassword(email) {
  try {
    const response = await fetch(
      `${supabase.url}/auth/v1/recover?grant_type=password`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': supabase.key
        },
        body: JSON.stringify({ email })
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.msg || data.error_description || 'Password reset failed');
    }

    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// ============================================
// PIN AUTH (fallback for offline mode)
// ============================================
export function checkPinAuth(role = 'admin') {
  const session = localStorage.getItem(SESSION_KEY);
  if (!session) return false;

  try {
    const data = JSON.parse(session);
    if (data.role !== role && data.role !== 'admin') return false;
    return data.expires_at ? Date.now() < data.expires_at : true;
  } catch {
    return false;
  }
}

export function setPinAuth(role = 'admin') {
  const session = {
    role,
    authenticated: true,
    expires_at: Date.now() + (24 * 60 * 60 * 1000) // 24 hours
  };
  localStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

export function clearPinAuth() {
  localStorage.removeItem(SESSION_KEY);
}

// ============================================
// ROLE CHECKING
// ============================================
export function hasRole(user, ...roles) {
  if (!user) return false;

  const userRole = user.role || user.user_metadata?.role || 'customer';
  return roles.includes(userRole) || roles.includes('*');
}

export function isAdmin(user) {
  return hasRole(user, 'admin');
}

export function isOperator(user) {
  return hasRole(user, 'admin', 'operator');
}

export function isPartner(user) {
  return hasRole(user, 'admin', 'operator', 'partner');
}

// ============================================
// PROTECTED ROUTES
// ============================================
export function requireAuth(redirectTo = '/login.html') {
  const session = localStorage.getItem(SESSION_KEY);
  if (!session) {
    window.location.href = redirectTo;
    return false;
  }

  try {
    const data = JSON.parse(session);
    if (data.expires_at && Date.now() > data.expires_at) {
      clearPinAuth();
      window.location.href = redirectTo;
      return false;
    }
  } catch {
    clearPinAuth();
    window.location.href = redirectTo;
    return false;
  }

  return true;
}

export function requireRole(role, redirectTo = '/unauthorized.html') {
  const session = localStorage.getItem(SESSION_KEY);
  if (!session) {
    window.location.href = '/login.html';
    return false;
  }

  try {
    const data = JSON.parse(session);
    if (data.role !== 'admin' && data.role !== role) {
      window.location.href = redirectTo;
      return false;
    }
  } catch {
    window.location.href = '/login.html';
    return false;
  }

  return true;
}

// ============================================
// AUTH UI HELPERS
// ============================================
export function showLoginForm(containerId, onSuccess) {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = `
    <div class="auth-overlay">
      <div class="auth-box">
        <h2>🔐 JG Mart</h2>
        <p class="auth-subtitle">Sign in to continue</p>

        <form id="authForm" onsubmit="return handleAuthSubmit(event)">
          <div id="authModeSwitcher" style="margin-bottom: 16px;">
            <button type="button" id="showLogin" class="auth-mode-btn active" onclick="switchAuthMode('login')">Sign In</button>
            <button type="button" id="showSignup" class="auth-mode-btn" onclick="switchAuthMode('signup')">Sign Up</button>
          </div>

          <div id="loginFields">
            <input type="email" id="authEmail" placeholder="Email" required autocomplete="email">
            <input type="password" id="authPassword" placeholder="Password" required autocomplete="current-password">
          </div>

          <div id="signupFields" style="display:none">
            <input type="text" id="authName" placeholder="Full Name">
            <input type="email" id="authEmail" placeholder="Email" required autocomplete="email">
            <input type="password" id="authPassword" placeholder="Password (min 6 chars)" required autocomplete="new-password">
            <select id="authRole">
              <option value="customer">Customer</option>
              <option value="partner">Partner</option>
            </select>
          </div>

          <button type="submit" id="authSubmitBtn">Sign In</button>
          <div id="authError" class="auth-error"></div>
        </form>

        <p class="auth-footer">
          <a href="/forgot-password.html">Forgot password?</a>
        </p>
      </div>
    </div>
  `;

  // Make functions globally accessible for onclick handlers
  window.switchAuthMode = (mode) => {
    const loginFields = document.getElementById('loginFields');
    const signupFields = document.getElementById('signupFields');
    const showLogin = document.getElementById('showLogin');
    const showSignup = document.getElementById('showSignup');
    const submitBtn = document.getElementById('authSubmitBtn');

    if (mode === 'login') {
      loginFields.style.display = 'block';
      signupFields.style.display = 'none';
      showLogin.classList.add('active');
      showSignup.classList.remove('active');
      submitBtn.textContent = 'Sign In';
    } else {
      loginFields.style.display = 'none';
      signupFields.style.display = 'block';
      showSignup.classList.add('active');
      showLogin.classList.remove('active');
      submitBtn.textContent = 'Create Account';
    }
  };

  window.handleAuthSubmit = async (e) => {
    e.preventDefault();

    const email = document.getElementById('authEmail').value;
    const password = document.getElementById('authPassword').value;
    const isSignup = document.getElementById('signupFields').style.display !== 'none';

    const errorEl = document.getElementById('authError');
    errorEl.style.display = 'none';

    try {
      let result;
      if (isSignup) {
        const name = document.getElementById('authName').value;
        const role = document.getElementById('authRole').value;
        result = await signUp(email, password, { full_name: name, role });
      } else {
        result = await signIn(email, password);
      }

      if (result.success) {
        container.innerHTML = '';
        if (onSuccess) onSuccess(result.user);
        return false;
      } else {
        errorEl.textContent = result.error;
        errorEl.style.display = 'block';
        return false;
      }
    } catch (error) {
      errorEl.textContent = error.message;
      errorEl.style.display = 'block';
      return false;
    }
  };
}

export function hideLoginForm(containerId) {
  const container = document.getElementById(containerId);
  if (container) {
    container.innerHTML = '';
  }
}

// ============================================
// INITIALIZATION
// ============================================
export async function initAuth() {
  // Try to restore session from Supabase
  const session = await supabase.getSession();
  if (session?.user) {
    currentUser = session.user;
    notifyAuthListeners(currentUser);
  }

  // Listen for auth changes
  // Note: In a real implementation, you'd use supabase.auth.onAuthStateChange()
}

// Auto-init if this module is loaded
if (typeof window !== 'undefined') {
  initAuth();
}
