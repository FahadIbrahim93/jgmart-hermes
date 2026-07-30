-- Fix infinite recursion in profiles RLS (run once in SQL Editor)
-- Cause: policies on other tables SELECT from profiles, which re-triggers profiles policies.

CREATE OR REPLACE FUNCTION public.is_staff()
RETURNS BOOLEAN
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.profiles
    WHERE id = auth.uid() AND role IN ('admin', 'operator', 'partner')
  );
$$;

CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.profiles
    WHERE id = auth.uid() AND role = 'admin'
  );
$$;

-- Profiles: replace self-referential admin policy
DROP POLICY IF EXISTS "Admins can view all profiles" ON public.profiles;
CREATE POLICY "Admins can view all profiles"
  ON public.profiles FOR SELECT
  USING (public.is_admin());

-- Categories
DROP POLICY IF EXISTS "Only admins can modify categories" ON public.categories;
CREATE POLICY "Only admins can modify categories"
  ON public.categories FOR INSERT WITH CHECK (public.is_staff());
CREATE POLICY "Only admins can update categories"
  ON public.categories FOR UPDATE USING (public.is_staff());
CREATE POLICY "Only admins can delete categories"
  ON public.categories FOR DELETE USING (public.is_staff());

-- Products (FOR ALL was also applying to SELECT and causing recursion)
DROP POLICY IF EXISTS "Only admins/operators can modify products" ON public.products;
CREATE POLICY "Only admins/operators can insert products"
  ON public.products FOR INSERT WITH CHECK (public.is_staff());
CREATE POLICY "Only admins/operators can update products"
  ON public.products FOR UPDATE USING (public.is_staff());
CREATE POLICY "Only admins/operators can delete products"
  ON public.products FOR DELETE USING (public.is_staff());

-- Orders
DROP POLICY IF EXISTS "Staff can view all orders" ON public.orders;
CREATE POLICY "Staff can view all orders"
  ON public.orders FOR SELECT
  USING (public.is_staff());

DROP POLICY IF EXISTS "Staff can update orders" ON public.orders;
CREATE POLICY "Staff can update orders"
  ON public.orders FOR UPDATE
  USING (public.is_staff());

-- Order items
DROP POLICY IF EXISTS "Order items viewable with order" ON public.order_items;
CREATE POLICY "Order items viewable with order"
  ON public.order_items FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.orders o
      WHERE o.id = order_items.order_id
      AND (auth.uid() = o.customer_id OR public.is_staff())
    )
  );

-- Customers
DROP POLICY IF EXISTS "Staff can manage customers" ON public.customers;
CREATE POLICY "Staff can manage customers"
  ON public.customers FOR ALL
  USING (public.is_staff());

-- Partners
DROP POLICY IF EXISTS "Partners viewable by staff" ON public.partners;
CREATE POLICY "Partners viewable by staff"
  ON public.partners FOR SELECT
  USING (public.is_staff());

DROP POLICY IF EXISTS "Only admins can modify partners" ON public.partners;
CREATE POLICY "Only admins can modify partners"
  ON public.partners FOR INSERT WITH CHECK (public.is_admin());
CREATE POLICY "Only admins can update partners"
  ON public.partners FOR UPDATE USING (public.is_admin());
CREATE POLICY "Only admins can delete partners"
  ON public.partners FOR DELETE USING (public.is_admin());

-- Settings
DROP POLICY IF EXISTS "Only admins can modify settings" ON public.settings;
CREATE POLICY "Only admins can modify settings"
  ON public.settings FOR INSERT WITH CHECK (public.is_admin());
CREATE POLICY "Only admins can update settings"
  ON public.settings FOR UPDATE USING (public.is_admin());
CREATE POLICY "Only admins can delete settings"
  ON public.settings FOR DELETE USING (public.is_admin());

-- Audit log
DROP POLICY IF EXISTS "Admins can view audit log" ON public.audit_log;
CREATE POLICY "Admins can view audit log"
  ON public.audit_log FOR SELECT
  USING (public.is_admin());
