# Inventory & Procurement System — MVP TODO

## Phase 0: Project Setup (Flask Migration)

- [X] Remove Node.js artifacts from `/server` (`package.json`, `package-lock.json`, `.gitkeep`)
- [X] Update `README.md` to reflect Python/Flask instead of Node.js
- [ ] Update `DEVLOG.md` with decision to switch to Flask (reason: course requirement + AI readiness)
- [X] Verify Python 3.10+ is installed (`python3 --version`)
- [X] Create Python virtual environment in `/server`: `python3 -m venv venv`
- [X] Activate virtual environment (`source venv/bin/activate` or `venv\Scripts\activate`)
- [X] Install dependencies: `flask`, `flask-cors`, `flask-jwt-extended`, `pymysql`, `bcrypt`, `python-dotenv`
- [X] Run `pip freeze > requirements.txt`
- [X] Add `venv/`, `__pycache__/`, `*.pyc` to root `.gitignore`

## Phase 1: Database Migrations & Schema

- [ ] Create folder structure in `/server`:
  - [ ] `app/`
  - [ ] `app/routes/`
  - [ ] `app/__init__.py`
  - [ ] `app/config.py`
  - [ ] `app/db.py`
  - [ ] `run.py`
  - [ ] `.env`
  - [ ] `.env.example`
- [ ] Write `app/config.py` to load environment variables
- [ ] Write `app/db.py` with `get_connection()` using `pymysql`
- [ ] Write `run.py` entry point with Flask app factory
- [ ] Write `migrate.py` that:
  - [ ] Creates database if not exists
  - [ ] Creates `migrations_log` tracking table
  - [ ] Runs all `.sql` files in `/server/migrations/` in order, skipping already run ones
- [ ] Run `python migrate.py` – verify 10 tables created
- [ ] Write `011_triggers.sql` (stock update on PO received + stock movement logging)
- [ ] Write `012_views.sql` (`low_stock_alerts` and `stock_valuation`)
- [ ] Run `python migrate.py` again – verify triggers and views added
- [ ] Create `/server/seeds/` folder
- [ ] Write seed JSON files: `roles.json`, `categories.json`, `units.json`, `suppliers.json`, `products.json`, `users.json`
- [ ] Write `seed.py` that reads JSON files and inserts data into tables in correct order
- [ ] Run `python seed.py` – verify data in MySQL Workbench

## Phase 2: Backend API Routes

- [ ] Write `app/routes/auth.py` with `/api/auth/login` endpoint (JWT creation)
- [ ] Register auth blueprint in `app/__init__.py`
- [ ] Test login endpoint with Postman (get token)
- [ ] Write `app/routes/products.py` (CRUD + `/low-stock` endpoint)
- [ ] Write `app/routes/categories.py` (CRUD)
- [ ] Write `app/routes/units.py` (CRUD)
- [ ] Write `app/routes/suppliers.py` (CRUD)
- [ ] Write `app/routes/purchase_orders.py`:
  - [ ] Create PO with line items (transaction)
  - [ ] Update status to approved (admin only)
  - [ ] Mark as received (triggers stock update)
- [ ] Write `app/routes/reports.py`:
  - [ ] `/stock-valuation` (query `stock_valuation` view)
  - [ ] `/movement-history` (query `stock_movements` with filters)
- [ ] Add `@jwt_required()` to all protected routes
- [ ] Add role‑based authorization (admin vs manager vs staff) using custom decorator or helper
- [ ] Test every endpoint in Postman end‑to‑end (login → token → CRUD → PO workflow → stock update → reports)

## Phase 3: Frontend (React + Vite)

- [ ] Install Tailwind CSS in `/client`
- [ ] Create folder structure: `pages/`, `components/`, `schemas/`, `api/`
- [ ] Write `api/client.js` with Axios instance pointing to Flask backend
- [ ] Create `AuthContext` (store token, user info, login/logout functions)
- [ ] Build `Login` page (email/password form, calls `/api/auth/login`)
- [ ] Build reusable `Sidebar` and `Navbar` components
- [ ] Build `FormRenderer` component (schema‑driven forms)
- [ ] Build `DataTable` component (reusable table with sorting/search)
- [ ] Write schemas: `productSchema`, `supplierSchema`, `userSchema`
- [ ] Build `Dashboard` page (summary cards + low stock list)
- [ ] Build `Products` page (list, add, edit, soft delete)
- [ ] Build `Suppliers` page (list, add, edit)
- [ ] Build `Categories` page (simple CRUD)
- [ ] Build `PurchaseOrders` page:
  - [ ] List all POs with status badges
  - [ ] Create PO (select supplier, add line items)
  - [ ] Admin approval button
  - [ ] Staff “mark received” button with quantity input
- [ ] Build `Reports` page (stock valuation table + movement history with date filter)
- [ ] Connect all pages to real API calls (replace mock data)

## Phase 4: Testing & Acceptance

- [ ] Run full Hassan scenario:
  - [ ] Login as Bilal (staff) → view dashboard (low stock)
  - [ ] Login as Sara (manager) → create purchase order
  - [ ] Login as Hassan (admin) → approve purchase order
  - [ ] Login as Bilal (staff) → mark order as received, enter received quantities
  - [ ] Verify product quantities increased
  - [ ] Verify stock movement logged
  - [ ] Run low stock report → updated
  - [ ] Run stock valuation report → correct totals
- [ ] Fix any bugs found

## Phase 5: Deployment & Documentation

- [ ] Update `README.md`:
  - [ ] Screenshot of running app
  - [ ] Tech stack (Flask, React, MySQL)
  - [ ] Step‑by‑step setup (clone, venv, install, migrate, seed, run)
  - [ ] Link to ERD in `/docs`
- [ ] Write `ARCHITECTURE.md` explaining key decisions (triggers vs app‑logic, schema‑driven forms, JWT, views)
- [ ] Add SQL comments to all triggers and views in migration files
- [ ] Deploy backend to Railway (set environment variables, attach MySQL)
- [ ] Deploy frontend to Vercel (point to Railway backend URL)
- [ ] Update `DEVLOG.md` with final summary (challenges, solutions, time taken)
- [ ] Final commit: `git add . && git commit -m "feat: MVP complete - inventory & procurement system" && git push`

## Completion Criteria

- [ ] All checklist items marked done
- [ ] Deployed application accessible via live URL
- [ ] Professor can clone, run, and use the system without errors
- [ ] Hassan scenario works 100%
