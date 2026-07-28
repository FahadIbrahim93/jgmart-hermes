/**
 * JG Mart — Supabase Configuration
 *
 * Setup:
 * 1. Create a Supabase project at https://supabase.com
 * 2. Run the SQL in schema.sql and seed.sql in the Supabase SQL Editor
 * 3. Replace the values below with your project URL and anon key
 * 4. Enable Email auth in Supabase Dashboard → Authentication → Providers
 */

export const SUPABASE_URL = 'https://your-project-id.supabase.co';
export const SUPABASE_ANON_KEY = 'your-anon-key';

// Client-side Supabase instance
// In production, import from '@supabase/supabase-js'
// For now, this is a configuration placeholder

export const JG_MART_CONFIG = {
  // Business
  whatsappNumber: '+8801870489448',
  currency: 'BDT',
  currencySymbol: '৳',
  aov: 800,
  deliveryFee: 30,
  subscriptionPrice: 149,
  commissionRate: 0.11,

  // Delivery slots
  slots: [
    { id: 'morning', label: '11:00 AM - 1:00 PM', cutoff: '9:00 AM' },
    { id: 'evening', label: '6:00 PM - 8:00 PM', cutoff: '3:00 PM' }
  ],

  // Delivery zones
  zones: [
    { id: 1, name: 'Cluster 1 & 2', fee: 0 },
    { id: 2, name: 'Cluster 3', fee: 20 },
    { id: 3, name: 'Cluster 4', fee: 30 }
  ],

  // Categories
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
