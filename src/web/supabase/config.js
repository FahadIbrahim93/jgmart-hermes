/**
 * JG Mart — Supabase Configuration
 *
 * Load order (first wins for URL/key):
 * 1. config.runtime.js  — CI / production (window.__JG_MART_SUPABASE__)
 * 2. config.local.js      — local dev (gitignored)
 * 3. Placeholders below
 */

let SUPABASE_URL = 'https://your-project-id.supabase.co';
let SUPABASE_ANON_KEY = 'your-anon-key';

if (typeof window !== 'undefined' && window.__JG_MART_SUPABASE__) {
  SUPABASE_URL = window.__JG_MART_SUPABASE__.url || SUPABASE_URL;
  SUPABASE_ANON_KEY = window.__JG_MART_SUPABASE__.anonKey || SUPABASE_ANON_KEY;
}

export { SUPABASE_URL, SUPABASE_ANON_KEY };

// Local-only override (gitignored)
try {
  const mod = await import('./config.local.js');
  if (mod?.SUPABASE_URL) SUPABASE_URL = mod.SUPABASE_URL;
  if (mod?.SUPABASE_ANON_KEY) SUPABASE_ANON_KEY = mod.SUPABASE_ANON_KEY;
} catch {
  // ignore if local config is absent
}

/** True when real Supabase credentials are configured (not placeholders). */
export function isSupabaseConfigured() {
  return (
    SUPABASE_URL.includes('supabase.co') &&
    !SUPABASE_URL.includes('your-project-id') &&
    SUPABASE_ANON_KEY.length > 20 &&
    !SUPABASE_ANON_KEY.includes('your-anon')
  );
}

export const JG_MART_CONFIG = {
  whatsappNumber: '+8801870489448',
  currency: 'BDT',
  currencySymbol: '৳',
  aov: 800,
  deliveryFee: 30,
  subscriptionPrice: 149,
  commissionRate: 0.11,
  slots: [
    { id: 'morning', label: '11:00 AM - 1:00 PM', cutoff: '9:00 AM' },
    { id: 'evening', label: '6:00 PM - 8:00 PM', cutoff: '3:00 PM' }
  ],
  zones: [
    { id: 1, name: 'Cluster 1 & 2', fee: 0 },
    { id: 2, name: 'Cluster 3', fee: 20 },
    { id: 3, name: 'Cluster 4', fee: 30 }
  ],
  categories: [
    { id: 'rice_dal', name: 'Rice & Dal', nameBn: 'চাউল ও ডাল', icon: '🍚' },
    { id: 'oil_spices', name: 'Oil & Spices', nameBn: 'তেল ও মশলা', icon: '🌶️' },
    { id: 'vegetables', name: 'Vegetables', nameBn: 'সবজি', icon: '🥬' },
    { id: 'fish', name: 'Fish', nameBn: 'মাছ', icon: '🐟' },
    { id: 'meat', name: 'Meat', nameBn: 'মাংস', icon: '🍗' },
    { id: 'dairy_eggs', name: 'Dairy & Eggs', nameBn: 'দুধ ও ডিম', icon: '🥛' },
    { id: 'fruits', name: 'Fruits', nameBn: 'ফল', icon: '🍎' },
    { id: 'fmcg', name: 'FMCG', nameBn: 'প্রয়োজনীয়', icon: '🧴' },
    { id: 'beverages', name: 'Beverages', nameBn: 'পানীয়', icon: '🥤' },
    { id: 'snacks', name: 'Snacks', nameBn: 'স্ন্যাকস', icon: '🍪' }
  ]
};
