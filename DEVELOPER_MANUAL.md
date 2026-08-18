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

The `services/` layer contains application-facing behavior, including modules such as:

```text
artist_service.py
program_service.py
record_service.py
search_service.py
song_service.py
```

Services should express application behavior using the generic infrastructure below them rather than duplicating SQL or connection management.

## 12. UI Layer

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

## 13. Why the Layers Matter

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

## 14. Transaction Semantics

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

## 15. Foreign Keys and Integrity

SQLite foreign-key enforcement is part of the tested architecture.

Relationships such as `Belong`, `Contain`, and `Sing` must not create references to nonexistent parent records.

Database integrity checks are also part of the test coverage.

## 16. Testing

The project uses:

```powershell
pytest -q
```

as the normal verification command.

The milestone tests cover repository integration, CRUD, validation, composite keys, transaction semantics, foreign keys, and generic relationship operations.

## 17. Development Workflow

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

## 18. Rules for Future Development

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

## 19. Direction for `main.py`

The architectural goal is for `main.py` to coordinate application startup and UI/services rather than becoming another database layer:

```text
main.py
   │
   ▼
Application
   │
   ▼
Services
   │
   ├── Repository
   └── Relationship Operations
           │
           ▼
     DatabaseContext
        │       │
        ▼       ▼
 DatabaseManager SchemaManager
        │
        ▼
      SQLite
```

The repository and relationship milestones exist specifically to make this transition safe.

## 20. Adding a New Entity

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

## 21. Database Architecture at a Glance

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

## 22. Final Architectural Principle

> **Application behavior belongs above the database infrastructure; database mechanics belong below it.**

`DatabaseManager` owns SQLite access.

`SchemaManager` understands database structure.

`Repository` provides generic table operations.

`Relationship Operations` provide generic relationship behavior.

`Services` express application-level operations.

The UI presents those operations to the user.

Keeping these responsibilities separate is what makes the architecture maintainable and allows the application to evolve without returning to table-specific SQL throughout the codebase.
