-- ============================================
-- JG Mart Database Schema
-- Run this in Supabase SQL Editor
-- ============================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================
-- 1. PROFILES (extends Supabase auth.users)
-- ============================================
CREATE TABLE public.profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  email TEXT UNIQUE,
  full_name TEXT,
  phone TEXT,
  role TEXT DEFAULT 'customer' CHECK (role IN ('customer', 'operator', 'admin', 'partner')),
  avatar_url TEXT,
  building TEXT,
  flat_number TEXT,
  cluster INTEGER CHECK (cluster IN (1, 2, 3, 4)),
  is_active BOOLEAN DEFAULT true,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
  ON public.profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = id);

CREATE POLICY "Admins can view all profiles"
  ON public.profiles FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email, full_name)
  VALUES (NEW.id, NEW.email, NEW.raw_user_meta_data->>'full_name');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ============================================
-- 2. CATEGORIES
-- ============================================
CREATE TABLE public.categories (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  name_bn TEXT NOT NULL,
  icon TEXT NOT NULL,
  sort_order INTEGER DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.categories ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Categories are viewable by everyone"
  ON public.categories FOR SELECT
  USING (true);

CREATE POLICY "Only admins can modify categories"
  ON public.categories FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND role IN ('admin', 'operator')
    )
  );

-- ============================================
-- 3. PRODUCTS
-- ============================================
CREATE TABLE public.products (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  category_id TEXT REFERENCES public.categories(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  name_bn TEXT,
  description TEXT,
  description_bn TEXT,
  price INTEGER NOT NULL CHECK (price >= 0),
  unit TEXT DEFAULT 'piece',
  unit_bn TEXT DEFAULT 'পিস',
  image_url TEXT,
  thumbnail_url TEXT,
  in_stock BOOLEAN DEFAULT true,
  stock_quantity INTEGER DEFAULT 0,
  is_featured BOOLEAN DEFAULT false,
  is_organic BOOLEAN DEFAULT false,
  sort_order INTEGER DEFAULT 0,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Products are viewable by everyone"
  ON public.products FOR SELECT
  USING (true);

CREATE POLICY "Only admins/operators can modify products"
  ON public.products FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND role IN ('admin', 'operator')
    )
  );

CREATE INDEX idx_products_category ON public.products(category_id);
CREATE INDEX idx_products_active ON public.products(in_stock) WHERE in_stock = true;

-- ============================================
-- 4. ORDERS
-- ============================================
CREATE TABLE public.orders (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  order_number TEXT UNIQUE NOT NULL,
  customer_id UUID REFERENCES public.profiles(id),
  customer_name TEXT NOT NULL,
  customer_phone TEXT NOT NULL,
  customer_building TEXT NOT NULL,
  customer_flat TEXT NOT NULL,
  delivery_zone_id INTEGER DEFAULT 1,
  delivery_slot TEXT DEFAULT 'morning',
  delivery_date DATE NOT NULL,
  delivery_time TEXT,
  items JSONB NOT NULL DEFAULT '[]'::jsonb,
  subtotal INTEGER NOT NULL CHECK (subtotal >= 0),
  delivery_fee INTEGER NOT NULL DEFAULT 0 CHECK (delivery_fee >= 0),
  discount INTEGER DEFAULT 0 CHECK (discount >= 0),
  total INTEGER NOT NULL CHECK (total >= 0),
  payment_method TEXT DEFAULT 'cash' CHECK (payment_method IN ('cash', 'bkash', 'nogod', 'rocket')),
  payment_status TEXT DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'failed', 'refunded')),
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'processing', 'out_for_delivery', 'delivered', 'cancelled')),
  rider_id UUID REFERENCES public.profiles(id),
  rider_name TEXT,
  notes TEXT,
  whatsapp_message_id TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Customers can view own orders"
  ON public.orders FOR SELECT
  USING (auth.uid() = customer_id);

CREATE POLICY "Staff can view all orders"
  ON public.orders FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND role IN ('admin', 'operator', 'partner')
    )
  );

CREATE POLICY "Staff can update orders"
  ON public.orders FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND role IN ('admin', 'operator')
    )
  );

-- WhatsApp MVP: anonymous customers can place orders without login
CREATE POLICY "Anyone can create orders"
  ON public.orders FOR INSERT
  WITH CHECK (true);

CREATE INDEX idx_orders_customer ON public.orders(customer_id);
CREATE INDEX idx_orders_status ON public.orders(status);
CREATE INDEX idx_orders_date ON public.orders(delivery_date);
CREATE INDEX idx_orders_created ON public.orders(created_at DESC);

-- ============================================
-- 5. ORDER ITEMS (normalized)
-- ============================================
CREATE TABLE public.order_items (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  order_id UUID REFERENCES public.orders(id) ON DELETE CASCADE,
  product_id UUID REFERENCES public.products(id),
  product_name TEXT NOT NULL,
  product_image_url TEXT,
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  unit_price INTEGER NOT NULL CHECK (unit_price >= 0),
  total INTEGER NOT NULL CHECK (total >= 0),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.order_items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Order items viewable with order"
  ON public.order_items FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.orders
      WHERE orders.id = order_items.order_id
      AND (auth.uid() = orders.customer_id OR EXISTS (
        SELECT 1 FROM public.profiles
        WHERE id = auth.uid() AND role IN ('admin', 'operator', 'partner')
      ))
    )
  );

CREATE POLICY "Anyone can create order items"
  ON public.order_items FOR INSERT
  WITH CHECK (true);

-- ============================================
-- 6. CUSTOMERS (denormalized for performance)
-- ============================================
CREATE TABLE public.customers (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  profile_id UUID REFERENCES public.profiles(id),
  name TEXT NOT NULL,
  phone TEXT UNIQUE NOT NULL,
  email TEXT,
  building TEXT NOT NULL,
  flat_number TEXT NOT NULL,
  cluster INTEGER CHECK (cluster IN (1, 2, 3, 4)),
  total_orders INTEGER DEFAULT 0,
  total_spend INTEGER DEFAULT 0,
  first_order_date DATE,
  last_order_date DATE,
  avg_order_value INTEGER DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  notes TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.customers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Staff can manage customers"
  ON public.customers FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND role IN ('admin', 'operator')
    )
  );

CREATE INDEX idx_customers_phone ON public.customers(phone);
CREATE INDEX idx_customers_cluster ON public.customers(cluster);

-- ============================================
-- 7. PARTNERS
-- ============================================
CREATE TABLE public.partners (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  profile_id UUID REFERENCES public.profiles(id),
  shop_name TEXT NOT NULL,
  category TEXT NOT NULL CHECK (category IN ('rice_dal', 'oil_spices', 'vegetables', 'fish', 'meat', 'dairy_eggs', 'fruits', 'fmcg', 'beverages', 'snacks')),
  contact_name TEXT NOT NULL,
  phone TEXT NOT NULL,
  whatsapp TEXT,
  address TEXT NOT NULL,
  location_lat DECIMAL(10, 8),
  location_lng DECIMAL(11, 8),
  commission_rate DECIMAL(5, 4) DEFAULT 0.10 CHECK (commission_rate >= 0 AND commission_rate <= 1),
  min_order_amount INTEGER DEFAULT 0,
  max_order_amount INTEGER DEFAULT 50000,
  cutoff_time TIME DEFAULT '09:00:00',
  pickup_start TIME DEFAULT '10:00:00',
  pickup_end TIME DEFAULT '11:00:00',
  is_active BOOLEAN DEFAULT true,
  is_verified BOOLEAN DEFAULT false,
  rating DECIMAL(3, 2) DEFAULT 0.00 CHECK (rating >= 0 AND rating <= 5),
  total_orders INTEGER DEFAULT 0,
  total_revenue INTEGER DEFAULT 0,
  notes TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.partners ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Partners viewable by staff"
  ON public.partners FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND role IN ('admin', 'operator')
    )
    OR
    auth.uid() = profile_id
  );

CREATE POLICY "Only admins can modify partners"
  ON public.partners FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

CREATE INDEX idx_partners_category ON public.partners(category);
CREATE INDEX idx_partners_active ON public.partners(is_active) WHERE is_active = true;

-- ============================================
-- 8. SETTINGS (key-value store)
-- ============================================
CREATE TABLE public.settings (
  key TEXT PRIMARY KEY,
  value JSONB NOT NULL,
  description TEXT,
  updated_by UUID REFERENCES public.profiles(id),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.settings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Settings viewable by authenticated users"
  ON public.settings FOR SELECT
  USING (auth.role() = 'authenticated');

CREATE POLICY "Only admins can modify settings"
  ON public.settings FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- Seed default settings
INSERT INTO public.settings (key, value, description) VALUES
  ('whatsapp_number', '"8801870489448"', 'Business WhatsApp number'),
  ('aov_bdt', '800', 'Average order value in BDT'),
  ('delivery_fee_bdt', '30', 'Standard delivery fee in BDT'),
  ('subscription_price_bdt', '149', 'Monthly subscription price in BDT'),
  ('commission_rate', '0.11', 'Blended commission rate'),
  ('site_name', '"JG Mart"', 'Site name'),
  ('site_tagline', '"Fresh Groceries at Krishi Market Prices"', 'Site tagline'),
  ('currency_symbol', '"৳"', 'Currency symbol'),
  ('delivery_slots', '["11:00 AM - 1:00 PM", "6:00 PM - 8:00 PM"]', 'Available delivery slots'),
  ('morning_cutoff', '"9:00 AM"', 'Morning slot order cutoff'),
  ('evening_cutoff', '"3:00 PM"', 'Evening slot order cutoff')
ON CONFLICT (key) DO NOTHING;

-- ============================================
-- 9. AUDIT LOG
-- ============================================
CREATE TABLE public.audit_log (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES public.profiles(id),
  action TEXT NOT NULL,
  table_name TEXT NOT NULL,
  record_id UUID,
  old_values JSONB,
  new_values JSONB,
  ip_address TEXT,
  user_agent TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.audit_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Admins can view audit log"
  ON public.audit_log FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

CREATE INDEX idx_audit_log_user ON public.audit_log(user_id);
CREATE INDEX idx_audit_log_table ON public.audit_log(table_name);
CREATE INDEX idx_audit_log_created ON public.audit_log(created_at DESC);

-- ============================================
-- 10. FUNCTIONS
-- ============================================

-- Update updated_at timestamp
CREATE OR REPLACE FUNCTION public.update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to relevant tables
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON public.products
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();

CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON public.orders
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();

CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON public.customers
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();

CREATE TRIGGER update_partners_updated_at BEFORE UPDATE ON public.partners
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();

-- Generate order number
CREATE OR REPLACE FUNCTION public.generate_order_number()
RETURNS TEXT AS $$
DECLARE
  seq INTEGER;
  num TEXT;
BEGIN
  SELECT COALESCE(MAX(CAST(SUBSTRING(order_number FROM 5) AS INTEGER)), 0) + 1
  INTO seq
  FROM public.orders
  WHERE order_number LIKE 'JG-%';

  num := 'JG-' || LPAD(seq::TEXT, 5, '0');
  RETURN num;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 11. REALTIME (optional)
-- ============================================

-- Enable realtime for orders
ALTER PUBLICATION supabase_realtime ADD TABLE public.orders;
ALTER PUBLICATION supabase_realtime ADD TABLE public.order_items;

-- ============================================
-- 12. STORAGE BUCKETS (optional)
-- ============================================

-- Create storage bucket for product images
-- Run this in Supabase Dashboard → Storage or via SQL:
-- INSERT INTO storage.buckets (id, name, public) VALUES ('product-images', 'product-images', true);

-- Storage policies:
-- CREATE POLICY "Product images are publicly accessible"
--   ON storage.objects FOR SELECT
--   USING (bucket_id = 'product-images');
--
-- CREATE POLICY "Admins can upload product images"
--   ON storage.objects FOR INSERT
--   WITH CHECK (
--     bucket_id = 'product-images' AND
--     EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'operator'))
--   );


-- Public order intake (WhatsApp MVP — no customer login)
-- Run AFTER schema.sql if policies are missing

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE schemaname = 'public' AND tablename = 'orders'
      AND policyname = 'Anyone can create orders'
  ) THEN
    CREATE POLICY "Anyone can create orders"
      ON public.orders FOR INSERT
      WITH CHECK (true);
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE schemaname = 'public' AND tablename = 'order_items'
      AND policyname = 'Anyone can create order items'
  ) THEN
    CREATE POLICY "Anyone can create order items"
      ON public.order_items FOR INSERT
      WITH CHECK (true);
  END IF;
END $$;


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


-- Auto-generated from catalog_data.json
-- Run AFTER schema.sql in Supabase SQL Editor

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'b6c99740-ba81-5aef-8d59-500aaa734132', 'rice_dal', 'Premium Chinigura Rice', 'প্রিমিয়াম চিনিগুরা চাউল', 'Aromatic fine-grain rice from northern Bangladesh', 'উত্তর বাংলাদেশের সুগন্ধি চিনিগুরা চাউল',
  120, 'kg', 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop', true, true, 1, '{"legacy_id": "p001", "emoji": "\ud83c\udf5a"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '881658c8-b270-5597-a73c-13802ed6f8e4', 'rice_dal', 'Organic Moong Dal', 'জৈব মুগ ডাল', 'Split green gram, polished and ready to cook', 'ভর্তা করা সবুজ মুগ ডাল, রান্নার জন্য প্রস্তুত',
  140, 'kg', 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop', true, true, 2, '{"legacy_id": "p002", "emoji": "\ud83d\udfe2"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '1b2ca03c-2f64-5645-82f5-5720e9944b6e', 'rice_dal', 'Premium Basmati Rice', 'প্রিমিয়াম বাসমতি চাউল', 'Extra-long grain basmati, aged for aroma', 'অতিরিক্ত দীর্ঘ দানার বাসমতি, সুবাসের জন্য বয়স্ক',
  160, 'kg', 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop', true, true, 3, '{"legacy_id": "p003", "emoji": "\ud83c\udf5a"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'e7f84876-3bc2-5760-a631-8d46759e1bbc', 'rice_dal', 'Moong Dal (Yellow)', 'মুগ ডাল (হলুদ)', 'Yellow split gram, protein-rich staple', 'হলুদ ভর্তা ডাল, প্রোটিন সমৃদ্ধ মৌলিক খাবার',
  110, 'kg', 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop', true, true, 4, '{"legacy_id": "p036", "emoji": "\ud83d\udfe1"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'ebedac24-cf16-5115-9b42-b57e555d584a', 'rice_dal', 'Masoor Dal (Red Lentil)', 'মসুর ডাল', 'Protein-rich red lentils, quick to cook', 'প্রোটিন সমৃদ্ধ মসুর ডাল, তাড়াতাড়ি রান্না হয়',
  100, 'kg', 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop', true, true, 5, '{"legacy_id": "p051", "emoji": "\ud83d\udfe0"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'e48842b0-f6d2-5bb5-98af-0104704ad63c', 'rice_dal', 'Fortified Rice (Local)', 'ফোর্টিফাইড চাউল (স্থানীয়)', 'Vitamin-fortified local rice, healthy choice', 'ভিটামিন সমৃদ্ধ স্থানীয় চাউল, স্বাস্থ্যকর পছন্দ',
  110, 'kg', 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop', true, true, 6, '{"legacy_id": "p052", "emoji": "\ud83c\udf5a"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'f1c655e3-8f0d-5f0f-9c09-3273e79bb864', 'rice_dal', 'Chola (Bengal Gram)', 'ছোলা (বুটের ডাল)', 'Whole Bengal gram, perfect for curries and snacks', 'পুরো বুটের ডাল, কারি ও স্ন্যাকসের জন্য উপযোগী',
  90, 'kg', 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop', true, false, 7, '{"legacy_id": "p053", "emoji": "\ud83d\udfe4"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'aa32044b-e81c-5eeb-b77e-b966a552ea1f', 'rice_dal', 'Biryani Rice (Kallijira)', 'বিরিয়ানি চাউল (কালিজিরা)', 'Aromatic Kallijira rice, ideal for biryani', 'সুগন্ধি কালিজিরা চাউল, বিরিয়ানির জন্য নিখুঁত',
  150, 'kg', 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop', true, false, 8, '{"legacy_id": "p054", "emoji": "\ud83c\udf5a"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'e061e60f-9f64-5640-8fff-17a14c391aee', 'oil_spices', 'Mustard Oil (Fortified)', 'সরিষা তেল (ফোর্টিফাইড)', 'Cold-pressed mustard oil for authentic Bengali cooking', 'প্রামাণ্য বাংলা রান্নার জন্য ঠান্ডা চাপা সরিষা তেল',
  180, 'L', 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=300&fit=crop', true, false, 9, '{"legacy_id": "p004", "emoji": "\ud83e\uded7"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '0687afff-7a45-5bd4-9e51-a3a63468fd26', 'oil_spices', 'Sunflower Oil', 'সূর্যমুখী তেল', 'Refined sunflower oil for daily cooking', 'দৈনিক রান্নার জন্য শোধন করা সূর্যমুখী তেল',
  170, 'L', 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=300&fit=crop', true, false, 10, '{"legacy_id": "p005", "emoji": "\ud83c\udf3b"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '862af440-a431-5c25-b0b8-a2999070900a', 'oil_spices', 'Turmeric Powder', 'হলুদ গুঁড়া', 'Premium quality haldi from local farms', 'স্থানীয় খামার থেকে প্রিমিয়াম মানের হলুদ',
  80, '100g', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop', true, false, 11, '{"legacy_id": "p006", "emoji": "\ud83e\udde1"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '9943cd45-c455-5f39-9b18-634622bda65e', 'oil_spices', 'Chili Powder', 'মরিচ গুঁড়া', 'Hot red chili powder for authentic heat', 'প্রামাণ্য গরম লাল মরিচ গুঁড়া',
  120, '100g', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop', true, false, 12, '{"legacy_id": "p037", "emoji": "\ud83c\udf36\ufe0f"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '5606c453-f702-5458-9fbc-f4ccb091ec9f', 'oil_spices', 'Cumin Powder', 'জিরা গুঁড়া', 'Aromatic cumin powder, essential for curries', 'সুবাসী জিরা গুঁড়া, কারির জন্য অপরিহার্য',
  90, '100g', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop', true, false, 13, '{"legacy_id": "p038", "emoji": "\ud83d\udfe4"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '8b815464-0d98-5d1f-9427-c0fc91313830', 'oil_spices', 'Soybean Oil (Fortified)', 'সয়াবিন তেল (ফোর্টিফাইড)', 'Vitamin-fortified soybean oil for daily cooking', 'ভিটামিন সমৃদ্ধ সয়াবিন তেল, দৈনিক রান্নার জন্য',
  160, 'L', 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=300&fit=crop', true, false, 14, '{"legacy_id": "p055", "emoji": "\ud83e\uded7"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '71cb8fad-0fb3-589e-bd3b-8305efe945a6', 'oil_spices', 'Cinnamon Sticks', 'দারুচিনি', 'Aromatic cinnamon sticks for rich flavor', 'সুগন্ধি দারুচিনি, সমৃদ্ধ স্বাদের জন্য',
  50, '100g', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop', true, false, 15, '{"legacy_id": "p056", "emoji": "\ud83d\udfe4"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '528b88f7-2814-507a-a7f3-f29289af55af', 'oil_spices', 'Cardamom (Green)', 'এলাচ (সবুজ)', 'Premium green cardamom, fragrant and flavorful', 'প্রিমিয়াম সবুজ এলাচ, সুগন্ধি ও স্বাদবহুল',
  120, '100g', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop', true, false, 16, '{"legacy_id": "p057", "emoji": "\ud83d\udfe2"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'a91785cb-3dba-5553-af43-b363e7bf1daa', 'vegetables', 'Red Onion', 'লাল পিয়াজ', 'Fresh red onions, farm-picked this morning', 'তাজা লাল পিয়াজ, আজ সকালে কৃষি বাজার থেকে',
  60, 'kg', 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&h=300&fit=crop', true, false, 17, '{"legacy_id": "p007", "emoji": "\ud83e\uddc5"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'c83db639-eb30-5a02-90d5-e3ec39917cc7', 'vegetables', 'Potato (Local)', 'স্থানীয় আলু', 'Versatile local potatoes, ideal for all dishes', 'সব ধরনের খাবারের জন্য উপযোগী স্থানীয় আলু',
  35, 'kg', 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&h=300&fit=crop', true, false, 18, '{"legacy_id": "p008", "emoji": "\ud83e\udd54"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '28e6713f-fa51-5877-8909-376c88f8e4b6', 'vegetables', 'Tomato (Deshi)', 'দেশি টমেটো', 'Juicy deshi tomatoes, perfect for curries', 'রসালো দেশি টমেটো, কারির জন্য নিখুঁত',
  70, 'kg', 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400&h=300&fit=crop', true, false, 19, '{"legacy_id": "p009", "emoji": "\ud83c\udf45"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '99301b95-ce87-55f7-847a-f76fc4b34143', 'vegetables', 'Brinjal (Long)', 'লম্বা বেগুন', 'Tender long brinjals, glossy and fresh', 'নরম লম্বা বেগুন, চকচকে এবং তাজা',
  40, 'kg', 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop', true, false, 20, '{"legacy_id": "p010", "emoji": "\ud83c\udf46"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'ba1497b1-3c8b-5770-8e7e-0523df2b874f', 'vegetables', 'Green Chili', 'কাঁচা মরিচ', 'Spicy green chilies, farm fresh', 'ঝাল কাঁচা মরিচ, খামার থেকে তাজা',
  40, '100g', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop', true, false, 21, '{"legacy_id": "p011", "emoji": "\ud83c\udf36\ufe0f"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'be60f4a0-b667-5e1d-8e31-c2890fbe3257', 'vegetables', 'Cauliflower', 'ফুলকপি', 'Fresh white cauliflower, tight florets', 'তাজা সাদা ফুলকপি, কড়া ফুলের সাথে',
  55, 'piece', 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop', true, false, 22, '{"legacy_id": "p012", "emoji": "\ud83e\udd66"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'eeb91464-f09a-5b8d-8695-b3f5e18902db', 'vegetables', 'Coriander Leaves', 'ধনিয়া পাতা', 'Fresh coriander leaves, bunch of 5-6 stems', 'তাজা ধনিয়া পাতা, ৫-৬ ডগা গুচ্ছ',
  15, 'bunch', 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop', true, false, 23, '{"legacy_id": "p039", "emoji": "\ud83c\udf3f"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '41b63c98-f823-5095-bea3-9a7a90661b97', 'vegetables', 'Brinjal (Round)', 'গোল বেগুন', 'Tender round brinjals, glossy and fresh', 'নরম গোল বেগুন, চকচকে এবং তাজা',
  35, 'kg', 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop', true, false, 24, '{"legacy_id": "p040", "emoji": "\ud83c\udf46"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'ab0ad41d-8e9e-51b3-a284-84f1549041e8', 'vegetables', 'Lady Finger (Bhindi)', 'ঢেঁড়স', 'Fresh bhindi, tender and crisp', 'তাজা ঢেঁড়স, নরম এবং কড়া',
  50, 'kg', 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop', true, false, 25, '{"legacy_id": "p041", "emoji": "\ud83e\udd52"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'cdad6087-57e9-5bdb-873d-d73e4c7b9349', 'vegetables', 'Pointed Gourd (Potol)', 'পটল', 'Fresh pointed gourd, perfect for curries', 'তাজা পটল, কারির জন্য নিখুঁত',
  80, 'kg', 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop', true, false, 26, '{"legacy_id": "p042", "emoji": "\ud83e\udd52"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '8e415a7b-8cbc-53a9-a2a7-daf9aea13379', 'vegetables', 'Lemon (Fresh)', 'তাজা লেবু', 'Juicy fresh lemons, great for drinks and cooking', 'রসালো তাজা লেবু, পানীয় ও রান্নার জন্য দারুণ',
  20, 'piece', 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400&h=300&fit=crop', true, false, 27, '{"legacy_id": "p063", "emoji": "\ud83c\udf4b"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'd97b7f7e-afe8-534d-b7f8-418fc35709c1', 'vegetables', 'Ginger (Fresh)', 'তাজা আদা', 'Fresh ginger root, essential for Bengali cooking', 'তাজা আদা, বাংলা রান্নার জন্য অপরিহার্য',
  60, 'kg', 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop', true, false, 28, '{"legacy_id": "p064", "emoji": "\ud83c\udf31"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '65f8c216-2666-5989-bad8-99e023789b1e', 'vegetables', 'Garlic (Deshi)', 'দেশি রসুন', 'Strong-flavored local garlic, dried and cleaned', 'ঝাঁজালো দেশি রসুন, শুকানো ও পরিষ্কার',
  100, 'kg', 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop', true, false, 29, '{"legacy_id": "p065", "emoji": "\ud83e\uddc4"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '261b911c-e2b1-544c-9849-8ee0c622e11f', 'fish', 'Ruhi Fish (Medium)', 'রুই মাছ (মাঝারি)', 'Fresh ruhi from local ponds, cleaned & packed', 'স্থানীয় পুকুর থেকে তাজা রুই, প্রস্তুত',
  280, 'kg', 'https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop', true, false, 30, '{"legacy_id": "p013", "emoji": "\ud83d\udc1f"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '2ba93b8f-09f5-5ebe-92a6-7ce831e2c063', 'fish', 'Prawns (Large)', 'বড় চিংড়ি', 'Jumbo river prawns, deveined and ready to cook', 'বড় নদী চিংড়ি, রান্নার জন্য প্রস্তুত',
  450, 'kg', 'https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop', true, false, 31, '{"legacy_id": "p014", "emoji": "\ud83e\udd90"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '0d8612a5-a820-571c-a757-48f3f1ed1c34', 'fish', 'Ilish Fish (Hilsa)', 'ইলিশ মাছ', 'Premium ilish hilsa, seasonal delicacy', 'প্রিমিয়াম ইলিশ, ঋতুর বিশেষ খাবার',
  850, 'kg', 'https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop', true, false, 32, '{"legacy_id": "p015", "emoji": "\ud83d\udc1f"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '652f0a78-2fd0-51cb-a661-d2eebc03ca6e', 'fish', 'Tilapia Fish', 'তেলাপিয়া মাছ', 'Farm-raised tilapia, boneless fillets available', 'খামারে উৎপাদিত তেলাপিয়া, বোনলেস ফিলেট উপলব্ধ',
  200, 'kg', 'https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop', true, false, 33, '{"legacy_id": "p016", "emoji": "\ud83d\udc1f"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'a2a3763c-f9ac-5854-9884-4ae57b463450', 'fish', 'Rohu Fish (Large)', 'রুই মাছ (বড়)', 'Large rohu fish, ideal for family meals', 'বড় রুই মাছ, পারিবারিক খাবারের জন্য নিখুঁত',
  240, 'kg', 'https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop', true, false, 34, '{"legacy_id": "p043", "emoji": "\ud83d\udc1f"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '3f0dc2ef-846d-5f86-b0d5-3b1f0368f861', 'fish', 'Katla Fish', 'কাতলা মাছ', 'Premium katla, boneless option available', 'প্রিমিয়াম কাতলা, বোনলেস অপশন উপলব্ধ',
  260, 'kg', 'https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop', true, false, 35, '{"legacy_id": "p044", "emoji": "\ud83d\udc1f"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '2f1f5bb6-156b-56ef-b773-11a34dfbb5da', 'meat', 'Chicken (Broiler)', 'বয়লার মুরগি', 'Halal-certified broiler chicken, whole or cut', 'হালাল সার্টিফাইড ব্রয়েলার চিকেন, পুরো বা কাটা',
  220, 'kg', 'https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400&h=300&fit=crop', true, false, 36, '{"legacy_id": "p017", "emoji": "\ud83c\udf57"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'e8342ba2-acb4-5e17-979f-9aea56ea462f', 'meat', 'Mutton (Curry Cut)', 'মটন (কারি কাট)', 'Tender mutton curry cuts, bone-in', 'কোমল মটন কারি কাট, হাড় সহ',
  680, 'kg', 'https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400&h=300&fit=crop', true, false, 37, '{"legacy_id": "p018", "emoji": "\ud83c\udf56"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '4633ef52-4978-50ce-981b-16e6452736e4', 'meat', 'Beef (Premium Cut)', 'বিফ (প্রিমিয়াম কাট)', 'Tender premium beef cuts, freshly cut', 'নরম প্রিমিয়াম গরুর মাংসের কাট, তাজা কাটা',
  520, 'kg', 'https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400&h=300&fit=crop', true, false, 38, '{"legacy_id": "p019", "emoji": "\ud83e\udd69"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'a5de528e-0163-54fa-ae03-65788dcabdd0', 'meat', 'Chicken Breast (Skinless)', 'চিকেন ব্রেস্ট (চামড়াবিহীন)', 'Lean skinless chicken breast, high protein', 'চর্বিহীন চামড়াবিহীন চিকেন ব্রেস্ট, উচ্চ প্রোটিন',
  260, 'kg', 'https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400&h=300&fit=crop', true, false, 39, '{"legacy_id": "p058", "emoji": "\ud83c\udf57"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'e7fd2a7b-bc2c-555b-8603-37a4504fbd5f', 'meat', 'Beef Liver', 'গরুর কলিজা', 'Fresh beef liver, iron-rich and nutritious', 'তাজা গরুর কলিজা, আয়রন সমৃদ্ধ ও পুষ্টিকর',
  280, 'kg', 'https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400&h=300&fit=crop', true, false, 40, '{"legacy_id": "p059", "emoji": "\ud83e\udd69"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '1d5a1644-9a7a-57e3-a4c9-308296d07cd7', 'dairy_eggs', 'Fresh Cow Milk', 'তাজা গরুর দুধ', 'Farm-fresh whole milk, delivered cold', 'খামার থেকে তাজা পুরো দুধ, ঠান্ডা ডেলিভারি',
  80, 'L', 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop', true, false, 41, '{"legacy_id": "p020", "emoji": "\ud83e\udd5b"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '1367001f-c432-51d3-ac0b-087744e00c0c', 'dairy_eggs', 'Farm Eggs', 'খামারের ডিম', 'Free-range eggs from local farms', 'স্থানীয় খামার থেকে মুক্ত পরিসরের ডিম',
  120, 'dozen', 'https://images.unsplash.com/photo-1582722879130-6286d4e080ea?w=400&h=300&fit=crop', true, false, 42, '{"legacy_id": "p021", "emoji": "\ud83e\udd5a"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '8d2e4ebe-3d7b-5e0b-bebb-9ca7824fa6d2', 'dairy_eggs', 'Paneer (Fresh)', 'তাজা পনির', 'Soft fresh paneer, made daily', 'নরম তাজা পনির, প্রতিদিন তৈরি',
  250, '250g', 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop', true, false, 43, '{"legacy_id": "p022", "emoji": "\ud83e\uddc0"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '984689ac-19df-5588-ae7b-987d38b0d0f4', 'dairy_eggs', 'Yogurt (Mishti Doi)', 'মিষ্টি দই', 'Sweetened creamy yogurt, traditional taste', 'মিষ্টি ক্রিমি দই, পারম্পরিক স্বাদ',
  60, '250g', 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop', true, false, 44, '{"legacy_id": "p023", "emoji": "\ud83c\udf6f"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '697b8f0c-4527-5e54-beff-b89a593f7749', 'dairy_eggs', 'Full Cream Milk', 'ফুল ক্রিম মিল্ক', 'Rich full cream milk, 3.5% fat', 'সমৃদ্ধ ফুল ক্রিম দুধ, ৩.৫% চর্বি',
  90, 'L', 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop', true, false, 45, '{"legacy_id": "p045", "emoji": "\ud83e\udd5b"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '70cd53d7-e690-522d-b612-52e5e010d58c', 'dairy_eggs', 'Butter (Cooking)', 'মাখন (রান্নার)', 'Creamy unsalted butter, perfect for cooking', 'ক্রিমি লবণবিহীন মাখন, রান্নার জন্য নিখুঁত',
  180, '200g', 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop', true, false, 46, '{"legacy_id": "p046", "emoji": "\ud83e\uddc8"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'a25f0eed-6b26-5cd3-b4ee-4f53110ce736', 'fruits', 'Deshi Mango (Himsagar)', 'দেশি আম (হিমসাগর)', 'Seasonal Himsagar mango, sweet and fibreless', 'ঋতুর হিমসাগর আম, মিষ্টি ও ফাইবারবিহীন',
  180, 'kg', 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&h=300&fit=crop', true, false, 47, '{"legacy_id": "p024", "emoji": "\ud83e\udd6d"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '6df89978-0c08-5890-987f-1e69795119b9', 'fruits', 'Banana (Sagor)', 'সাগর কলা', 'Ripe sagor bananas, energy-boosting', 'পাকা সাগর কলা, শক্তি বৃদ্ধিকারী',
  50, 'dozen', 'https://images.unsplash.com/photo-1571771894821-ce9b784f8114?w=400&h=300&fit=crop', true, false, 48, '{"legacy_id": "p025", "emoji": "\ud83c\udf4c"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'cf436522-ed90-5819-9a15-03f0a0675d76', 'fruits', 'Watermelon', 'তরমুজ', 'Sweet summer watermelon, chilled on request', 'মিষ্টি গরমের তরমুজ, অনুরোধে ঠান্ডা করা',
  40, 'kg', 'https://images.unsplash.com/photo-1619566636859-ad7264c1d2c4?w=400&h=300&fit=crop', true, false, 49, '{"legacy_id": "p026", "emoji": "\ud83c\udf49"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '045f0307-17d4-52b0-811f-f1198d2ab7aa', 'fruits', 'Jackfruit (Kathal)', 'কাঁঠাল', 'Fresh seasonal jackfruit, sweet and fibrous', 'তাজা ঋতুর কাঁঠাল, মিষ্টি ও আঁশযুক্ত',
  30, 'kg', 'https://images.unsplash.com/photo-1619566636859-ad7264c1d2c4?w=400&h=300&fit=crop', true, false, 50, '{"legacy_id": "p027", "emoji": "\ud83e\uded2"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '71ea4d3f-2b11-5add-8617-a466e42712ec', 'fruits', 'Mango (Fazli)', 'ফাজলি আম', 'Large fazli mangoes, juicy and sweet', 'বড় ফাজলি আম, রসালো ও মিষ্টি',
  120, 'kg', 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&h=300&fit=crop', true, false, 51, '{"legacy_id": "p047", "emoji": "\ud83e\udd6d"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'b73f2519-81a1-54ed-bd1b-910fa9067603', 'fruits', 'Papaya (Ripe)', 'পেঁপে (পাকা)', 'Ripe papaya, sweet and digestive', 'পাকা পেঁপে, মিষ্টি ও পাচনকারক',
  60, 'kg', 'https://images.unsplash.com/photo-1619566636859-ad7264c1d2c4?w=400&h=300&fit=crop', true, false, 52, '{"legacy_id": "p048", "emoji": "\ud83e\udedb"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'c1c58aca-30ae-59ae-b518-f7e232fcc27f', 'fmcg', 'Signal Toothpaste', 'সিগন্যাল টুথপেস্ট', 'Anti-cavity mint toothpaste, 100g', 'এন্টি-ক্যাভিটি মিন্ট টুথপেস্ট, ১০০গ্রাম',
  70, 'piece', 'https://images.unsplash.com/photo-1600857062245-46e9d2e4bf05?w=400&h=300&fit=crop', true, false, 53, '{"legacy_id": "p028", "emoji": "\ud83e\udea5"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '0864e400-9905-5620-8f17-5eb07733335d', 'fmcg', 'Ariel Washing Powder', 'এরিয়েল ওয়াশিং পাউডার', 'Auto-laundry powder, removes tough stains', 'অটো-লন্ড্রি পাউডার, কঠিন ময়লা মুছে ফেলে',
  240, '500g', 'https://images.unsplash.com/photo-1600857062245-46e9d2e4bf05?w=400&h=300&fit=crop', true, false, 54, '{"legacy_id": "p029", "emoji": "\ud83e\uddfa"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '45809558-ab4d-5269-9775-55d1a83c55ff', 'fmcg', 'Dove Soap', 'ডাভ সাবান', 'Moisturizing beauty bar, 100g', 'ময়েশ্চারাইজিং বিউটি বার, ১০০ গ্রাম',
  45, 'piece', 'https://images.unsplash.com/photo-1600857062245-46e9d2e4bf05?w=400&h=300&fit=crop', true, false, 55, '{"legacy_id": "p030", "emoji": "\ud83e\uddfc"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '05f7b617-5359-5de0-8a1f-cdbf8be9ed7c', 'fmcg', 'Harpic Toilet Cleaner', 'হারপিক টয়লেট ক্লিনার', 'Powerful toilet cleaner, 500ml bottle', 'শক্তিশালী টয়লেট ক্লিনার, ৫০০মিলি বোতল',
  80, 'piece', 'https://images.unsplash.com/photo-1600857062245-46e9d2e4bf05?w=400&h=300&fit=crop', true, false, 56, '{"legacy_id": "p060", "emoji": "\ud83e\uddf4"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '73218e97-e020-5bd1-a891-900bfcd99556', 'fmcg', 'Wheel Washing Powder', 'হুইল ওয়াশিং পাউডার', 'Economical washing powder, tough on stains', 'সাশ্রয়ী ওয়াশিং পাউডার, দাগ দূর করতে কার্যকর',
  100, '500g', 'https://images.unsplash.com/photo-1600857062245-46e9d2e4bf05?w=400&h=300&fit=crop', true, false, 57, '{"legacy_id": "p061", "emoji": "\ud83e\uddfa"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '1bbda1dd-a376-5c72-8af1-a87a7d2b662e', 'beverages', 'Pepsi (2L)', 'পেপসি (২ লিটার)', 'Chilled 2-liter bottle of Pepsi', 'ঠান্ডা করা ২-লিটার পেপসি বোতল',
  90, 'piece', 'https://images.unsplash.com/photo-1543253687-c931c8e01820?w=400&h=300&fit=crop', true, false, 58, '{"legacy_id": "p031", "emoji": "\ud83e\udd64"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '9af160dd-9f22-5a8f-a7d3-c938b5d0e573', 'beverages', 'Fresh Lemon Juice', 'তাজা লেবুর রস', 'Freshly squeezed lemon juice, no preservatives', 'তাজা নিছক লেবুর রস, প্রিজার্ভেটিভ মুক্ত',
  30, '250ml', 'https://images.unsplash.com/photo-1543253687-c931c8e01820?w=400&h=300&fit=crop', true, false, 59, '{"legacy_id": "p032", "emoji": "\ud83c\udf4b"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'ff1276bd-f944-5344-aef6-d42e846761c8', 'beverages', 'Coca-Cola (1.5L)', 'কোকাকোলা (১.৫ লিটার)', 'Chilled 1.5-liter bottle of Coca-Cola', 'ঠান্ডা করা ১.৫-লিটার কোকাকোলা বোতল',
  70, 'piece', 'https://images.unsplash.com/photo-1543253687-c931c8e01820?w=400&h=300&fit=crop', true, false, 60, '{"legacy_id": "p033", "emoji": "\ud83e\udd64"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '0ad4a8b0-56df-59b9-b8db-de3367ba46fd', 'beverages', '7up (2L)', 'সেভেন আপ (২ লিটার)', 'Chilled 2-liter bottle of 7up', 'ঠান্ডা করা ২-লিটার সেভেন আপ বোতল',
  85, 'piece', 'https://images.unsplash.com/photo-1543253687-c931c8e01820?w=400&h=300&fit=crop', true, false, 61, '{"legacy_id": "p049", "emoji": "\ud83e\udd64"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '6027a312-a1a1-5332-afb5-a3f9011d2bc8', 'snacks', 'Parle-G Biscuits', 'পার্ল-জি বিস্কুট', 'India''s favorite glucose biscuits, 100g', 'ভারতের সবচেয়ে প্রিয় গ্লুকোজ বিস্কুট, ১০০গ্রাম',
  20, 'packet', 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=300&fit=crop', true, false, 62, '{"legacy_id": "p034", "emoji": "\ud83c\udf6a"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'a4ed7734-d93c-5c63-9f4c-092ee4e8fcc1', 'snacks', 'Lays Chips', 'লেস চিপস', 'Classic salted chips, 50g', 'ক্লাসিক সল্টেড চিপস, ৫০গ্রাম',
  40, 'packet', 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=300&fit=crop', true, false, 63, '{"legacy_id": "p035", "emoji": "\ud83c\udf5f"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  'b52bb4b3-589f-5b6b-b149-cb662877f448', 'snacks', 'Chicken Momos (Frozen)', 'চিকেন মোমো (ফ্রোজেন)', 'Ready-to-cook chicken momos, 12 pieces', 'রান্নার জন্য প্রস্তুত চিকেন মোমো, ১২টি',
  150, 'packet', 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=300&fit=crop', true, false, 64, '{"legacy_id": "p050", "emoji": "\ud83e\udd5f"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();

INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '4c20248c-0341-52b9-b5c8-75cd85823298', 'snacks', 'Mixed Nut Mix', 'মিক্সড নাট মিক্স', 'Premium roasted mixed nuts, 200g', 'প্রিমিয়াম রোস্টেড মিক্সড বাদাম, ২০০গ্রাম',
  200, 'packet', 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=300&fit=crop', true, false, 65, '{"legacy_id": "p062", "emoji": "\ud83e\udd5c"}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();
