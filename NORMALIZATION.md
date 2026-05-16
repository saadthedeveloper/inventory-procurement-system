# Normalization – Inventory & Procurement System

## Introduction
I checked all tables in my database. I applied First Normal Form (1NF), Second Normal Form (2NF), and Third Normal Form (3NF). For each table I write why it is okay or if I changed something.

## Table 1: roles

**1NF**  
All values are single (atomic). `id` is integer, `name` is string. No repeating groups. Primary key `id` exists. So 1NF is satisfied.

**2NF**  
Primary key is only one column (`id`). There is no partial dependency. So 2NF is satisfied.

**3NF**  
All non-key columns (`name`) depend only on the primary key (`id`). No column depends on another non-key column. So 3NF is satisfied.

## Table 2: users

**1NF**  
All columns have atomic values. No repeating groups. Primary key `id`. Satisfies 1NF.

**2NF**  
Single-column primary key. No partial dependency. Satisfies 2NF.

**3NF**  
Non-key columns: `name`, `email`, `password`, `role_id`, `is_active`, `created_at`.  
All depend only on `id`. `role_id` is a foreign key but it depends on `id`, not on another non-key column. So 3NF is satisfied.


## Table 3: categories

**1NF**  
Primary key `id`. `name` is atomic. No repeating groups. Satisfies 1NF.

**2NF**  
Single-column PK → no partial dependency. Satisfies 2NF.

**3NF**  
Only non-key column `name` depends only on `id`. No transitive dependency. Satisfies 3NF.


## Table 4: units

**1NF**  
`id` PK, `name` atomic. Satisfies 1NF.

**2NF**  
Single-column PK → no partial dependency. Satisfies 2NF.

**3NF**  
`name` depends only on `id`. Satisfies 3NF.

## Table 5: products

**1NF**  
All columns atomic. `id` PK. No repeating groups. Satisfies 1NF.

**2NF**  
Single-column PK → no partial dependency. Satisfies 2NF.

**3NF**  
Non-key columns: `name`, `sku`, `category_id`, `unit_id`, `quantity`, `reorder_level`, `unit_price`, `is_active`, `created_at`.  
Each depends only on `id`. Foreign keys (`category_id`, `unit_id`) are not dependent on other non-key columns. So 3NF is satisfied.


## Table 6: suppliers

**1NF**  
`id` PK. All atomic values. Satisfies 1NF.

**2NF**  
Single-column PK → no partial dependency. Satisfies 2NF.

**3NF**  
Non-key columns: `name`, `contact_person`, `email`, `phone`, `payment_terms`, `is_active`, `created_at`.  
All depend only on `id`. No transitive dependency. Satisfies 3NF.


## Table 7: product_suppliers

**1NF**  
`id` PK. All values atomic. No repeating groups. Satisfies 1NF.

**2NF**  
Primary key is `id` (surrogate key). There is no composite key, so partial dependency is impossible. Satisfies 2NF.

**3NF**  
Non-key columns: `product_id`, `supplier_id`, `unit_cost`, `is_preferred`.  
All depend only on `id`. The unique constraint on `(product_id, supplier_id)` is not a dependency issue. So 3NF is satisfied.


## Table 8: purchase_orders

**1NF**  
`id` PK. Atomic values. No repeating groups. Satisfies 1NF.

**2NF**  
Single-column PK → no partial dependency. Satisfies 2NF.

**3NF**  
Non-key columns: `supplier_id`, `created_by`, `approved_by`, `approved_at`, `status`, `notes`, `created_at`, `updated_at`.  
All depend only on `id`. Foreign keys point to other tables but that is fine. No column depends on another non-key column. So 3NF is satisfied.


## Table 9: purchase_order_items

**1NF**  
`id` PK. Atomic values. No repeating groups. Satisfies 1NF.

**2NF**  
Single-column PK → no partial dependency. Satisfies 2NF.

**3NF**  
Non-key columns: `purchase_order_id`, `product_id`, `quantity_ordered`, `quantity_received`, `unit_cost`.  
All depend only on `id`. No transitive dependency. Satisfies 3NF.


## Table 10: stock_movements

**1NF**  
`id` PK. Atomic values. No repeating groups. Satisfies 1NF.

**2NF**  
Single-column PK → no partial dependency. Satisfies 2NF.

**3NF**  
Non-key columns: `product_id`, `user_id`, `quantity_before`, `quantity_after`, `reason`, `changed_at`.  
All depend only on `id`. No transitive dependency. Satisfies 3NF.


## Conclusion
My database satisfies 1NF, 2NF, and 3NF. No changes were needed because I designed the schema correctly from the beginning. I have documented the justification for each table.
