-- Run AFTER creating admin user in Supabase Dashboard → Authentication → Users
-- Replace the email below with your admin email, then run in SQL Editor.

-- Example: create profile for admin@jgmartbd.com
INSERT INTO public.profiles (id, email, full_name, role)
SELECT id, email, 'JG Mart Admin', 'admin'
FROM auth.users
WHERE email = 'admin@jgmartbd.com'
ON CONFLICT (id) DO UPDATE SET role = 'admin', full_name = EXCLUDED.full_name;
