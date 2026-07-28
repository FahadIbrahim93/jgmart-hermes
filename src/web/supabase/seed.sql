-- ============================================
-- JG Mart Seed Data
-- Run this AFTER schema.sql
-- ============================================

-- Seed categories
INSERT INTO public.categories (id, name, name_bn, icon, sort_order, is_active) VALUES
  ('rice_dal', 'Rice & Dal', 'চাউল ও ডাল', '🍚', 1, true),
  ('oil_spices', 'Oil & Spices', 'তেল ও মশলা', '🌶️', 2, true),
  ('vegetables', 'Vegetables', 'সবজি', '🥬', 3, true),
  ('fish', 'Fish', 'মাছ', '🐟', 4, true),
  ('meat', 'Meat', 'মাংস', '🍗', 5, true),
  ('dairy_eggs', 'Dairy & Eggs', 'দুধ ও ডিম', '🥛', 6, true),
  ('fruits', 'Fruits', 'ফল', '🍎', 7, true),
  ('fmcg', 'FMCG', 'প্রয়োজনীয়', '🧴', 8, true),
  ('beverages', 'Beverages', 'পানীয়', '🥤', 9, true),
  ('snacks', 'Snacks', 'স্ন্যাকস', '🍪', 10, true)
ON CONFLICT (id) DO NOTHING;

-- Seed sample products
INSERT INTO public.products (id, category_id, name, name_bn, price, unit, unit_bn, in_stock, is_featured, sort_order) VALUES
  -- Rice & Dal
  ('11111111-1111-1111-1111-111111111111', 'rice_dal', 'Chinigura Rice', 'চিনিগুরা চাউল', 120, 'kg', 'কেজি', true, true, 1),
  ('11111111-1111-1111-1111-111111111112', 'rice_dal', 'Miniket Rice', 'মিনিকেট চাউল', 85, 'kg', 'কেজি', true, true, 2),
  ('11111111-1111-1111-1111-111111111113', 'rice_dal', 'Mug Dal', 'মুগ ডাল', 140, 'kg', 'কেজি', true, false, 3),
  ('11111111-1111-1111-1111-111111111114', 'rice_dal', 'Cholar Dal', 'ছোলার ডাল', 160, 'kg', 'কেজি', true, false, 4),

  -- Vegetables
  ('22222222-2222-2222-2222-222222222221', 'vegetables', 'Potato', 'আলু', 30, 'kg', 'কেজি', true, true, 1),
  ('22222222-2222-2222-2222-222222222222', 'vegetables', 'Onion', 'পিয়াজ', 40, 'kg', 'কেজি', true, true, 2),
  ('22222222-2222-2222-2222-222222222223', 'vegetables', 'Tomato', 'টমেটো', 50, 'kg', 'কেজি', true, false, 3),
  ('22222222-2222-2222-2222-222222222224', 'vegetables', 'Green Chili', 'কাঁচা মরিচ', 80, 'kg', 'কেজি', true, false, 4),

  -- Fish
  ('33333333-3333-3333-3333-333333333331', 'fish', 'Ruhi Fish', 'রুই মাছ', 280, 'kg', 'কেজি', true, true, 1),
  ('33333333-3333-3333-3333-333333333332', 'fish', 'Katla Fish', 'কাতলা মাছ', 320, 'kg', 'কেজি', true, true, 2),
  ('33333333-3333-3333-3333-333333333333', 'fish', 'Pabda Fish', 'পাবদা মাছ', 350, 'kg', 'কেজি', true, false, 3),

  -- Meat
  ('44444444-4444-4444-4444-444444444441', 'meat', 'Chicken', 'চিকেন', 220, 'kg', 'কেজি', true, true, 1),
  ('44444444-4444-4444-4444-444444444442', 'meat', 'Beef', 'গরুর মাংস', 450, 'kg', 'কেজি', true, false, 2),
  ('44444444-4444-4444-4444-444444444443', 'meat', 'Mutton', 'খাসির মাংস', 750, 'kg', 'কেজি', true, false, 3),

  -- Dairy
  ('55555555-5555-5555-5555-555555555551', 'dairy_eggs', 'Fresh Milk', 'তাজা দুধ', 80, 'liter', 'লিটার', true, true, 1),
  ('55555555-5555-5555-5555-555555555552', 'dairy_eggs', 'Eggs', 'ডিম', 120, 'dozen', 'ডজন', true, true, 2),

  -- FMCG
  ('66666666-6666-6666-6666-666666666661', 'fmcg', 'Soybean Oil', 'সয়াবিন তেল', 180, 'liter', 'লিটার', true, false, 1),
  ('66666666-6666-6666-6666-666666666662', 'fmcg', 'Sugar', 'চিনি', 90, 'kg', 'কেজি', true, false, 2),
  ('66666666-6666-6666-6666-666666666663', 'fmcg', 'Salt', 'লবণ', 25, 'kg', 'কেজি', true, false, 3)
ON CONFLICT (id) DO NOTHING;

-- Seed sample admin user
-- Note: You need to create this user in Supabase Auth first, then run:
-- INSERT INTO public.profiles (id, email, full_name, role, phone) VALUES
--   ('auth-user-uuid-here', 'admin@jgmartbd.com', 'Fahad Ibrahim', 'admin', '8801870489448')
-- ON CONFLICT (id) DO NOTHING;
