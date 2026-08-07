-- Rewrite create_public_order to price server-side from the products table.
--
-- The old version accepted client-supplied subtotal/delivery_fee/total and
-- item prices, inserting them verbatim — a direct fraud path (anyone with the
-- public anon key could call this RPC and insert orders at ৳1 each).
--
-- This version:
--   1. Accepts only item_id (legacy catalog id) + qty per line.
--   2. Looks up the current price from the products table.
--   3. Computes subtotal, delivery_fee, and total server-side.
--   4. Validates customer fields and rejects unknown products.
--
-- Run in Supabase SQL Editor. The client (db.js) must be updated to send the
-- new item format {product_id, qty} and must no longer send price/total fields.

CREATE OR REPLACE FUNCTION public.create_public_order(
  p_order_number text,
  p_customer_name text,
  p_customer_phone text,
  p_customer_building text,
  p_customer_flat text,
  p_delivery_slot text DEFAULT 'morning',
  p_delivery_date date DEFAULT NULL,
  p_items jsonb DEFAULT '[]'::jsonb,
  p_payment_method text DEFAULT 'cash'
)
RETURNS public.orders
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  new_order public.orders;
  subtotal integer := 0;
  delivery_fee integer := 0;
  item record;
  product_row public.products%ROWTYPE;
  fee_setting jsonb;
BEGIN
  -- Validate payment method
  IF p_payment_method NOT IN ('cash', 'bkash', 'nogod', 'rocket') THEN
    RAISE EXCEPTION 'invalid payment method';
  END IF;

  -- Validate customer fields
  IF p_customer_phone IS NULL OR p_customer_phone = '' THEN
    RAISE EXCEPTION 'customer phone required';
  END IF;
  IF p_customer_building IS NULL OR p_customer_building = '' THEN
    RAISE EXCEPTION 'customer building required';
  END IF;

  -- Validate items
  IF p_items IS NULL OR jsonb_array_length(p_items) = 0 THEN
    RAISE EXCEPTION 'no items';
  END IF;

  -- Look up delivery fee from settings (default 30 BDT)
  SELECT value INTO fee_setting FROM public.settings WHERE key = 'delivery_fee_bdt';
  delivery_fee := COALESCE((fee_setting::integer), 30);

  -- Compute subtotal from product prices (ignore any client-sent price).
  -- item_id is the legacy catalog id (e.g. "p001") stored in products.metadata.legacy_id.
  FOR item IN SELECT * FROM jsonb_array_elements(p_items) LOOP
    IF NOT ((item->>'qty')::integer > 0) THEN
      RAISE EXCEPTION 'invalid qty for item';
    END IF;

    SELECT * INTO product_row FROM public.products
    WHERE (metadata->>'legacy_id') = item->>'product_id'
    LIMIT 1;

    IF product_row.id IS NULL THEN
      RAISE EXCEPTION 'product not found: %', item->>'product_id';
    END IF;

    subtotal := subtotal + (product_row.price * (item->>'qty')::integer);
  END LOOP;

  INSERT INTO public.orders (
    order_number, customer_name, customer_phone, customer_building, customer_flat,
    delivery_slot, delivery_date, items, subtotal, delivery_fee, total, payment_method, status
  ) VALUES (
    p_order_number, p_customer_name, p_customer_phone, p_customer_building, p_customer_flat,
    p_delivery_slot, COALESCE(p_delivery_date, CURRENT_DATE), p_items, subtotal, delivery_fee, subtotal + delivery_fee, p_payment_method, 'pending'
  )
  RETURNING * INTO new_order;

  RETURN new_order;
END;
$$;

GRANT EXECUTE ON FUNCTION public.create_public_order TO anon, authenticated;