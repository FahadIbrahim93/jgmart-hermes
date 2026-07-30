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
