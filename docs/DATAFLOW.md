## Dataflow Description

Data enters my system in three ways:

- First, an admin or manager can enter data manually through the website forms. For example, they add a new product, register a supplier, or create a user account. The frontend sends this data to the backend API, and the backend saves it in the correct table.

- Second, the system generates data automatically. When a staff member marks a purchase order as "received", the database triggers run. They update the product quantity and write a record in the stock movements table. Nobody types that data. It happens by itself.

- Third, I loaded initial fake data using CSV files. I ran a Python script that read the CSV files and inserted rows into all tables. This gave me realistic data to start with, like 100 products and 50 suppliers.

How data moves between tables:

- The `users` table depends on `roles`. You cannot create a user without a role.
- `products` depends on `categories` and `units`. A product must have a category and a unit.
- `purchase_orders` depends on `suppliers` and `users` (who created it).
- `purchase_order_items` depends on `purchase_orders` and `products`.
- `product_suppliers` links products and suppliers. It depends on both.
- `stock_movements` depends on `products` and sometimes `users`.

When a purchase order is created, data goes into `purchase_orders` and `purchase_order_items`. When it is approved, the `status` column changes. When it is marked as received, the stock quantity in `products` increases and a new row appears in `stock_movements`. This is the main flow of data.
The output from the system includes low stock alerts (from the `low_stock_alerts` view), a stock valuation report (from `stock_valuation` view), and a movement history report (directly from `stock_movements` table). These outputs help the pharmacy manager make decisions. 
No data goes outside the system except through these reports. There is no external API or data export for now.
