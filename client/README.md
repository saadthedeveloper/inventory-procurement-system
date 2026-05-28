# Inventory Pro — React Frontend

A complete dark-themed React frontend for the Inventory Management System.

## Tech Stack

- **React 18** with Vite
- **Tailwind CSS** (dark mode)
- **React Router v6**
- **Axios** for API calls
- **Lucide React** for icons

## Folder Structure

```
client/
  src/
    api/
      client.js           # Axios instance with auth interceptor
    components/
      DataTable.jsx        # Reusable searchable table
      FormRenderer.jsx     # Schema-driven modal form
      Navbar.jsx           # Top bar
      ProtectedRoute.jsx   # Auth guard component
      Sidebar.jsx          # Navigation sidebar
    context/
      AuthContext.jsx      # Auth state (login/logout/user)
    pages/
      Login.jsx
      Dashboard.jsx        # Stats cards + low stock alerts
      Products.jsx         # Full CRUD
      Suppliers.jsx        # Full CRUD
      Categories.jsx       # Full CRUD
      PurchaseOrders.jsx   # Create / Approve / Receive
      Reports.jsx          # Stock valuation + movement history
    App.jsx                # Router + layout
    main.jsx
    index.css              # Tailwind directives
```

## Setup

1. **Install dependencies:**
   ```bash
   cd client
   npm install
   ```

2. **Start the backend** on port 5000 (Flask API).

3. **Run the dev server:**
   ```bash
   npm run dev
   ```

4. Open [http://localhost:5173](http://localhost:5173)

## Roles

| Role ID | Name    | Permissions                              |
|---------|---------|------------------------------------------|
| 1       | Admin   | Full access (CRUD, approve POs)          |
| 2       | Manager | Create POs, view all                     |
| 3       | Staff   | View only, receive approved POs          |

## API Base URL

The frontend connects to `http://localhost:5000/api` by default.
To change it, edit `src/api/client.js`.
