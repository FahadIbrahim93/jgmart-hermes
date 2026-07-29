/**
 * JG Mart — Catalog Database Integration
 *
 * This script replaces localStorage-based data loading with Supabase.
 * Falls back to catalog_data.json if Supabase is not configured.
 */

import { supabase } from '../supabase/client.js';
import { isSupabaseConfigured } from '../supabase/config.js';

const USE_SUPABASE = isSupabaseConfigured();

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

    return data || [];
  } catch (error) {
    console.warn('Failed to load from Supabase, falling back to JSON:', error);
    return loadProductsFromJSON();
  }
}

function loadProductsFromJSON() {
  return fetch('catalog_data.json')
    .then(r => r.json())
    .then(data => data.products || [])
    .catch(err => {
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
  return fetch('catalog_data.json')
    .then(r => r.json())
    .then(data => data.categories || [])
    .catch(err => {
      console.error('Failed to load categories:', err);
      return [];
    });
}

// ============================================
// ORDERS
// ============================================
async function submitOrder(orderData) {
  if (!USE_SUPABASE) {
    return saveOrderToLocalStorage(orderData);
  }

  try {
    // Generate order number
    const { data: orderNumResult, error: numError } = await supabase.rpc('generate_order_number');
    if (numError) throw numError;
    const orderNum = orderNumResult;

    const { data, error } = await supabase
      .from('orders')
      .insert([{
        order_number: orderNum || `JG-${Date.now()}`,
        customer_name: orderData.customerName,
        customer_phone: orderData.customerPhone,
        customer_building: orderData.building,
        customer_flat: orderData.flat,
        delivery_zone_id: orderData.zoneId || 1,
        delivery_slot: orderData.slot || 'morning',
        delivery_date: orderData.deliveryDate || new Date().toISOString().split('T')[0],
        items: orderData.items,
        subtotal: orderData.subtotal,
        delivery_fee: orderData.deliveryFee,
        total: orderData.total,
        payment_method: orderData.paymentMethod || 'cash',
        status: 'pending'
      }])
      .select()
      .single();

    if (error) throw error;

    // Also insert order items
    if (orderData.items && orderData.items.length > 0) {
      const items = orderData.items.map(item => ({
        order_id: data.id,
        product_id: item.id,
        product_name: item.name,
        quantity: item.qty,
        unit_price: item.price,
        total: item.price * item.qty
      }));

      const { error: itemsError } = await supabase
        .from('order_items')
        .insert(items);

      if (itemsError) console.error('Failed to insert order items:', itemsError);
    }

    return { success: true, order: data };
  } catch (error) {
    console.error('Failed to submit order to Supabase:', error);
    return saveOrderToLocalStorage(orderData);
  }
}

function saveOrderToLocalStorage(orderData) {
  const orders = JSON.parse(localStorage.getItem('jgmart_ords') || '[]');
  const newOrder = {
    id: 'ORD-' + Date.now(),
    ...orderData,
    date: new Date().toISOString(),
    status: 'pending'
  };
  orders.push(newOrder);
  localStorage.setItem('jgmart_ords', JSON.stringify(orders));
  return { success: true, order: newOrder };
}

// ============================================
// SETTINGS
// ============================================
async function loadSettings() {
  if (!USE_SUPABASE) {
    return loadSettingsFromLocalStorage();
  }

  try {
    const { data, error } = await supabase
      .from('settings')
      .select('*');

    if (error) throw error;

    const settings = {};
    data?.forEach(s => {
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

// ============================================
// EXPORT
// ============================================
export {
  loadProductsFromDB,
  loadCategoriesFromDB,
  submitOrder,
  loadSettings
};
