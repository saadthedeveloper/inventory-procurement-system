## 2026-04-30

### 1. What is a migration file

A migration file is a **numbered file** (usually SQL, but could be Python or PHP) that contains DDL commands like `CREATE TABLE` or `ALTER TABLE`, to manage database schema changes in a structured and repeatable way. It lives alongside the application code.

The numbering gives files a strict order. For example, `001_roles.sql` must run before `002_users.sql` because the `users` table depends on `roles`. Running them out of order would cause a database error.

### 2. How migrate.js and the tracking table work

`migrate.js` is a small script that:

- Connects to the database
- Looks inside a `migrations/` folder for `.sql` files (like `001_roles.sql`, `002_users.sql`)
- Checks a **tracking table** (often called `migrations_log`) to see which files already ran
- Runs only the new files in order
- Records each successful run in the tracking table

The tracking table is what prevents the same migration from running twice. The first time you run `migrate.js`, the script creates that tracking table automatically. After that, each migration file is recorded when it succeeds. That is why running the migration script a second time does nothing. The tracking table says "already did that."

### 3. Changing the schema requires new migrations, not edits

Every time you need to change the schema (add a column, change a data type, add an index, drop a table), you write a **new migration file** that contains an `ALTER` statement. You never go back and edit an old migration file that has already been run on production.

The only time editing an old migration is acceptable is during early development before you have a live production database, and you are willing to run `reset` (drop all tables and remigrate). But that is not safe for production.

### 4. Why migrations matter

Not every SQL file is a migration. If you write `everything.sql` and run it manually when you remember, that is just a script. It is hard to repeat and easy to mess up.

A proper migration system is:

- Numbered or timestamped
- Tracked automatically by a script
- Stored in Git
- Never edited after being applied to production

This makes database changes reliable, repeatable, and team friendly. Every developer gets the same database structure with one command.

### Forward Migration

A **forward migration** is a change that moves your database schema **forward** from one version to the next.

Example: `ALTER TABLE users ADD COLUMN phone VARCHAR(20);`

### Backward Migration (Rollback)

A **backward migration** (also called a "down migration") is the **reverse** of a forward migration. It takes the schema **back** to the previous state.

Example: `ALTER TABLE users DROP COLUMN phone;`

### Key points about Migration
- Rollbacks are **rarely used in production** because they can cause data loss.
- Most teams write a **new forward migration** to fix mistakes instead of rolling back.
- During **development only**, you can reset the database and reapply all migrations from scratch.


## 2026-05-3
ON DELETE RESTRICT → you can’t delete a role if any user is using it;
ON UPDATE CASCADE → if a role’s ID changes, it automatically updates in all users.
primary keys rarely change so its optional

## 2026-05-5
- npm init -y is something you usually do when you’re starting a Node.js project in a folder, but it’s not mandatory. What it really does is create that package.json file, which helps Node (and npm) keep track of your project details and any libraries you install.
- if someone else downloads your project, they can just run npm install, and Node will look at package.json and automatically install everything listed there. Without it, they’d have no idea what your project needs to work.
- In JSON:
    - Keys must be in double quotes ("name", not name)
    - Values can only be simple things: strings, numbers, true/false, arrays, or other JSON objects
    - You can’t put functions or logic inside it

# 2026-05-15
You just created a Python virtual environment inside your /server folder. A virtual environment is an isolated container for Python packages. It prevents the libraries you install for this project (Flask, PyMySQL, etc.) from interfering with other Python projects on your computer or system-wide Python.
The venv folder contains its own copy of Python and pip. Activating it with source venv/bin/activate tells your terminal to use this isolated environment instead of the global Python.

#2026-05-15
.env is like a private sticky note where you write down your database password and other secrets that should never be shared publicly. config.py is a small program that reads that sticky note and hands those secrets to the rest of your application so it can log into the database and work properly, keeping your passwords out of your main code and safe from being accidentally uploaded to GitHub.
