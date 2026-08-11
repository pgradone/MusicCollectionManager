# Master Prompt — Music Collection Manager

I want you to help me build a **professional Windows desktop Music Collection Manager in Python** for my existing SQLite database, `Musi.db`.

## Core Technology

Use:

* **Python**
* **PySide6 / Qt** for the GUI
* **SQLite**
* Clean **MVC/layered architecture**
* Qt Designer `.ui` files where useful

Use this architecture:

```text
GUI → Controller → Repository → SQLite
```

The GUI must **never access SQLite directly**.

The application should eventually be packageable as a standalone Windows `.exe`, requiring no Python installation.

## Existing Database

`Musi.db` is an existing relational music database. Do **not** redesign it or replace it with a generic database.

The main entities include:

* Artists
* Songs
* Records
* Programs
* Styles
* BPM
* Discogs

Important relationship/junction tables include:

* Sing
* Contain
* Belong
* Schedule

The application must understand the existing schema, primary keys, foreign keys, and relationships.

Do not make users work directly with junction tables. Instead, provide user-friendly relationship editors.

For example:

* Song → Artists
* Song → Styles
* Song → Records
* Song → Programs
* Record → Tracks
* Record → Discogs

Use meaningful names instead of displaying raw foreign-key IDs wherever possible.

## Main Features

Build a professional database application with:

* Dashboard
* Navigation sidebar
* CRUD screens
* Search
* Filtering
* Sorting
* Create / Edit / Delete / Duplicate
* Relationship management
* Reports
* CSV/Excel/PDF export
* Backup and recovery
* Light/dark themes
* Logging
* Error handling
* Transactions and rollback
* Data validation
* Status bar
* Keyboard shortcuts where useful

### Song Editor

Include:

```text
General
Artists
Styles
Records
Programs
```

### Record Editor

Include:

```text
General
Tracks
Artists
Discogs
```

Track management must support adding, removing, and reordering tracks while maintaining the underlying relationship data.

### Program Editor

Provide playlist management with:

* Position
* Song
* Artist
* Record
* Year
* BPM
* Duration

Allow songs to be inserted, removed, reordered, and automatically renumbered.

## Dashboard

Show useful collection statistics such as:

* Artists
* Songs
* Records
* Programs
* Styles
* Average BPM
* Collection value
* Recently added items
* Missing metadata

## Search & Reports

Provide global search across relevant entities.

Eventually provide reports such as:

* Songs per artist
* Records per artist
* Songs by style
* Missing BPM/styles
* Songs without records
* Songs never programmed
* Collection valuation
* Discogs information
* Potential duplicates

## Data Integrity

Treat multi-table operations as transactions.

The application must:

* Validate input
* Respect foreign keys
* Prevent unsafe deletions
* Roll back failed operations
* Preserve referential integrity
* Give clear error messages
* Confirm destructive actions

## Project Structure

Use a maintainable structure similar to:

```text
MusicCollectionManager/
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── database/
├── models/
├── repositories/
├── controllers/
├── views/
├── dialogs/
├── widgets/
├── ui/
├── themes/
├── reports/
├── logs/
├── backups/
├── exports/
└── Musi.db
```

Keep database, business logic, and presentation clearly separated.

## Development Strategy

**Do not attempt to build the entire application at once.**

Develop it incrementally.

### Phase 1 — Foundation

First build:

* Project structure
* SQLite connection/database manager
* Schema inspection
* Logging
* Configuration
* Backup utilities
* Main window
* Navigation
* Dashboard
* Status bar
* Theme support
* Error handling

### Phase 2 — CRUD

Add:

* Artists
* Songs
* Records
* Programs
* Styles
* BPM
* Discogs

### Phase 3 — Relationships

Implement the user-friendly relationship editors and automatically maintain the junction tables.

### Phase 4 — Search & Reports

Add global search, advanced filtering, statistics, and exports.

### Phase 5 — Enhancements

Add artwork, automatic backups, undo where practical, drag-and-drop, Discogs integration, shortcuts, and other quality-of-life improvements.

## How I Want You to Work

I have limited Python experience, so **guide me step by step**.

For each phase:

1. Tell me exactly what we are building.
2. Give me the complete code for every new or modified file.
3. Tell me exactly where each file belongs.
4. Give exact installation/run commands.
5. Explain how to test it.
6. Include troubleshooting for likely errors.
7. Do not assume I know Python or Qt.

Before writing code that depends on the database schema, **inspect `Musi.db` and use its actual tables, columns, keys, and relationships**.

Do not invent schema details.

When modifying existing code, provide the complete updated file unless there is a strong reason not to.

Keep the architecture clean and extensible because later phases will depend on the foundation.

### Immediate Task

Start with **Phase 1 — Foundation**.

First inspect the existing `Musi.db` schema, explain what you found, identify the relevant relationships, and then propose the Phase 1 project structure.

**Do not start generating the full application yet.**

### Future developments

For precise reference, this project's full reference is maintained in the following public github repository:
https://github.com/pgradone/MusicCollectionManager
