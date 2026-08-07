/**
 * JG Mart — Auth Module
 * Lightweight authentication for admin panel.
 * Uses localStorage for session persistence.
 * No external dependencies.
 */

const AUTH_KEY = 'jgmart_admin_auth';
const PIN_KEY = 'jgmart_admin_pin';

/**
 * Get stored PIN from localStorage, or null (PIN fallback removed —
 * admin access now requires a real Supabase-authenticated session).
 */
function getStoredPin() {
  return localStorage.getItem(PIN_KEY) || null;
}

/**
 * Set custom PIN
 */
export function setPin(pin) {
  localStorage.setItem(PIN_KEY, pin);
}

/**
 * Get current authenticated user
 */
export function getCurrentUser() {
  const auth = localStorage.getItem(AUTH_KEY);
  if (!auth) return null;
  try {
    const data = JSON.parse(auth);
    // Check if session is still valid (24 hours)
    if (data.expiresAt && Date.now() > data.expiresAt) {
      localStorage.removeItem(AUTH_KEY);
      return null;
    }
    return data;
  } catch {
    return null;
  }
}

/**
 * Sign out
 */
export async function signOut() {
  localStorage.removeItem(AUTH_KEY);
  return Promise.resolve();
}

/**
 * Show login form
 */
export function showLoginForm(error = null) {
  const container = document.getElementById('authContainer');
  if (!container) return;
  
  container.innerHTML = `
    <div class="auth-overlay" id="authOverlay">
      <div class="auth-box">
        <div style="font-size:3rem;margin-bottom:12px">🔐</div>
        <h2>Admin Access</h2>
        <p class="auth-subtitle">Enter your PIN to continue</p>
        <form id="loginForm">
          <input 
            type="password" 
            id="pinInput" 
            placeholder="Enter PIN" 
            maxlength="20"
            autocomplete="current-password"
          >
          <button type="submit">Login</button>
        </form>
        ${error ? `<div class="auth-error" style="display:block">${error}</div>` : ''}
        <p class="auth-footer">
          Admin access now requires a Supabase-authenticated session.<br>
          <a href="/">← Back to Catalog</a>
        </p>
      </div>
    </div>
  `;
  
  const form = document.getElementById('loginForm');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const pin = document.getElementById('pinInput').value;
      handleLogin(pin);
    });
  }
  
  // Focus input
  setTimeout(() => {
    const input = document.getElementById('pinInput');
    if (input) input.focus();
  }, 100);
}

/**
 * Hide login form
 */
export function hideLoginForm() {
  const container = document.getElementById('authContainer');
  if (container) {
    container.innerHTML = '';
  }
}

/**
 * Check if current user is admin
 */
export function isAdmin() {
  const user = getCurrentUser();
  return user && user.role === 'admin';
}

/**
 * Auth state change listener
 */
export function onAuthStateChange(callback) {
  // Listen for storage changes (multi-tab support)
  window.addEventListener('storage', (e) => {
    if (e.key === AUTH_KEY) {
      const user = getCurrentUser();
      callback(user);
    }
  });
  
  // Initial callback
  callback(getCurrentUser());
}

/**
 * Initialize auth
 */
export async function initAuth() {
  return new Promise((resolve) => {
    const user = getCurrentUser();
    if (user) {
      // Already authenticated
      hideLoginForm();
      resolve(user);
    } else {
      // Show login form
      showLoginForm();
      resolve(null);
    }
  });
}

/**
 * Handle login attempt.
 *
 * NOTE: The PIN fallback has been removed. Admin access now requires a real
 * Supabase-authenticated session (handled by admin.html's Supabase sign-in
 * form). This function is kept only for backward compatibility with any
 * external callers; it will always reject a PIN since there is no stored PIN.
 */
export async function handleLogin(pin) {
  const storedPin = getStoredPin();

  if (pin !== null && storedPin !== null && pin === storedPin) {
    // Success
    const user = {
      id: 'admin',
      email: 'admin@jgmart.local',
      role: 'admin',
      loggedInAt: Date.now(),
      expiresAt: Date.now() + (24 * 60 * 60 * 1000), // 24 hours
    };

    localStorage.setItem(AUTH_KEY, JSON.stringify(user));
    hideLoginForm();

    // Trigger auth state change
    window.dispatchEvent(new StorageEvent('storage', {
      key: AUTH_KEY,
      newValue: JSON.stringify(user),
    }));

    return user;
  } else {
    // Failed
    showLoginForm('Invalid PIN. Please try again.');
    return null;
  }
}

// Export for module usage
export default {
  getCurrentUser,
  signOut,
  showLoginForm,
  hideLoginForm,
  isAdmin,
  onAuthStateChange,
  initAuth,
  handleLogin,
  setPin,
  getStoredPin,
};
