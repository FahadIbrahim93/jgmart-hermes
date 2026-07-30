/**
 * Admin backend — Supabase Auth + CRUD when configured.
 * Loaded as ES module from admin.html.
 */
import { supabase } from '../supabase/client.js';
import { isSupabaseConfigured } from '../supabase/config.js';
import {
  loadProductsFromDB,
  loadOrdersFromDB,
  updateProductInDB,
  updateOrderStatusInDB
} from './db.js';

const ADMIN_SESSION_KEY = 'jgmart_admin_auth';

function mapDbProduct(row, index) {
  const legacyId = row.metadata?.legacy_id || `p${String(index + 1).padStart(2, '0')}`;
  return {
    id: legacyId,
    _uuid: row.id,
    name: row.name,
    nameBn: row.name_bn || '',
    category: row.category_id,
    price: row.price,
    unit: row.unit || 'kg',
    image: row.image_url || `images/${legacyId}.svg`,
    in_stock: row.in_stock !== false
  };
}

async function signIn(email, password) {
  const session = await supabase.signIn(email, password);
  const user = await supabase.getUser();
  if (!user) throw new Error('Login failed');

  const { data: profileRows, error } = await supabase
    .from('profiles')
    .select('role, full_name, email')
    .eq('id', user.id)
    .limit(1);

  if (error) console.warn('Profile lookup:', error);
  const profile = Array.isArray(profileRows) ? profileRows[0] : profileRows;
  const role = profile?.role || user.user_metadata?.role;

  if (!['admin', 'operator'].includes(role)) {
    await supabase.signOut();
    throw new Error('Admin or operator role required');
  }

  const auth = {
    id: user.id,
    email: user.email,
    role,
    name: profile?.full_name || user.email,
    expiresAt: Date.now() + 86400000,
    supabase: true
  };
  localStorage.setItem(ADMIN_SESSION_KEY, JSON.stringify(auth));
  return auth;
}

async function signOut() {
  await supabase.signOut();
  localStorage.removeItem(ADMIN_SESSION_KEY);
}

async function restoreSession() {
  const session = await supabase.getSession();
  if (!session) return null;
  const stored = localStorage.getItem(ADMIN_SESSION_KEY);
  if (!stored) return null;
  try {
    return JSON.parse(stored);
  } catch {
    return null;
  }
}

async function fetchProducts() {
  const rows = await loadProductsFromDB();
  return (rows || []).map((row, i) =>
    row.name && row.category_id ? mapDbProduct(row, i) : row
  );
}

async function fetchOrders() {
  return loadOrdersFromDB(100);
}

async function saveProduct(product) {
  const result = await updateProductInDB(product.id || product._uuid, {
    price: product.price,
    name: product.name,
    nameBn: product.nameBn,
    unit: product.unit,
    in_stock: product.in_stock !== false
  });
  return result;
}

async function setOrderStatus(orderId, status) {
  return updateOrderStatusInDB(orderId, status);
}

const backend = {
  enabled: isSupabaseConfigured(),
  signIn,
  signOut,
  restoreSession,
  fetchProducts,
  fetchOrders,
  saveProduct,
  setOrderStatus
};

window.JG_ADMIN_BACKEND = backend;

// Signal admin inline script when ready
window.dispatchEvent(new CustomEvent('jg-admin-backend-ready'));

export default backend;
