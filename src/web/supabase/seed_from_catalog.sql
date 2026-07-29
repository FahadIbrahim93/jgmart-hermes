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
