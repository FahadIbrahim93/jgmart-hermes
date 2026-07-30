/**
 * JG Mart — Catalog Database Integration
 * Supabase-first with localStorage / JSON fallback.
 */

import { supabase } from '../supabase/client.js';
import { isSupabaseConfigured } from '../supabase/config.js';

const USE_SUPABASE = isSupabaseConfigured();

/** In-memory map: legacy catalog id (p001) → Supabase UUID */
let productUuidByLegacyId = new Map();

function isUuid(value) {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(
    String(value || '')
  );
}

function indexProducts(rows) {
  productUuidByLegacyId = new Map();
  (rows || []).forEach((row) => {
    const legacy = row.metadata?.legacy_id || row.legacy_id;
    if (legacy && row.id) productUuidByLegacyId.set(legacy, row.id);
    if (row.id) productUuidByLegacyId.set(row.id, row.id);
  });
}

function normalizeOrderInput(raw) {
  const items = (raw.items || []).map((item) => ({
    id: item.id,
    name: item.name || item.nm || 'Item',
    qty: Number(item.qty || item.quantity || 1),
    price: Number(item.price ?? item.pr ?? 0),
    uuid: item.uuid || item._uuid || null
  }));

  return {
    customerName: raw.customerName || raw.name || 'Customer',
    customerPhone: raw.customerPhone || raw.phone || '',
    building: raw.building || raw.customer_building || '',
    flat: raw.flat || raw.customer_flat || '',
    zoneId: raw.zoneId || raw.delivery_zone_id || 1,
    slot: raw.slot || raw.delivery_slot || 'morning',
    deliveryDate:
      raw.deliveryDate ||
      raw.delivery_date ||
      new Date().toISOString().split('T')[0],
    items,
    subtotal: Number(raw.subtotal ?? raw.sub ?? 0),
    deliveryFee: Number(raw.deliveryFee ?? raw.fee ?? 0),
    total: Number(raw.total ?? 0),
    paymentMethod: raw.paymentMethod || raw.payment || 'cash',
    notes: raw.notes || ''
  };
}

async function resolveProductUuid(legacyOrUuid) {
  if (!legacyOrUuid) return null;
  if (isUuid(legacyOrUuid)) return legacyOrUuid;
  if (productUuidByLegacyId.has(legacyOrUuid)) {
    return productUuidByLegacyId.get(legacyOrUuid);
  }
  if (!USE_SUPABASE) return null;

  try {
    const { data, error } = await supabase
      .from('products')
      .select('id, metadata')
      .limit(500);

    if (error) throw error;
    indexProducts(data);
    return productUuidByLegacyId.get(legacyOrUuid) || null;
  } catch (error) {
    console.warn('Product UUID lookup failed:', error);
    return null;
  }
}

// ============================================
// PRODUCTS
// ============================================
async function loadProductsFromDB() {
  if (!USE_SUPABASE) {
    return loadProductsFromJSON();
  }

  try {
    const { data, error } = await supabase
      .from('products')
      .select('*, categories(*)')
      .eq('in_stock', true)
      .order('sort_order', { ascending: true });

    if (error) throw error;
    indexProducts(data);
    return data || [];
  } catch (error) {
    console.warn('Failed to load from Supabase, falling back to JSON:', error);
    return loadProductsFromJSON();
  }
}

function loadProductsFromJSON() {
  return fetch('/src/web/catalog/catalog_data.json')
    .then((r) => (r.ok ? r : fetch('catalog_data.json')))
    .then((r) => r.json())
    .then((data) => data.products || [])
    .catch((err) => {
      console.error('Failed to load catalog_data.json:', err);
      return [];
    });
}

// ============================================
// CATEGORIES
// ============================================
async function loadCategoriesFromDB() {
  if (!USE_SUPABASE) {
    return loadCategoriesFromJSON();
  }

  try {
    const { data, error } = await supabase
      .from('categories')
      .select('*')
      .eq('is_active', true)
      .order('sort_order', { ascending: true });

    if (error) throw error;
    return data || [];
  } catch (error) {
    console.warn('Failed to load categories from Supabase, falling back to JSON:', error);
    return loadCategoriesFromJSON();
  }
}

function loadCategoriesFromJSON() {
  return fetch('/src/web/catalog/catalog_data.json')
    .then((r) => (r.ok ? r : fetch('catalog_data.json')))
    .then((r) => r.json())
    .then((data) => data.categories || [])
    .catch((err) => {
      console.error('Failed to load categories:', err);
      return [];
    });
}

// ============================================
// ORDERS
// ============================================
async function submitOrder(orderData) {
  const order = normalizeOrderInput(orderData);

  if (!USE_SUPABASE) {
    return saveOrderToLocalStorage(order);
  }

  try {
    const { data: orderNumResult, error: numError } = await supabase.rpc(
      'generate_order_number'
    );
    if (numError) console.warn('generate_order_number RPC:', numError);

    const orderNum = orderNumResult || `JG-${Date.now()}`;

    const itemsJson = order.items.map((item) => ({
      id: item.id,
      name: item.name,
      qty: item.qty,
      price: item.price
    }));

    // Use SECURITY DEFINER RPC to bypass anon RLS on orders insert (WhatsApp MVP).
    // Direct table insert is blocked by RLS even with permissive policy because
    // Supabase anon role requires DEFINER context for this write.
    const { data, error } = await supabase.rpc('create_public_order', {
      p_order_number: orderNum,
      p_customer_name: order.customerName,
      p_customer_phone: order.customerPhone || 'N/A',
      p_customer_building: order.building,
      p_customer_flat: order.flat,
      p_delivery_slot: order.slot || 'morning',
      p_delivery_date: order.deliveryDate || null,
      p_items: itemsJson,
      p_subtotal: order.subtotal || 0,
      p_delivery_fee: order.deliveryFee || 0,
      p_total: order.total || 0,
      p_payment_method: order.paymentMethod || 'cash',
      p_status: 'pending'
    });

    if (error) throw error;

    // Insert line items (uses anon RLS policy on order_items; falls back silently)
    const lineItems = [];
    for (const item of order.items) {
      const productId = await resolveProductUuid(item.uuid || item.id);
      if (!productId) continue;
      lineItems.push({
        order_id: data.id,
        product_id: productId,
        product_name: item.name,
        quantity: item.qty,
        unit_price: item.price,
        total: item.price * item.qty
      });
    }

    if (lineItems.length > 0) {
      const { error: itemsError } = await supabase.from('order_items').insert(lineItems);
      if (itemsError) console.error('Failed to insert order items:', itemsError);
    }

    saveOrderToLocalStorage({ ...order, id: data.order_number, supabaseId: data.id });
    return { success: true, order: data };
  } catch (error) {
    console.error('Failed to submit order to Supabase:', error);
    return { success: false, error, order: saveOrderToLocalStorage(order).order };
  }
}

function saveOrderToLocalStorage(orderData) {
  const order = normalizeOrderInput(orderData);
  const orders = JSON.parse(localStorage.getItem('jgmart_ords') || '[]');
  const newOrder = {
    id: orderData.id || 'ORD-' + Date.now(),
    ...order,
    name: order.customerName,
    date: new Date().toISOString(),
    status: orderData.status || 'pending'
  };
  orders.unshift(newOrder);
  if (orders.length > 100) orders.length = 100;
  localStorage.setItem('jgmart_ords', JSON.stringify(orders));
  return { success: true, order: newOrder };
}

// ============================================
// ADMIN / DASHBOARD READS
// ============================================
async function loadOrdersFromDB(limit = 50) {
  if (!USE_SUPABASE) {
    return JSON.parse(localStorage.getItem('jgmart_ords') || '[]');
  }

  try {
    const { data, error } = await supabase
      .from('orders')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(limit);

    if (error) throw error;
    return (data || []).map(mapDbOrderToLocal);
  } catch (error) {
    console.warn('Failed to load orders from Supabase:', error);
    return JSON.parse(localStorage.getItem('jgmart_ords') || '[]');
  }
}

function mapDbOrderToLocal(row) {
  return {
    id: row.order_number || row.id,
    supabaseId: row.id,
    customerName: row.customer_name,
    name: row.customer_name,
    customerPhone: row.customer_phone,
    building: row.customer_building,
    flat: row.customer_flat,
    slot: row.delivery_slot,
    total: row.total,
    subtotal: row.subtotal,
    deliveryFee: row.delivery_fee,
    status: row.status,
    date: row.created_at,
    items: row.items || []
  };
}

async function updateProductInDB(productId, updates) {
  if (!USE_SUPABASE) return { success: false, error: new Error('Supabase not configured') };

  const uuid = await resolveProductUuid(productId);
  if (!uuid) return { success: false, error: new Error('Product not found') };

  const payload = {};
  if (updates.price !== undefined) payload.price = Math.round(Number(updates.price));
  if (updates.name !== undefined) payload.name = updates.name;
  if (updates.nameBn !== undefined) payload.name_bn = updates.nameBn;
  if (updates.in_stock !== undefined) payload.in_stock = updates.in_stock;
  if (updates.unit !== undefined) payload.unit = updates.unit;

  const { data, error } = await supabase
    .from('products')
    .update(payload)
    .eq('id', uuid)
    .select()
    .single();

  if (error) return { success: false, error };
  return { success: true, product: data };
}

async function updateOrderStatusInDB(orderId, status) {
  if (!USE_SUPABASE) return { success: false };

  const { data, error } = await supabase
    .from('orders')
    .update({ status })
    .eq('order_number', orderId)
    .select()
    .single();

  if (error) {
    const byId = await supabase.from('orders').update({ status }).eq('id', orderId).select().single();
    if (byId.error) return { success: false, error: byId.error };
    return { success: true, order: byId.data };
  }
  return { success: true, order: data };
}

// ============================================
// SETTINGS
// ============================================
async function loadSettings() {
  if (!USE_SUPABASE) {
    return loadSettingsFromLocalStorage();
  }

  try {
    const { data, error } = await supabase.from('settings').select('*');
    if (error) throw error;

    const settings = {};
    data?.forEach((s) => {
      settings[s.key] = s.value;
    });
    return settings;
  } catch (error) {
    console.warn('Failed to load settings from Supabase, using defaults:', error);
    return loadSettingsFromLocalStorage();
  }
}

function loadSettingsFromLocalStorage() {
  return {
    whatsapp_number: localStorage.getItem('jgmart_wa') || '8801870489448',
    delivery_fee_bdt: 30,
    aov_bdt: 800
  };
}

export {
  loadProductsFromDB,
  loadCategoriesFromDB,
  submitOrder,
  loadSettings,
  loadOrdersFromDB,
  updateProductInDB,
  updateOrderStatusInDB,
  saveOrderToLocalStorage,
  normalizeOrderInput,
  resolveProductUuid
};

if (typeof window !== 'undefined') {
  window.submitOrderToSupabase = submitOrder;
  window.JG_DB = {
    loadProductsFromDB,
    loadOrdersFromDB,
    updateProductInDB,
    updateOrderStatusInDB,
    submitOrder
  };
}
