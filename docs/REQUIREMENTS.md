# Requirements — MVP

## Business Context
A generic inventory and procurement management system,
demonstrated for a pharmacy use case.

## Functional Requirements
- Staff can log in with email and password
- Each user has a role
- Different roles have different levels of access
- Admin can manage users, products, categories, units, and suppliers
- System displays an alert when stock drops below reorder level
- Manager can create and submit purchase orders to suppliers
- Admin can approve or cancel purchase orders
- Staff can mark a delivery as received
- Stock quantity updates automatically when a delivery is confirmed
- Every stock change is logged with timestamp
- Admin can view stock valuation and movement history reports

## Non-Functional Requirements
- Passwords must be encrypted
- All routes protected, only logged in users can access the system
- Must run in a modern web browser
