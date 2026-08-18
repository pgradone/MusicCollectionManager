# MusicCollectionManager — User Manual

## 1. Introduction

MusicCollectionManager is a desktop application for managing a personal music collection. It uses a structured SQLite database to organize artists, songs, records, programs, schedules, styles, and the relationships between them.

This guide is intended for non-developers.

## 2. What the Application Manages

### Artists
Performers or musical acts in the collection.

### Songs
Tracks with information such as title, BPM, year, and duration/time.

### Records
Physical or collectible releases, including information such as record house, support/media type, artist, valuation, and sale-related fields.

### Styles
Musical classifications associated with songs.

### Programs and Schedules
Information used to model programming and scheduling.

### Relationships
Associations connect the main objects. Examples include:
- artists singing songs
- songs belonging to styles
- songs contained on records
- records associated with artists
- programs associated with schedules

## 3. How to Think About the Collection

The collection is a connected model rather than a set of unrelated lists:

**Artist → Song → Style**

and

**Artist → Record → Song**

A song may have several styles, an artist may perform several songs, and a record may contain several songs.

## 4. Using the Application Safely

When using the graphical interface:

1. Select the relevant area.
2. Find the record you want.
3. Make the change.
4. Save/confirm it when requested.
5. Refresh or reopen the information when necessary to verify it.

Avoid editing the SQLite database directly unless you are deliberately performing database maintenance.

## 5. Relationships

A relationship is different from changing an object's own data.

For example, changing a song title modifies the song. Associating that song with an artist modifies the artist/song relationship.

The same principle applies to songs/styles and records/songs.

## 6. Data Integrity

Primary keys identify records uniquely. Foreign keys connect records that belong together.

The database can therefore reject a relationship that refers to a nonexistent record instead of silently creating broken data.

## 7. Backups

Before substantial maintenance or bulk changes:

1. Close the application.
2. Copy the database file.
3. Keep the backup separately.
4. Perform the changes.
5. Verify the application afterward.

## 8. Troubleshooting

### Expected data is missing
Check that the intended database is being used and refresh/restart the application.

### A relationship cannot be created
Check that the referenced records already exist. Foreign-key rules may reject invalid references.

### A change appears unsaved
Check whether the operation was committed and whether the interface needs refreshing.

### Unexpected information appears
Avoid manually editing SQLite first. Investigate the application behavior and database structure.

## 9. Glossary

**Artist** — A performer or musical act.

**Song** — A musical track represented in the collection.

**Record** — A physical or collectible release containing one or more songs.

**Style** — A musical classification associated with songs.

**Primary key** — A value, or combination of values, uniquely identifying a database record.

**Foreign key** — A value connecting one database record to another.

**Junction/association table** — A table representing a relationship between entities, such as Song–Style or Artist–Song.

**SQLite** — The database technology used to store the collection.

## 10. Summary

MusicCollectionManager is a connected model of a music collection. Artists, songs, records, styles, programs, and schedules are structured data, while their associations are represented explicitly so the collection can remain consistent as it grows.
