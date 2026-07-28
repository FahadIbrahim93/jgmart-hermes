// JG Mart Dashboard Auth Module
// Usage: Add <script src="auth.js"></script> to any dashboard page
// Place this script BEFORE any other scripts in the page

const DEFAULT_PIN = '1234';
const STORAGE_KEY = 'jgmart_dashboard_pin';

function requireAuth() {
  const savedPin = localStorage.getItem(STORAGE_KEY);
  if (!savedPin) {
    showLoginOverlay();
    return false;
  }
  if (savedPin !== DEFAULT_PIN && savedPin !== getCurrentPin()) {
    localStorage.removeItem(STORAGE_KEY);
    showLoginOverlay();
    return false;
  }
  return true;
}

function getCurrentPin() {
  // Check admin.html for the current PIN
  return DEFAULT_PIN;
}

function showLoginOverlay() {
  const overlay = document.getElementById('loginOverlay');
  if (overlay) {
    overlay.classList.remove('hidden');
  } else {
    // Create overlay if it doesn't exist
    const div = document.createElement('div');
    div.id = 'loginOverlay';
    div.className = 'login-overlay';
    div.innerHTML = `
      <div class="login-box">
        <h2 class="text-2xl font-bold text-jg-900 mb-2">🔐 JG Mart</h2>
        <p class="text-sm text-gray-500 mb-4">Operations Dashboard</p>
        <input type="password" id="dashPin" maxlength="6" placeholder="Enter PIN" onkeydown="if(event.key==='Enter')dashLogin()">
        <button onclick="dashLogin()">Unlock Dashboard</button>
        <div class="error" id="dashError" style="color:#c0392b;font-size:0.85rem;margin-top:8px;display:none">Wrong PIN. Try again.</div>
        <p class="text-xs text-gray-400 mt-4">Default PIN: <code class="bg-gray-100 px-2 py-1 rounded">1234</code></p>
      </div>
    `;
    document.body.prepend(div);
  }
  // Hide main content
  const main = document.getElementById('dashboardMain');
  if (main) main.classList.add('hidden');
}

function dashLogin() {
  const pin = document.getElementById('dashPin').value;
  if (pin === DEFAULT_PIN || pin === getCurrentPin()) {
    localStorage.setItem(STORAGE_KEY, pin);
    const overlay = document.getElementById('loginOverlay');
    if (overlay) overlay.classList.add('hidden');
    const main = document.getElementById('dashboardMain');
    if (main) main.classList.remove('hidden');
    if (typeof initDashboard === 'function') initDashboard();
  } else {
    const error = document.getElementById('dashError');
    if (error) {
      error.style.display = 'block';
      setTimeout(() => error.style.display = 'none', 2000);
    }
  }
}

function dashLogout() {
  localStorage.removeItem(STORAGE_KEY);
  location.reload();
}

// Auto-check on load
if (!requireAuth()) {
  console.log('Dashboard locked - PIN required');
}
