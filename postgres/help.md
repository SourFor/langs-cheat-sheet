# use vars for testing json
```sql
DO $$
DECLARE
output jsonb;
BEGIN
output := '{
  "total": {
    "area": 0.32,
    "products_price": "207,00 ₽",
    "services_price": "144,00 ₽",
    "consumables_price": "56,00 ₽"
  },
  "products": [
    {
      "area": 0.08,
      "count": 2,
      "price": "77,80 ₽",
      "price_of_unit": "38,90 ₽",
      "system_of_units_id": 2,
      "system_of_units_value": "п.м.",
      "metal_structures_type_id": 1,
      "metal_structures_class_id": 1,
      "area_calculation_factor_id": 1,
      "metal_structures_type_name": "10*10",
      "metal_structures_class_name": "труба",
      "metal_structures_product_id": 1,
      "area_calculation_factor_value": 0.04
    },
    {
      "area": 0.24,
      "count": 4,
      "price": "129,20 ₽",
      "price_of_unit": "32,30 ₽",
      "system_of_units_id": 2,
      "system_of_units_value": "п.м.",
      "metal_structures_type_id": 2,
      "metal_structures_class_id": 1,
      "area_calculation_factor_id": 3,
      "metal_structures_type_name": "15*15",
      "metal_structures_class_name": "труба",
      "metal_structures_product_id": 2,
      "area_calculation_factor_value": 0.06
    }
  ],
  "services": [
    {
      "price": "0,00 ₽",
      "service_id": 1,
      "service_name": "сварка",
      "service_price": "30,00 ₽"
    },
    {
      "price": "0,00 ₽",
      "service_id": 2,
      "service_name": "резка",
      "service_price": "10,00 ₽"
    },
    {
      "price": "0,00 ₽",
      "service_id": 3,
      "service_name": "зачистка",
      "service_price": "10,00 ₽"
    },
    {
      "price": "56,00 ₽",
      "service_id": 4,
      "service_name": "малярные работы",
      "service_price": "175,00 ₽"
    },
    {
      "price": "0,00 ₽",
      "service_id": 5,
      "service_name": "гибка",
      "service_price": "10,00 ₽"
    },
    {
      "price": "88,00 ₽",
      "service_id": 6,
      "service_name": "покраска",
      "service_price": "275,00 ₽"
    }
  ],
  "consumables": [
    {
      "price": "32,00 ₽",
      "consumables_id": 1,
      "consumables_name": "краска",
      "consumables_price": "100,00 ₽"
    },
    {
      "price": "24,00 ₽",
      "consumables_id": 2,
      "consumables_name": "электро-энергия",
      "consumables_price": "75,00 ₽"
    }
  ]
}';
SELECT * 
	FROM jsonb_insert(
		output,
		'{total,production_price}',
		(SELECT * FROM to_jsonb((output->'total'->>'products_price')::money + (output->'total'->>'services_price')::money + (output->'total'->>'consumables_price')::money ) )  )
	INTO output;
SELECT * 
	FROM jsonb_insert(
		output,
		'{total,selling_price}',
		(SELECT * FROM to_jsonb((output->'total'->>'production_price')::money * (SELECT sale_calculation_factor_value FROM metal_structures_calculator.sale_calculation_factor WHERE sale_calculation_factor_id=1)) )  )
	INTO output;
raise notice '%', output;
END $$
```