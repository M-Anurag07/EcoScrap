# Database Design - EcoScrap

## collectors
- id, preferred_language, area, pin_hash, created_at

## material_categories
- id, name, hazard_level (low / medium / high), description

## recyclers
- id, name, address, lat, lng, authorization_number,
  authorization_status, phone, pickup_available, service_radius_km

## recycler_rates
- id, recycler_id, category_id, rate_per_kg, updated_at

## lots
- id, lot_ref, collector_id, category_id, description, image_path,
  weight_kg, condition, estimated_value, lat, lng, status, created_at

## price_history
- id, category_id, location, date, buying_price, quoted_price,
  unit, recycler_id

## transactions
- id, lot_id, recycler_id, quoted_price, final_price,
  payment_status, status, created_at

## handovers
- id, lot_id, reference_code, photo_path, weight_kg,
  gps_lat, gps_lng, handed_over_at, recycler_confirmed_at

## end_of_life_guidance
- id, category_id, step_order, action_type
  (reuse / refurbish / harvest_parts / recycle / safe_disposal),
  text_en, text_hi, text_mr, audio_path