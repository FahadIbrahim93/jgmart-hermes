-- Fix generate_order_number RPC to handle non-JG- prefixed order numbers
-- (e.g., "PC-004" from Cursor testing)
-- This was broken because it tried to CAST order_number suffix to integer
-- without handling non-numeric values.

CREATE OR REPLACE FUNCTION public.generate_order_number()
RETURNS text
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  max_num integer;
  new_num integer;
BEGIN
  -- Try to get max number from JG- prefixed orders
  BEGIN
    SELECT COALESCE(MAX(CAST(SUBSTRING(order_number FROM 5) AS INTEGER)), 0)
    INTO max_num
    FROM public.orders
    WHERE order_number LIKE 'JG-%';
  EXCEPTION WHEN OTHERS THEN
    -- If parsing fails (e.g., "PC-004"), start from 1
    max_num := 0;
  END;
  
  new_num := max_num + 1;
  RETURN 'JG-' || LPAD(new_num::text, 5, '0');
END;
$$;
