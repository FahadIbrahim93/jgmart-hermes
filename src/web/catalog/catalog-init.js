/**
 * JG Mart — Catalog bootstrap
 * Loads products into localStorage from catalog_data.json or Supabase before the UI renders.
 */
import { isSupabaseConfigured } from '../supabase/config.js';
import { loadProductsFromDB } from './db.js';

const CATEGORY_EMOJI = {
  rice_dal: '🍚',
  oil_spices: '🌶️',
  vegetables: '🥬',
  fish: '🐟',
  meat: '🍗',
  dairy_eggs: '🥛',
  fruits: '🍎',
  fmcg: '🧴',
  beverages: '🥤',
  snacks: '🍪'
};

function toCatalogProduct(p, index) {
  const id = p.id || `p${String(index + 1).padStart(2, '0')}`;
  const num = parseInt(String(id).replace(/\D/g, ''), 10) || index + 1;
  const imgFile = `images/p${String(num).padStart(3, '0')}.svg`;
  return {
    id,
    nm: p.name || p.nm,
    ct: p.category || p.category_id || p.ct,
    pr: p.price ?? p.pr,
    un: p.unit || p.un || 'pc',
    em: p.emoji || p.em || CATEGORY_EMOJI[p.category || p.ct] || '🛒',
    rt: p.rating ?? p.rt ?? 4.5,
    rv: p.orders ?? p.reviews ?? p.rv ?? 10,
    de: p.desc || p.description || p.de || '',
    im: p.image?.startsWith('http') ? p.image : imgFile
  };
}

function mapSupabaseProduct(row, index) {
  const legacyId = row.metadata?.legacy_id || `p${String(index + 1).padStart(2, '0')}`;
  return {
    id: legacyId,
    _uuid: row.id,
    nm: row.name,
    ct: row.category_id,
    pr: row.price,
    un: row.unit || 'pc',
    em: row.metadata?.emoji || CATEGORY_EMOJI[row.category_id] || '🛒',
    rt: row.metadata?.rating ?? 4.5,
    rv: row.metadata?.reviews ?? 10,
    de: row.description || '',
    im: row.image_url || `images/${legacyId}.svg`
  };
}

async function loadFromJson() {
  const response = await fetch('catalog_data.json');
  if (!response.ok) return null;
  const data = await response.json();
  if (!data.products?.length) return null;
  return data.products.map(toCatalogProduct);
}

async function loadFromSupabase() {
  const rows = await loadProductsFromDB();
  if (!rows?.length) return null;
  return rows.map(mapSupabaseProduct);
}

async function bootstrapCatalog() {
  // Always try to load fresh data from Supabase or JSON first.
  // This avoids stale cache during development and ensures the
  // catalog reflects the current database state on every visit.
  let products = null;

  if (isSupabaseConfigured()) {
    try {
      products = await loadFromSupabase();
    } catch (error) {
      console.warn('Supabase catalog load failed, falling back to JSON:', error);
    }
  }

  if (!products?.length) {
    try {
      products = await loadFromJson();
    } catch (error) {
      console.warn('catalog_data.json load failed:', error);
    }
  }

  if (products?.length) {
    localStorage.setItem('jgmart_prods', JSON.stringify(products));
    return products;
  }

  // Final fallback: return whatever is already in localStorage
  return JSON.parse(localStorage.getItem('jgmart_prods') || '[]');
}

window.__JG_CATALOG_READY = bootstrapCatalog();
if (window.JG_OFFLINE_QUEUE?.updateStatus) {
  window.JG_OFFLINE_QUEUE.updateStatus();
}
