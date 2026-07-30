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
