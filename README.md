# Fruad Apps Sehar

FruadApps-Sehar is an application for analysing app reviews and potentially fraudulent apps.

![Flask](https://img.shields.io/badge/Flask-2563EB?style=flat-square) ![MySQL](https://img.shields.io/badge/MySQL-0F172A?style=flat-square)

## Overview

The Flask implementation is organized around the entry points and modules below.

## Implemented workflows

The source defines these handlers:

- **Index** — `index`
- **Login** — `login`
- **Admin Dashboard** — `admin_dashboard`
- **Delete Fake Review** — `delete_fake_review`
- **Admin Reviews** — `admin_reviews`
- **Add Application** — `add_application`
- **View Applications** — `view_applications`
- **Toggle App Status** — `toggle_app_status`
- **Edit Application** — `edit_application`
- **Delete Application** — `delete_application`
- **Register** — `register`
- **User Login** — `user_login`

## Getting started

### 1. Get the project

```bash
git clone https://github.com/nasirabbas827/FruadApps-Sehar.git
cd FruadApps-Sehar
```

### 2. Prepare Python

Create an isolated environment:

```bash
python -m venv .venv
```

Activate it with `.venv\Scripts\activate` on Windows Command Prompt, or `source .venv/bin/activate` on macOS/Linux.

No requirements file is included. The inspected Python imports indicate these dependencies as a starting point:

```bash
python -m pip install Flask-Mail Werkzeug Flask Flask-MySQLdb textblob nltk
```

Dependency versions are not pinned in this repository.

### 3. Configure and run

Import [`Database/fraudapps_db.sql`](Database/fraudapps_db.sql) and set the local database connection in the application configuration before starting.

Run from the repository root so relative file paths resolve correctly:

```bash
python app.py
```

Open http://127.0.0.1:5000/, or use the address printed by the application.

## Repository guide

| Path | Purpose |
| --- | --- |
| [`Database`](Database) | Database scripts |
| [`app.py`](app.py) | Application entry point |
| [`static`](static) | Static application assets |
| [`templates`](templates) | HTML page templates |

## Development notes

These setup instructions are based on the repository source. The application has not been executed as part of this documentation update; verify dependencies and configuration in your local environment.
