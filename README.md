Here is a complete `README.md` for your project. Save it in the project root folder.

```markdown
# Inventory & Procurement Management System

A full‑stack web application for managing inventory, suppliers, purchase orders, and stock movements. Built with **React (Vite)** on the frontend, **Flask** on the backend, and **MySQL** as the database. Designed for a pharmacy use case but generic enough for any small‑business inventory.

## Features

- **Role‑based access** – Admin, Manager, Staff with different permissions.
- **Product management** – CRUD, low‑stock alerts, soft delete.
- **Supplier & category management** – CRUD operations (Admin only).
- **Purchase order workflow** – Manager creates, Admin approves, Staff marks as received.
- **Automatic stock update** – Database triggers increase stock when a purchase order is received.
- **Audit trail** – Every stock change is logged in `stock_movements` (auto‑triggered).
- **Reports** – Stock valuation view, movement history with filters.
- **Dark theme** – Modern, readable UI.

## Tech Stack

| Layer       | Technology                                      |
|-------------|-------------------------------------------------|
| Frontend    | React 18, Vite, Tailwind CSS, React Router, Axios, Lucide Icons |
| Backend     | Python 3.10+, Flask, Flask‑CORS, Flask‑JWT‑Extended, PyMySQL, bcrypt |
| Database    | MySQL 8.0 (with triggers, views, foreign keys) |

## Architecture Overview

- **Frontend** communicates with the Flask REST API (port 5000). JWT tokens are stored in `localStorage` and attached to every request.
- **Backend** provides endpoints for authentication, CRUD operations, and reports. All write operations are protected by role checks.
- **Database** uses triggers to update product stock automatically when a purchase order is marked as received, and to log every stock change in `stock_movements`. Views (`low_stock_alerts`, `stock_valuation`) simplify reporting.

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Node.js 18+ and npm
- MySQL 8.0 (running locally)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/saadthedeveloper/inventory-procurement-system.git
cd inventory-procurement-system
```

### 2. Backend Setup (Flask)

```bash
cd server
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `server/` folder:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=inventory_ms
JWT_SECRET_KEY=your_super_secret_key
FLASK_ENV=development
```

Run database migrations (creates tables, triggers, views):

```bash
python migrate.py
```

Load synthetic data (CSV files):

```bash
python load_data.py
```

Start the backend server:

```bash
python run.py
```

The API will be available at `http://localhost:5000`.

### 3. Frontend Setup (React)

Open a new terminal:

```bash
cd client
npm install
npm run dev
```

The frontend will run at `http://localhost:5173`.

### 4. Login

Use one of the following demo accounts (created by `load_data.py`):

| Email                     | Password       | Role    |
|---------------------------|----------------|---------|
| test@example.com          | password123    | Admin   |
| gkaiser@example.net       | BW&&Q6Spr^&O   | Staff   |
| cwarren@example.net       | (needs reset, see notes) | |

> **Note:** Some users may have `is_active = 0` or plain‑text passwords. Run the following SQL in MySQL Workbench to activate a user and set a known password:
> ```sql
> UPDATE users SET is_active = 1, password = '$2b$12$iPii12gaof90yuWFnlrY3e.KBeYW8OEP8MtP227yjhabBH2gBduUu' WHERE email = 'cwarren@example.net';
> ```
> Then login with password `BW&&Q6Spr^&O`.

### 5. Environment Variables (Backend)

| Variable         | Description                             |
|------------------|-----------------------------------------|
| DB_HOST          | MySQL host (usually localhost)          |
| DB_USER          | MySQL username                          |
| DB_PASSWORD      | MySQL password                          |
| DB_NAME          | Database name (default: inventory_ms)   |
| JWT_SECRET_KEY   | Secret key for signing JWT tokens       |
| FLASK_ENV        | development / production                |

## API Endpoints (Summary)

| Method | Endpoint                                  | Description                     | Access            |
|--------|-------------------------------------------|---------------------------------|-------------------|
| POST   | `/api/auth/login`                         | Login, returns JWT              | public            |
| GET    | `/api/products`                           | List active products            | authenticated     |
| POST   | `/api/products`                           | Create product                  | Admin only        |
| GET    | `/api/products/low-stock`                 | Low stock alerts                | authenticated     |
| GET    | `/api/categories`                         | List categories                 | authenticated     |
| POST   | `/api/categories`                         | Create category                 | Admin only        |
| GET    | `/api/units`                              | List units                      | authenticated     |
| GET    | `/api/suppliers`                          | List suppliers                  | authenticated     |
| POST   | `/api/purchase-orders`                    | Create purchase order           | Manager/Admin     |
| PUT    | `/api/purchase-orders/<id>/approve`       | Approve order                   | Admin only        |
| PUT    | `/api/purchase-orders/<id>/receive`       | Mark order as received          | authenticated     |
| GET    | `/api/reports/stock-valuation`            | Stock valuation report          | authenticated     |
| GET    | `/api/reports/movement-history`           | Movement history (with filters) | authenticated     |

## Folder Structure

```
inventory-procurement-system/
├── client/                 # React frontend
│   ├── src/
│   │   ├── api/            # Axios instance
│   │   ├── components/     # DataTable, FormRenderer, Sidebar, etc.
│   │   ├── context/        # AuthContext
│   │   ├── pages/          # Login, Dashboard, Products, etc.
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── server/                 # Flask backend
│   ├── app/
│   │   ├── routes/         # Blueprints (auth, products, etc.)
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── db.py
│   ├── migrations/         # SQL migration files (001_roles.sql ... 012_views.sql)
│   ├── csv_data/           # Synthetic CSV data
│   ├── migrate.py          # Runs migrations
│   ├── load_data.py        # Loads CSV data into MySQL
│   ├── run.py
│   └── requirements.txt
└── docs/                   # Documentation (ERD, dataflow, normalization)
```

## Database Triggers & Views

- **`update_stock_on_receive`** – After a purchase order status changes to `'received'`, adds `quantity_received` to product stock.
- **`log_stock_movement`** – After any update to `products.quantity`, inserts a record into `stock_movements`.
- **`low_stock_alerts` view** – Products with `quantity < reorder_level`.
- **`stock_valuation` view** – Product name, quantity, unit price, and total value.

## Testing the System

1. **Log in** as Admin (`test@example.com` / `password123`).
2. **Create a product**, a category, a supplier.
3. **Create a purchase order** (Manager or Admin).
4. **Approve** the order (Admin).
5. **Mark as received** – stock will increase automatically.
6. **Check low stock alerts** and **reports**.

## Deployment

- **Backend** (Railway / PythonAnywhere / your own server):
  - Set environment variables, attach a MySQL database.
  - Run `migrate.py` and `load_data.py` once.
  - Use a production WSGI server (e.g., `gunicorn`).
- **Frontend** (Vercel / Netlify):
  - Build with `npm run build` and deploy the `dist` folder.
  - Update `api/client.js` with your production backend URL.

## Future Improvements

- Add pagination and sorting to tables.
- Real‑time notifications for low stock.
- Export reports to PDF/Excel.
- Multi‑warehouse support.
- Optimistic locking for concurrent stock updates.

## License

MIT

## Acknowledgements

- Built as a final project for Database Systems lab (BSCS).
- Special thanks to the instructor for guidance.

---

**Happy inventory managing!**
```
