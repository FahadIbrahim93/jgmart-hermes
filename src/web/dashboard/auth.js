/**
 * JG Mart — Dashboard Auth Module
 *
 * Secure authentication using Supabase (email/password).
 * Includes graceful fallback if Supabase is not yet configured.
 *
 * Usage: Add <script src="auth.js"></script> to any dashboard page
 * Place this script BEFORE any other scripts in the page.
 */

// ────────────────────────────────────────────────────────────
// SUPABASE CONFIG (mirrors src/web/supabase/config.js)
// In production, set these via localStorage or .env injection.
// ────────────────────────────────────────────────────────────
const __SUPABASE_URL = localStorage.getItem('jgmart_supabase_url') || 'https://your-project-id.supabase.co';
const __SUPABASE_ANON_KEY = localStorage.getItem('jgmart_supabase_anon_key') || 'your-anon-key';
const __IS_CONFIGURED = __SUPABASE_URL !== 'https://your-project-id.supabase.co';
const __SESSION_KEY = 'jgmart_session';

// ────────────────────────────────────────────────────────────
// MINIMAL SUPABASE AUTH CLIENT
// ────────────────────────────────────────────────────────────
const __supabase = {
  url: __SUPABASE_URL.replace(/\/$/, ''),
  key: __SUPABASE_ANON_KEY,

  async signIn(email, password) {
    const res = await fetch(`${this.url}/auth/v1/token?grant_type=password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'apikey': this.key },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.msg || data.error_description || 'Login failed');
    localStorage.setItem(__SESSION_KEY, JSON.stringify(data));
    return data;
  },

  async signOut() {
    const str = localStorage.getItem(__SESSION_KEY);
    if (str) {
      try {
        const { access_token } = JSON.parse(str);
        await fetch(`${this.url}/auth/v1/logout`, {
          method: 'POST',
          headers: { 'apikey': this.key, 'Authorization': `Bearer ${access_token}` }
        });
      } catch (_) { /* ignore logout errors */ }
    }
    localStorage.removeItem(__SESSION_KEY);
  },

  getSession() {
    const str = localStorage.getItem(__SESSION_KEY);
    if (!str) return null;
    try {
      const s = JSON.parse(str);
      if (s.expires_at && Date.now() / 1000 > s.expires_at) {
        localStorage.removeItem(__SESSION_KEY);
        return null;
      }
      return s;
    } catch { return null; }
  }
};

// ────────────────────────────────────────────────────────────
// PUBLIC API
// ────────────────────────────────────────────────────────────

/**
 * Check if user is authenticated.
 * Returns true if valid session exists, otherwise shows login overlay and returns false.
 */
function requireAuth() {
  const session = __supabase.getSession();
  if (session) return true;
  showLoginOverlay();
  return false;
}

/**
 * Handle login form submission.
 * Called by the login overlay button / Enter key.
 */
async function dashLogin() {
  const email = document.getElementById('dashEmail').value.trim();
  const password = document.getElementById('dashPassword').value;
  const errorEl = document.getElementById('dashError');
  const submitBtn = document.getElementById('dashLoginBtn');

  // Reset error
  if (errorEl) { errorEl.style.display = 'none'; errorEl.textContent = ''; }

  // Validate
  if (!email) { showError('Please enter your email'); return; }
  if (!password) { showError('Please enter your password'); return; }

  // Loading state
  if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = '⏳ Signing in...'; }

  try {
    if (__IS_CONFIGURED) {
      await __supabase.signIn(email, password);
    } else {
      // Demo mode: accept any email/password for testing
      // In production, this branch only runs when Supabase isn't configured
      const demoSession = {
        access_token: 'demo-token-' + Date.now(),
        token_type: 'bearer',
        expires_in: 86400,
        expires_at: Math.floor(Date.now() / 1000) + 86400,
        user: {
          id: 'demo-user',
          email: email,
          user_metadata: { role: 'admin', full_name: email.split('@')[0] }
        }
      };
      localStorage.setItem(__SESSION_KEY, JSON.stringify(demoSession));
    }

    // Success — hide overlay, show dashboard
    const overlay = document.getElementById('loginOverlay');
    if (overlay) overlay.classList.add('hidden');
    const main = document.getElementById('dashboardMain');
    if (main) main.classList.remove('hidden');

    // Trigger dashboard init if available
    if (typeof initDashboard === 'function') initDashboard();

  } catch (err) {
    showError(err.message || 'Login failed. Check your credentials.');
    if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Sign In'; }
  }
}

/**
 * Log out and reload the page.
 */
async function dashLogout() {
  await __supabase.signOut();
  location.reload();
}

/**
 * Forgot password — opens a flow in the overlay.
 */
function dashForgotPassword() {
  const overlay = document.getElementById('loginOverlay');
  if (!overlay) return;

  const box = overlay.querySelector('.login-box');
  if (!box) return;

  box.innerHTML = `
    <div style="text-align:left">
      <button onclick="dashBackToLogin()" style="background:none;border:none;color:#00442D;font-size:.82rem;cursor:pointer;font-family:inherit;margin-bottom:12px;display:flex;align-items:center;gap:4px">
        ← Back to Sign In
      </button>
      <h2 style="font-size:1.1rem;font-weight:700;color:#1a1a1a;margin-bottom:4px">🔑 Reset Password</h2>
      <p style="font-size:.78rem;color:#5c5c5c;margin-bottom:16px">Enter your email and we'll send you a reset link.</p>
      <input type="email" id="dashResetEmail" placeholder="Your email" style="width:100%;padding:11px 14px;border:1.5px solid #ddd;border-radius:8px;font-size:.85rem;font-family:inherit;margin-bottom:12px;outline:none" onfocus="this.style.borderColor='#00442D'" onblur="this.style.borderColor='#ddd'">
      <button onclick="dashSendReset()" style="width:100%;background:#00442D;color:#fff;border:none;padding:11px;border-radius:8px;font-weight:600;font-size:.85rem;cursor:pointer;font-family:inherit">Send Reset Link</button>
      <div id="dashResetError" style="color:#c0392b;font-size:.78rem;margin-top:8px;display:none"></div>
      <div id="dashResetSuccess" style="color:#0a6b47;font-size:.78rem;margin-top:8px;display:none"></div>
    </div>
  `;
}

async function dashSendReset() {
  const email = document.getElementById('dashResetEmail').value.trim();
  const errorEl = document.getElementById('dashResetError');
  const successEl = document.getElementById('dashResetSuccess');

  if (errorEl) errorEl.style.display = 'none';
  if (successEl) successEl.style.display = 'none';

  if (!email) {
    if (errorEl) { errorEl.textContent = 'Please enter your email'; errorEl.style.display = 'block'; }
    return;
  }

  try {
    const res = await fetch(`${__supabase.url}/auth/v1/recover?grant_type=password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'apikey': __supabase.key },
      body: JSON.stringify({ email })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.msg || data.error_description || 'Reset failed');
    if (successEl) { successEl.textContent = '✅ Reset link sent! Check your email.'; successEl.style.display = 'block'; }
  } catch (err) {
    if (errorEl) { errorEl.textContent = err.message; errorEl.style.display = 'block'; }
  }
}

function dashBackToLogin() {
  const overlay = document.getElementById('loginOverlay');
  if (overlay) overlay.remove();
  showLoginOverlay();
}

// ────────────────────────────────────────────────────────────
// LOGIN OVERLAY UI
// ────────────────────────────────────────────────────────────

function showLoginOverlay() {
  // Remove existing overlay if present
  const existing = document.getElementById('loginOverlay');
  if (existing) existing.remove();

  const overlay = document.createElement('div');
  overlay.id = 'loginOverlay';
  overlay.innerHTML = `
    <div class="login-overlay" style="position:fixed;inset:0;background:rgba(0,0,0,0.55);backdrop-filter:blur(6px);display:flex;align-items:center;justify-content:center;z-index:9999;padding:16px">
      <div class="login-box" style="background:#fff;border-radius:18px;padding:32px 28px 28px;width:100%;max-width:380px;box-shadow:0 24px 80px rgba(0,0,0,0.25);animation:loginIn 0.3s ease">
        <style>
          @keyframes loginIn{from{opacity:0;transform:scale(0.92) translateY(12px)}to{opacity:1;transform:scale(1) translateY(0)}}
          @keyframes loginShake{0%,100%{transform:translateX(0)}20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(4px)}}
          .login-box input:focus{border-color:#00442D!important;box-shadow:0 0 0 3px rgba(0,68,45,0.1)}
          .login-box .shake{animation:loginShake 0.35s ease}
        </style>

        <!-- Logo -->
        <div style="text-align:center;margin-bottom:20px">
          <div style="width:48px;height:48px;background:#00442D;border-radius:14px;display:inline-flex;align-items:center;justify-content:center;font-size:1.5rem;margin-bottom:8px;box-shadow:0 4px 12px rgba(0,68,45,0.2)">🌿</div>
          <h1 style="font-size:1.2rem;font-weight:800;color:#1a1a1a;margin:0">JG <span style="color:#c9a227">Mart</span></h1>
          <p style="font-size:.78rem;color:#5c5c5c;margin:2px 0 0">Operations Dashboard</p>
        </div>

        <!-- Login Form -->
        <form id="dashLoginForm" onsubmit="event.preventDefault();dashLogin()" style="margin-bottom:4px">
          <div style="margin-bottom:14px">
            <label for="dashEmail" style="font-size:.72rem;font-weight:600;color:#00442D;display:block;margin-bottom:4px">Email</label>
            <input type="email" id="dashEmail" placeholder="admin@jgmart.com" autocomplete="email" value="${__IS_CONFIGURED ? '' : 'demo@jgmart.com'}"
              style="width:100%;padding:11px 14px;border:1.5px solid #ddd;border-radius:10px;font-size:.85rem;font-family:inherit;outline:none;transition:border-color 0.15s">
          </div>
          <div style="margin-bottom:18px">
            <label for="dashPassword" style="font-size:.72rem;font-weight:600;color:#00442D;display:block;margin-bottom:4px">Password</label>
            <input type="password" id="dashPassword" placeholder="••••••••" autocomplete="current-password" value="${__IS_CONFIGURED ? '' : 'demo1234'}"
              style="width:100%;padding:11px 14px;border:1.5px solid #ddd;border-radius:10px;font-size:.85rem;font-family:inherit;outline:none;transition:border-color 0.15s">
          </div>
          <button type="submit" id="dashLoginBtn"
            style="width:100%;background:#00442D;color:#fff;border:none;padding:12px;border-radius:10px;font-weight:700;font-size:.88rem;cursor:pointer;font-family:inherit;transition:all 0.15s;display:flex;align-items:center;justify-content:center;gap:6px"
            onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'" onmousedown="this.style.transform='scale(0.97)'" onmouseup="this.style.transform='scale(1)'">
            Sign In
          </button>
          <div id="dashError" style="color:#c0392b;font-size:.78rem;margin-top:10px;display:none;text-align:center"></div>
        </form>

        <!-- Footer links -->
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:14px">
          <button type="button" onclick="dashForgotPassword()" style="background:none;border:none;color:#5c5c5c;font-size:.75rem;cursor:pointer;font-family:inherit;text-decoration:underline;text-underline-offset:2px">Forgot password?</button>
          ${!__IS_CONFIGURED ? '<span style="font-size:.65rem;color:#c9a227;background:#fff8e1;padding:3px 8px;border-radius:999px">⚡ Demo mode</span>' : ''}
        </div>
        ${!__IS_CONFIGURED ? '<p style="font-size:.68rem;color:#aaa;text-align:center;margin-top:14px;border-top:1px solid #f0f0f0;padding-top:12px">Configure Supabase in config.js to enable real auth.</p>' : ''}
      </div>
    </div>
  `;
  document.body.prepend(overlay);

  // Hide main content
  const main = document.getElementById('dashboardMain');
  if (main) main.classList.add('hidden');

  // Focus email field
  setTimeout(() => {
    const emailField = document.getElementById('dashEmail');
    if (emailField) emailField.focus();
  }, 100);
}

// ────────────────────────────────────────────────────────────
// HELPERS
// ────────────────────────────────────────────────────────────

function showError(msg) {
  const el = document.getElementById('dashError');
  if (!el) return;
  el.textContent = msg;
  el.style.display = 'block';
  // Shake animation
  const box = el.closest('.login-box');
  if (box) {
    box.classList.remove('shake');
    void box.offsetWidth; // trigger reflow
    box.classList.add('shake');
    setTimeout(() => box.classList.remove('shake'), 400);
  }
}

// ────────────────────────────────────────────────────────────
// INIT — check session on page load
// Wait for DOM to be ready since we access document.getElementById
// ────────────────────────────────────────────────────────────
(function init() {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
    return;
  }

  const session = __supabase.getSession();
  if (session) {
    // Session exists — show dashboard content
    const main = document.getElementById('dashboardMain');
    if (main) main.classList.remove('hidden');
    // Trigger dashboard init after a tick (allows page scripts to define initDashboard)
    setTimeout(() => {
      if (typeof initDashboard === 'function') initDashboard();
    }, 50);
  } else {
    // No session — show login
    showLoginOverlay();
  }
})();
