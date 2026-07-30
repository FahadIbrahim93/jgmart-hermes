-- Public order intake (WhatsApp MVP — no customer login)
-- Run AFTER schema.sql if policies are missing
--
-- NOTE: Supabase anon REST inserts into `orders` are blocked by RLS even with a
-- permissive INSERT policy (WITH CHECK true). The reliable fix is a SECURITY
-- DEFINER RPC function that performs the insert inside a DEFINER context.
-- The policy below is kept for defense-in-depth; the RPC is what db.js calls.

-- Permissive policy (allows anon/authenticated INSERT)
DROP POLICY IF EXISTS "Anyone can create orders" ON public.orders;
CREATE POLICY "Anyone can create orders"
  ON public.orders FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

DROP POLICY IF EXISTS "Anyone can create order items" ON public.order_items;
CREATE POLICY "Anyone can create order items"
  ON public.order_items FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

-- SECURITY DEFINER function: bypasses anon RLS for the insert while keeping
-- app-layer validation in db.js. Called via supabase.rpc('create_public_order').
CREATE OR REPLACE FUNCTION public.create_public_order(
  p_order_number text,
  p_customer_name text,
  p_customer_phone text,
  p_customer_building text,
  p_customer_flat text,
  p_delivery_slot text DEFAULT 'morning',
  p_delivery_date date DEFAULT NULL,
  p_items jsonb DEFAULT '[]'::jsonb,
  p_subtotal integer DEFAULT 0,
  p_delivery_fee integer DEFAULT 0,
  p_total integer DEFAULT 0,
  p_payment_method text DEFAULT 'cash',
  p_status text DEFAULT 'pending'
)
RETURNS public.orders
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  new_order public.orders;
BEGIN
  INSERT INTO public.orders (
    order_number, customer_name, customer_phone, customer_building, customer_flat,
    delivery_slot, delivery_date, items, subtotal, delivery_fee, total, payment_method, status
  ) VALUES (
    p_order_number, p_customer_name, p_customer_phone, p_customer_building, p_customer_flat,
    p_delivery_slot, COALESCE(p_delivery_date, CURRENT_DATE), p_items, p_subtotal, p_delivery_fee, p_total, p_payment_method, p_status
  )
  RETURNING * INTO new_order;
  RETURN new_order;
END;
$$;

GRANT EXECUTE ON FUNCTION public.create_public_order TO anon, authenticated;
