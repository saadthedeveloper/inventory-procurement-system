## April 30, 2026

### Understanding Migration Files

A migration file is a numbered file—typically SQL, though it can be written in Python or PHP—that contains DDL (Data Definition Language) commands such as `CREATE TABLE` or `ALTER TABLE`. These files manage database schema changes in a structured, repeatable manner and are version-controlled alongside application code.

The numbering system enforces strict execution order. For instance, `001_roles.sql` must execute before `002_users.sql` because the `users` table has a foreign key dependency on `roles`. Executing migrations out of sequence would trigger database constraint errors.

### How Migration Scripts and Tracking Tables Work

`migrate.js` is a lightweight script that orchestrates the migration process:

- Establishes a database connection
- Scans the `migrations/` directory for `.sql` files (e.g., `001_roles.sql`, `002_users.sql`)
- Queries a tracking table (commonly named `migrations_log`) to identify previously executed migrations
- Executes only new migration files in numerical order
- Records each successful migration in the tracking table

The tracking table serves as a safeguard against duplicate execution. On first run, `migrate.js` automatically creates this table. Subsequently, each migration is logged upon successful completion. This is why re-running the migration script has no effect—the tracking table indicates that all migrations have already been applied.

### Schema Changes Require New Migrations

When modifying the database schema—whether adding columns, changing data types, creating indexes, or dropping tables—you must create a new migration file containing the appropriate `ALTER` statement. Never modify an existing migration file that has been executed in production.

The only exception is during early development, before production deployment, when you can safely reset the database (drop all tables and re-migrate). However, this approach is never appropriate for production environments.

### Why Migrations Matter

Not all SQL files qualify as migrations. A manually executed `everything.sql` script lacks repeatability and is error-prone.

A proper migration system is:

- Numbered or timestamped for clear sequencing
- Tracked automatically through scripts
- Version-controlled in Git
- Immutable once applied to production

This approach makes database changes reliable, repeatable, and team-friendly. Every developer can achieve identical database structure with a single command.

### Forward and Backward Migrations

**Forward migrations** advance your database schema from one version to the next.

Example: `ALTER TABLE users ADD COLUMN phone VARCHAR(20);`

**Backward migrations** (also called "down migrations" or "rollbacks") reverse a forward migration, returning the schema to its previous state.

Example: `ALTER TABLE users DROP COLUMN phone;`

**Important considerations:**
- Rollbacks are rarely used in production due to potential data loss
- Teams typically write new forward migrations to address mistakes rather than rolling back
- During development only, you can reset the database and reapply all migrations from scratch

---

## May 3, 2026

### Foreign Key Constraints

`ON DELETE RESTRICT` prevents deletion of a role if any user references it, maintaining referential integrity.

`ON UPDATE CASCADE` automatically propagates changes when a role's ID is modified, updating all dependent user records.

Note: Primary keys rarely change in practice, making `ON UPDATE CASCADE` optional in most cases.

---

## May 5, 2026

### Understanding package.json

Running `npm init -y` when starting a Node.js project creates a `package.json` file. While not strictly mandatory, this file serves as the project's manifest, tracking metadata and dependencies.

When another developer clones your project, they can simply run `npm install`, and Node will reference `package.json` to automatically install all required libraries. Without this file, there's no record of project dependencies.

### JSON Syntax Rules

In JSON:
- Keys must use double quotes (`"name"`, not `name`)
- Values are limited to primitives: strings, numbers, booleans, arrays, or nested objects
- Functions and executable logic are not permitted

---

## May 15, 2026

### Python Virtual Environments

A virtual environment is an isolated Python environment specific to a single project. Creating a `venv` folder in your `/server` directory prevents library conflicts between projects and avoids polluting the system-wide Python installation.

The `venv` folder contains its own Python interpreter and pip package manager. Activating it with `source venv/bin/activate` instructs your shell to use this isolated environment rather than the global Python installation.

### Configuration Management

`.env` is a private configuration file containing sensitive information like database credentials and API keys that should never be committed to version control.

`config.py` reads the `.env` file and exposes these secrets to your application securely, keeping credentials out of source code and preventing accidental exposure through Git.

### Environment Variables

Environment variables are dynamic key-value pairs stored outside application source code that configure running processes.

**`.env`**: Contains actual environment variables—database credentials, JWT secret keys, and application settings. This file is excluded from version control and must never be committed.

**`.env.example`**: A template documenting required variable names without actual values. This file is committed to the repository to guide configuration.

### Project Structure Components

**`requirements.txt`**: Lists all Python dependencies for the project. Running `pip install -r requirements.txt` installs the exact package versions needed, ensuring consistency across development environments.

**`config.py`**: Loads environment variables from `.env` and makes them accessible throughout the application.

**`db.py`**: Provides a database connection helper. Any module requiring database access imports this file.

**`run.py`**: The application entry point. Running this file starts the Flask server and binds it to port 5000.

**`app/__init__.py`**: The Flask application factory. This file configures CORS (enabling frontend-backend communication), JWT authentication (for token-based auth), and registers API route blueprints.
