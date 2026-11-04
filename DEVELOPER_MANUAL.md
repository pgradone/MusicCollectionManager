# MusicCollectionManager — Developer Manual

## 1. Purpose

MusicCollectionManager is a Python application built around a SQLite database. Its architecture separates database access, schema metadata, generic repository operations, relationship operations, service-layer behavior, and the user interface.

The central objective is to keep application code independent from table-specific SQL wherever practical.

The developer manual places particular emphasis on the database architecture, the responsibilities of DatabaseManager, SchemaManager, DatabaseContext, Repository, relationship_operations, the service layer, and the intended UI → services → database flow

## 2. Architectural Overview

```text
main.py / Application
        │
        ▼
       UI
        │
        ▼
    Services
        │
        ▼
Repository / Relationship Operations
        │
        ▼
  DatabaseContext
     /       \
    ▼         ▼
DatabaseManager  SchemaManager
    │
    ▼
  SQLite
```

The SQLite connection is owned by `DatabaseManager`. Higher layers should not independently create SQLite connections.

## 3. Database Layer — `core/database.py`

`DatabaseManager` is the low-level database gateway. It handles:

- opening and closing SQLite connections
- SQL execution
- parameter handling
- transactions
- commits and rollbacks
- query logging/timing
- database information
- integrity checks
- low-level schema access

It is the intended sole owner of the SQLite connection.

## 4. Schema Layer — `core/schema.py`

`SchemaManager` sits above `DatabaseManager` and discovers/caches metadata such as:

- tables
- columns
- primary keys
- foreign keys
- indexes
- table relationships

This lets the repository layer understand a table without hard-coding its structure everywhere.

## 5. Database Context — `core/context.py`

`DatabaseContext` coordinates `DatabaseManager` and `SchemaManager`.

It exposes:

```python
context.database
context.schema
```

Its lifecycle is:

1. connect the database
2. optionally load schema metadata
3. expose initialized components
4. clear schema state and disconnect when closed

It does not replace either manager.

## 6. Generic Repository — `core/repository.py`

`Repository` provides metadata-aware CRUD for a table:

- `all`
- `find`
- `get`
- `require`
- `count`
- `insert`
- `update`
- `delete`
- `exists`

It is instantiated with a `DatabaseContext` and table name and obtains structure through `SchemaManager`.

The repository handles normal and composite primary keys.

## 7. Composite Keys

Examples include:

```text
Belong   : SongID + StyleID
Contain  : RecordID + SongID
Sing     : ArtistID + SongID
```

Generic code must not assume every record is identified by one integer.

## 8. Relationship Operations — `core/relationship_operations.py`

The relationship layer provides generic operations such as:

```text
list_related
link
unlink
reorder
```

The current junction-table relationships include:

```text
Sing
Contain
Belong
```

The objective is to describe a relationship once and operate generically rather than implementing table-specific relationship code.

## 9. Direct and Reverse-Direct Relationships

`direct` and `reverse_direct` relationships have different key semantics from junction tables.

The project uses these shapes for relationships such as:

```text
Records ↔ Artist
Programs ↔ Schedule
```

They should therefore not be forced into the junction-table implementation.

## 10. Relationship Descriptions

Relationship metadata contains the information required for generic operations. A significant addition is `source_table`, which allows an operation to validate the owning/source row without requiring the caller to supply the table name repeatedly.

Conceptually:

```text
Relationship
    ├── source table
    ├── target table
    ├── relationship type
    └── key/column mapping
```

This makes relationship behavior declarative rather than table-specific.

## 11. Services Layer

The `services/` layer contains application-facing behavior. It builds on the generic infrastructure below it (repositories and relationship operations) rather than duplicating SQL or connection management.

| Module | Role |
| --- | --- |
| `artist_service.py`, `song_service.py`, `record_service.py`, `program_service.py` | Business operations for one entity, such as creating a record, linking a Discogs release, or moving schedule lines. |
| `report_service.py` | Dashboard statistics and the integrity reports. |
| `search_service.py` | Global search across the main tables. |
| `discogs_service.py` | Reaching records and songs through a Discogs release number, and suggesting matches. |
| `discogs_import.py` | Importing a newer Discogs collection export. |

The entity services validate input and raise service-specific errors (`ServiceError` subclasses). Report, search and Discogs services are different in kind: they read whole tables rather than perform single-row operations, so they use `repository_for()` directly. None of them contains SQL.

`ProgramService` owns the schedule, because `Schedule` does not fit the generic relationship model: its primary key includes `Position`, it carries copied BPM and year values, and `SongID` is only a soft foreign key. `move_selected()` moves any set of lines (adjacent or not) by one place, computed from one snapshot of the schedule and written in a single transaction.

Utilities that need no `DatabaseContext` live in `core/`: `export.py` (file writers), `backup.py`, `logger.py` and `settings.py`. `settings.py` is built and tested but not used by the application yet.

## 12. Reporting, Search and Discogs

These services are read-only, apart from `DiscogsService.confirm_match()` which delegates to `RecordService.link_discogs()`.

### `ReportService`
`dashboard_stats()` returns a frozen `DashboardStats` dataclass: counts per table, average BPM, collection value (valuation of records without a sold date) and sold value, missing-metadata counts, and recently created programs. "Recently added" exists only for `Programs`, because `Programs.DateCreate` is the only creation timestamp in the schema.

The integrity reports are `songs_without_artists`, `songs_without_records`, `artists_without_songs`, `records_without_songs`, `duplicate_artists` and `songs_sung_by_many_artists`. They were chosen from the saved queries of the legacy `Musi.accdb`. `duplicate_artists` groups by case-insensitive, trimmed `(Surname, Name)`; it never groups rows with no surname, and it deliberately does not group by surname alone, since unrelated people share common surnames.

### `SearchService`
`search(query)` is a case-insensitive substring search over Artists (name, surname), Songs (title), Records (title), Programs (name, description) and Styles (label). A blank query returns nothing. Each hit is a `SearchResult(table, primary_key_column, primary_key_value, row)`, which is what lets the UI navigate to it.

### `DiscogsService`
- `parse_release_id(text)` accepts `98675`, `r98675`, `[r98675]` or a discogs.com release URL and returns the digits as text, because `Discogs.release_id` is a text key.
- `lookup(text)` returns a `DiscogsLookup(release, record, artist, tracks)`. Tracks come from `Contain`, ordered by their free-text `Position`.
- `list_releases(linked=...)` adds the linked record's id and title (`RecordID`, `RecordTitle`) to each release.
- `suggest_records(release_id)` scores unlinked records against a release using `difflib`. Artist and title are normalised (case, punctuation, a leading "the", and Discogs' `(5)` disambiguation suffix) and compared both combined and as titles alone, because record titles in this collection often start with the artist. Records that already hold a release are skipped. Checked against the existing 81 links: the right record was first in 76 and in the top three in 79. It takes about 0.2 s per release, and is only run for the release being looked at.
- `confirm_match()` links through `RecordService.link_discogs()`. The database enforces that a release belongs to at most one record (a unique column), and that is not duplicated in code.

The service works only on data already in the database; it never calls discogs.com.

## 13. Export and Import

### Export: `core/export.py`
`export_to_csv`, `export_to_excel` and `export_to_pdf` each take `(rows, columns, path)`, where rows are dicts and columns give the order. They are stateless and know nothing about the database. Excel output has a bold header, content-sized columns and a sheet title cleaned for Excel's rules (no `\ / ? * [ ] :`, at most 31 characters). The PDF is landscape with a repeating header row, and columns share the page width equally so even the 12-column Records table fits.

### Export in the UI
`MainWindow._export_table_widget()` is shared by Browse, Reports, Search and Discogs. It reads **from the `QTableWidget`**, not from the Python data that built it: only visible rows, in their current visual order, under the current headers. This is deliberate. `filter_rows()` hides rows with `setRowHidden()` without touching `table_rows`, and a header click reorders the widget without touching it either, so exporting `table_rows` would silently ignore both. The format follows the extension typed in the save dialog.

### Import: `services/discogs_import.py`
`DiscogsImporter` brings a Discogs collection export (CSV) into the `Discogs` table.

- `read_export(path)` parses the file (BOM-safe), turns blank cells into `NULL`, ignores unknown columns, skips rows with a missing, non-numeric or duplicate `release_id` and reports them as problems. A file without a `release_id` column raises `DiscogsImportError`.
- `preview(path)` returns an `ImportPreview` (new rows, changes with old and new values, unchanged count, count of database releases absent from the file, problems) without changing anything. Only the columns present in the file are compared.
- `apply(preview)` writes everything inside one `database.transaction()`, so a failure part-way rolls back completely. New rows get `ID` = highest `ID` + 1 and `https://www.discogs.com/release/<id>` as their link.

Rules that must be kept: **nothing is deleted** (a release missing from the file may be linked to a record), `release_id` is never changed, and `Records` is never touched, so existing `Records.Discogs_release` links stay valid.

## 14. Artwork

Records can have a cover image. It is deliberately **not** stored in the database: there is no artwork column or table, so the feature changed nothing in `Musi.db` and needed no migration.

### `services/artwork_service.py`
`ArtworkService(folder=None)` works only with files (like `core/export.py` and `core/backup.py`, it has no `DatabaseContext`). The folder defaults to `config.ARTWORK_FOLDER`, read when the object is created so a test can redirect it.

- A cover is `artwork/<RecordID>.jpg`. `path_for()` says where it would be, `get()` returns the path only if the file exists.
- `set_image(record_id, source)` opens the source with Pillow, turns it upright using its EXIF orientation, flattens transparency onto white, shrinks it to fit within `MAX_SIZE` (1000) pixels without enlarging, and saves a JPEG. It writes `<id>.jpg.tmp` first and then `os.replace`s it, so a failure never destroys the cover already there.
- Anything unreadable raises `ArtworkError` with a message naming the file; a missing file, a non-image and a decompression bomb all take that path.
- `remove(record_id)` returns whether there was a cover.

### The Cover panel in `main.py`
`cover_group` sits beside the record details and is visible only while a `Records` row with an integer ID is selected (`_current_record_id()`). `_update_cover_panel()` runs at the start of `_update_related_tabs()` (which `load_table_data()` always ends with) and at the end of `clear_form()`, so it follows every selection change. It loads the picture from the file's bytes instead of `QPixmap(path)`, so a replaced cover is never served from Qt's cache.

`ArtworkLabel` is a `QLabel` that accepts a dropped image file and emits `imageDropped(path)`; it welcomes only local files, not text or web addresses. Problems with a chosen file are shown in the status line, not in a message box.

### Deleting records
`delete_record()` removes the cover of a deleted **Records** row (`_remove_cover_of_deleted_record`). This matters because SQLite can hand a deleted record's ID to a later record, which would otherwise inherit the old cover. The cleanup lives in the UI, not in `RecordService.delete()`, so service tests never touch the artwork folder. Rows of other tables are never touched, even if their ID equals a record's ID.

### Not covered by backups
`backup_database()` copies only the database. Covers live in `artwork/`, which is not backed up and is in `.gitignore`.

## 15. Startup, Backup and Logging

`main.run_startup_tasks()` runs first in `main()`, before the `QApplication` and `MainWindow` exist:

1. `initialise_logger()` configures the root logger: a rotating file `logs/music_collection.log` plus the console, at `config.LOG_LEVEL`. (`logging.basicConfig` is not used as well, because that would print every console line twice.)
2. If `config.AUTO_BACKUP` is on and `todays_backup()` finds a file named `Musi_<today>_*.db`, nothing more is done. This gives one backup a day, so `MAX_BACKUPS` (30) covers thirty days rather than thirty launches.
3. Otherwise `backup_database()` copies the database to `backups/Musi_<YYYYMMDD>_<HHMMSS>.db`, prunes the oldest beyond `MAX_BACKUPS`, and returns the new path (or `None` when disabled or there is no database yet).

A failed backup (`OSError`) is logged as a warning and never stops the application starting.

**Why a plain file copy is safe:** the database uses the default `delete` journal mode, and the copy is taken before the application opens a connection. If the database were ever switched to WAL mode, replace the copy with SQLite's online backup API (`sqlite3.Connection.backup`).

Only the database is backed up; cover images in `artwork/` are not (see Artwork).

Backups are named by date, and `todays_backup()` reads the date from the name rather than the file's modified time, which a copy or restore can change. `backups/` and `logs/` are in `.gitignore`.

Configuration lives in `config.py`: `AUTO_BACKUP`, `MAX_BACKUPS`, `BACKUP_FOLDER`, `LOG_FOLDER`, `LOG_LEVEL`, `EXPORT_FOLDER`, `DATABASE_FILE`.

## 16. UI Layer

The preferred dependency direction is:

```text
UI
 ↓
Services
 ↓
Repository / Relationship Operations
 ↓
DatabaseContext
 ↓
DatabaseManager + SchemaManager
 ↓
SQLite
```

UI code should not independently open SQLite connections or duplicate repository SQL.

### The tabs
`MainWindow` has five top-level tabs in a `QTabWidget`: Browse, Dashboard, Reports, Search and Discogs. Each tab's widget is kept (`_browse_widget`, `_dashboard_widget`, `_reports_widget`, `_search_widget`, `_discogs_widget`) so code can tell which is showing. Dashboard, Reports and Discogs load their data the first time they are opened, via `_on_main_tab_changed`. The new tabs report problems in a status label rather than a `QMessageBox`, because a modal box waits for a click.

Navigation from any tab to a record goes through `_navigate_to_related_value()`, which switches back to Browse, selects the table in the combo box and selects the row.

### Relationship-driven subforms
The tabs under the record form come from `discover_relationships()`, not from hard-coded lists. Whether a junction table's extra column is a number or free text is read from the declared column type: `Relationship.numeric_extra_columns` lists the numeric ones, and only those get Move Up / Move Down / Renumber controls. `Contain.Position` is text (`A1`, `B2`), so it is edited directly in the cell instead. `Relationship.order_column` marks an ordered child table such as `Schedule`, whose primary key is the foreign key plus one numeric column.

### Reloading and the schedule selection
`load_table_data()` rebuilds the related tabs **more than once per call**, because re-selecting the current row fires the selection signal again. Anything a rebuild must restore therefore has to be idempotent and cleared only after the whole reload has finished. `_pending_schedule_reselect` follows this rule: it is set before the reload, re-applied by every rebuild of the Schedule tab, and cleared afterwards, which is what keeps the moved rows selected.

### Keyboard shortcuts
`_install_shortcuts()` creates the `QShortcut` objects, keeps them in `self._shortcuts` keyed by their key text, and sets tooltips. Handlers do not duplicate behavior: they click the same button the mouse would (`save_button`, `new_button`, each tab's export button, and the Move Up / Move Down buttons of the open related tab). `Delete` is bound to the record list only (`Qt.ShortcutContext.WidgetShortcut` with `table_widget` as parent); a window-wide Delete would fire while erasing text in a box. `delete_record()` itself asks for confirmation, so the button and the key behave identically.

## 17. Why the Layers Matter

| Layer | Responsibility |
|---|---|
| UI | Presentation and user interaction |
| Services | Application/business behavior |
| Relationship operations | Generic relationship behavior |
| Repository | Generic table CRUD and validation |
| DatabaseContext | Lifecycle and coordination |
| SchemaManager | Database metadata |
| DatabaseManager | SQLite access and transactions |
| SQLite | Persistent data |

This separation allows one layer to evolve without rewriting the entire application.

## 18. Transaction Semantics

Transaction control remains with `DatabaseManager`.

Repository operations can request commit behavior, but the repository does not own the SQLite connection.

The distinction is:

```text
Repository:
    what database operation is performed

DatabaseManager:
    how the SQLite transaction is controlled
```

The transaction tests cover insert/update/delete with both commit and rollback behavior.

## 19. Foreign Keys and Integrity

SQLite foreign-key enforcement is part of the tested architecture.

Relationships such as `Belong`, `Contain`, and `Sing` must not create references to nonexistent parent records.

Database integrity checks are also part of the test coverage.

## 20. Testing

The normal verification command is:

```powershell
python -m pytest -q
```

Use `python -m pytest` rather than `pytest` so it works even when the Scripts folder is not on `PATH`. On a new machine, `pip install -r requirements-dev.txt` installs the application's packages plus the test tools. `pypdf`, which the export tests use to read PDFs back, is part of `requirements.txt`.

Tests cover the repository, CRUD, validation, composite keys, transactions, foreign keys, relationship operations, every service, export, import, startup and the main window.

### Conventions
- **Test database.** Tests that write use `tests/Musi_crud_test.db`, never `Musi.db`. In window tests use the `crud_window` fixture, which constructs `MainWindow` and then points it at that database.
- **`crud_window` caveat.** `MainWindow` loads its first table from the production database before the fixture redirects it. Call `load_table_data()` yourself after creating rows, and remember that `_navigate_to_related_value()` only reloads if the table combo's selection really changes.
- **Never assume production data.** `Musi.db` changes as it is used (a report that had rows can become empty). Create synthetic rows with an unmistakable prefix such as `Zzz`, assert on those, and delete them in `finally`. Assert before/after differences, not absolute counts.
- **Artwork folder.** `tests/test_main_window.py` has an autouse fixture, `isolated_artwork_folder`, that points `config.ARTWORK_FOLDER` at a throwaway directory for every test in the file. Keep it: record IDs in the test database overlap real ones, so without it deleting a test record could delete the cover of a real record with the same ID.
- **Files and folders.** Use `tmp_path`, and point `config.DATABASE_FILE`, `BACKUP_FOLDER` and `LOG_FOLDER` at it with `monkeypatch`.
- **Dialogs.** `QMessageBox.question/information/warning` and `QFileDialog` block waiting for a click, even with `QT_QPA_PLATFORM=offscreen`. Patch them (`patch("main.QMessageBox.question", ...)`) in every test that could reach one.
- **Logging.** `initialise_logger()` changes the root logger, a process-wide singleton. Restore its handlers and level afterwards.
- **Key presses.** To test a real key combination, show and activate the window, send it with `QTest.keyClick`, and `hide()` the window afterwards. Do not `close()` it: closing disconnects the shared database.
- **Qt items.** Read what you need from a `QTableWidgetItem` before triggering anything that rebuilds the table; the item is deleted by the rebuild.
- Running the tests changes `Musi.db` and `Musi_crud_test.db` slightly. Restore them with `git checkout -- Musi.db tests/Musi_crud_test.db` before committing, and add files to git by name.

## 21. Development Workflow

A safe development cycle is:

```text
1. Modify one architectural layer
2. Add/update focused tests
3. Run pytest -q
4. Inspect the result
5. Commit
6. Push
7. Continue
```

Keeping commits aligned with completed, passing milestones makes regressions easier to identify.

## 22. Rules for Future Development

### Do not bypass `DatabaseManager`
Do not introduce independent `sqlite3.connect(...)` calls in application code.

### Do not duplicate repository CRUD
Use `Repository` for generic table operations instead of adding repeated SELECT/INSERT/UPDATE/DELETE implementations.

### Do not duplicate relationship logic
Use the generic relationship-operation layer for supported relationship types.

### Keep schema knowledge centralized
Use schema and relationship metadata rather than scattering table structure throughout the UI.

### Keep UI database-agnostic
The UI should ask services to perform application operations rather than constructing SQL.

## 23. State of `main.py`

The goal set out earlier has been reached: `main.py` contains no SQL. Every table load, save and delete goes through `Repository`; related records go through `core.relationships` and `core.relationship_operations`; behavior with rules (schedules, Discogs, reports, search, import) goes through a service. What `main.py` still asks of `DatabaseManager` is schema metadata only (`columns()`, `primary_key()`).

```text
main.py (MainWindow)
   │
   ▼
Services ── Repository / Relationship Operations
                 │
                 ▼
          DatabaseContext
           │            │
           ▼            ▼
   DatabaseManager  SchemaManager
           │
           ▼
         SQLite
```

Known loose ends:

- `main.py` is large (about 2,600 lines). The five tabs are natural candidates for separate modules.
- `core/settings.py` exists and is tested but nothing uses it yet.
- Not every Qt dialog path is covered by tests.

## 24. Adding a New Entity

Preferred sequence:

1. Ensure the SQLite schema is correct.
2. Ensure primary/foreign keys are correct.
3. Ensure `SchemaManager` discovers the table.
4. Use `Repository` for generic CRUD.
5. Add a service for application-specific behavior.
6. Add relationship metadata if needed.
7. Add focused pytest coverage.
8. Run `pytest -q`.
9. Wire the UI only after the infrastructure tests pass.

## 25. Database Architecture at a Glance

```text
                         APPLICATION
                              │
                         ┌────▼────┐
                         │   UI    │
                         └────┬────┘
                              │
                         ┌────▼────┐
                         │Services │
                         └────┬────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
        ┌───────▼────────┐        ┌────────▼─────────┐
        │   Repository   │        │   Relationship   │
        │ Generic CRUD   │        │   Operations     │
        └───────┬────────┘        └────────┬─────────┘
                │                           │
                └─────────────┬─────────────┘
                              │
                       ┌──────▼──────┐
                       │ Database    │
                       │   Context   │
                       └──────┬──────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
             ┌──────▼──────┐     ┌──────▼──────┐
             │  Database   │     │   Schema    │
             │   Manager   │     │   Manager   │
             └──────┬──────┘     └─────────────┘
                    │
                    ▼
                 SQLite
```

## 26. Final Architectural Principle

> **Application behavior belongs above the database infrastructure; database mechanics belong below it.**

`DatabaseManager` owns SQLite access.

`SchemaManager` understands database structure.

`Repository` provides generic table operations.

`Relationship Operations` provide generic relationship behavior.

`Services` express application-level operations.

The UI presents those operations to the user.

Keeping these responsibilities separate is what makes the architecture maintainable and allows the application to evolve without returning to table-specific SQL throughout the codebase.
