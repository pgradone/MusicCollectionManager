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

## 7. The Main Window

The window has five tabs along the top. **Ctrl+1** to **Ctrl+5** jump between them, and hovering over a tab shows its key.

| Tab | What it is for |
| --- | --- |
| **Browse** | Look at, add, change and delete the records of each table, and manage how they link together. |
| **Dashboard** | A summary of the whole collection. |
| **Reports** | Lists that point out gaps and oddities in the data. |
| **Search** | Find a name or title anywhere in the collection. |
| **Discogs** | Reach your records and songs through their Discogs release number. |

Messages about what the application just did, such as "Record saved.", appear above the table in Browse. Reports, Search and Discogs show theirs in a line just above their list.

## 8. Browsing and Editing

This is the **Browse** tab.

### Choosing and finding records
Choose a table (Artists, Songs, Records, Programs or Styles) in the drop-down list. Its rows appear in the list; click a column heading to sort by that column. The **Search rows** box above the list hides the rows that do not contain what you type. It only filters the table you are looking at; to look everywhere, use the Search tab. **Refresh** (F5) reloads the data.

### Changing a record
Click a row and its fields appear in the form on the right. Change them and press **Save** (Ctrl+S).

To add a record press **New** (Ctrl+N), fill in the fields and press **Save**. **Clear** only empties the form; nothing stored is changed, but be aware that pressing Save afterwards adds a new record.

### Deleting a record
Select the row and press **Delete**, or press the **Delete key** while the list of rows has the focus. The application first asks you to confirm, naming the record, and the answer you get by pressing Enter is **No**. A deletion cannot be undone; the daily backup (see Backups) is your way back. If other records still depend on the one you are deleting, the database may refuse and the message explains why.

The Delete key does nothing while you are typing in a text box, so it cannot remove a record by accident.

### Opening a linked record
Double-click a value that refers to another record, for example the artist of a record, and that record opens.

### The tabs under the form: related records
For the selected record, the tabs under the form list the records linked to it. A song shows its artists, styles and records; a record shows its songs; an artist shows its songs. In each of these:

- **Add** links an existing record to this one.
- **Remove** removes the link only. The record itself is not deleted.
- Double-click a row to open that record.

On a **record**, the *Songs* tab has a **Position** column. Positions are free text such as `A1`, `B2` or `1A1`, so type straight into the cell. The change is saved when you press Enter or leave the cell.

### The cover of a record
When a record is selected, a **Cover** panel appears beside its details. To give the record a picture, press **Choose image...** and pick a file, or drag a picture file from your file explorer and drop it on the panel. PNG, JPEG, GIF, WebP, BMP and TIFF files all work. The application stores its own copy, reduced to at most 1000 pixels on the longest side, in the `artwork` folder next to the program, so the original file is never changed and you can move or delete it afterwards. Choosing another image replaces the cover.

**Remove image** deletes the cover after asking you to confirm. Deleting a record also deletes its cover. If the file you choose is not a picture the application says so and leaves the cover as it was.

### A program's Schedule
For a program, the **Schedule** tab lists its songs in playing order. The **Position** is a whole number and also has small up/down arrows.

- **Add Song** adds a song at the next free position (you can choose another); its BPM and year are copied into the schedule line.
- **Remove** takes the selected line out of the schedule.
- **Move Up** and **Move Down** (or **Alt+Up** and **Alt+Down**) move the selected lines one place. You can select several lines: Shift+click selects a range, Ctrl+click adds or removes single lines, and lines that are not next to each other each move one place. The lines stay selected, so you can press the button again straight away.

On a **song**, the *Programs scheduling this Song* tab shows where that song is used.

## 9. Dashboard

The **Dashboard** tab summarises the collection. It loads when you open the tab; **Refresh** or **F5** reloads it.

- **Collection size**: how many artists, songs, records, programs and styles there are.
- **Average BPM**, and how many songs it is based on.
- **Current collection value** and **sold value**. The current value adds up the valuation of the records you have not sold; sold records are counted separately.
- **Missing metadata**: songs with no BPM, songs with no year, and records with no artist.
- **Recently created programs**. Double-click one to open it in Browse.

Only programs have a creation date in the database, so there is no "recently added" list for artists, songs or records.

## 10. Reports

The **Reports** tab lists things that probably need attention. Choose a report in the drop-down list:

| Report | What it shows |
| --- | --- |
| Songs without an Artist | Songs not linked to any artist. |
| Songs not on any Record | Songs that are not a track on any record. |
| Artists without a Song | Artists with no song linked. |
| Records without a Song | Records with no tracks. |
| Possible duplicate Artists | Artists with the same name and surname once capital letters and extra spaces are ignored. Different people who merely share a surname are not listed. |
| Songs sung by multiple Artists | Songs with more than one artist, such as collaborations, with the artists named. |

An empty report is good news. Double-click a row to open that record in Browse. **Export** saves the list (see Exporting).

## 11. Search

The **Search** tab looks in the whole collection at once. Type some text and press Enter or the **Search** button (Ctrl+F jumps to the box).

It finds partial matches, ignoring capital letters, in:

- artists: name and surname
- songs: title
- records: title
- programs: name and description
- styles: label

Each result shows which table it came from, a short description and its ID. Double-click a result to open it in Browse. This is different from the **Search rows** box in Browse, which only filters the table you are already looking at.

## 12. Discogs

The **Discogs** tab reaches your records and songs through their Discogs release number. It works on the Discogs collection list stored in the database (your Discogs collection export) and never contacts the Discogs website.

### Finding a release
Type a release number into the box, or paste what you have: `98675`, `[r98675]` or the link to the release page. Press **Look up**. The release is selected in the list below, and underneath you see:

- the release's details,
- the record in your collection linked to it,
- the songs on that record, in position order (`A1`, `B1` and so on). Double-click a song to open it.

Double-click a release in the list to open its record in Browse.

### The list
The list shows your Discogs releases. The drop-down list above it chooses **All releases**, only those **Linked to a record**, or only those **Not linked yet**. Only releases that are linked to a record can lead you to songs, so linking the rest is worth doing.

### Linking a release to a record
Select a release that is not linked yet. The application suggests records that probably match, comparing artist and title, with a percentage. Select the right one and press **Link selected record**. A record can have one release, and a release belongs to one record; the database refuses anything else. Double-click a suggestion to look at the record first.

### Importing a newer Discogs export
When your collection on Discogs has changed, export it again from the Discogs website as a CSV file, then press **Import export...** and choose the file. Before anything changes you are told how many releases would be added, how many updated, and how many are already up to date, and you are asked to confirm.

- Releases already in the list are updated where the file differs.
- Releases that are new are added.
- **Nothing is deleted**, even a release that is no longer in the file, and the links to your records stay as they are.
- The import happens completely or not at all.

A file that is not a Discogs collection export is rejected with a message, and nothing changes.

## 13. Exporting

**Browse**, **Reports**, **Search** and **Discogs** each have an **Export** button (Ctrl+E). It saves exactly what you see: if you have filtered the rows or sorted a column, the file has those rows in that order.

Choose a file name and finish it with the format you want:

- `.csv` for a plain text table that opens in any spreadsheet,
- `.xlsx` for an Excel workbook,
- `.pdf` for a printable table.

The suggested folder is `exports`, next to the application. If there is nothing to show you are told so and nothing is written. The Dashboard has no Export button.

## 14. Backups

The application protects the database for you. The first time you start it each day, it copies the database into the `backups` folder, named `Musi_<date>_<time>.db`, and keeps the newest 30 (about a month of history). Starting it again the same day does not make another copy. What the application does is recorded in `logs/music_collection.log`.

To go back to an earlier state: close the application, keep a copy of the current `Musi.db`, then copy the backup you want over it under the name `Musi.db`.

**Cover images are not part of these backups.** They are ordinary files in the `artwork` folder next to the program; copy that folder yourself when you back up your collection.

A day's backup is the database as it was at the first start of that day, so before substantial maintenance or bulk changes also make your own copy:

1. Close the application.
2. Copy the database file.
3. Keep the backup separately.
4. Perform the changes.
5. Verify the application afterward.

## 15. Troubleshooting

### Expected data is missing
Check that the intended database is being used and refresh/restart the application.

### A relationship cannot be created
Check that the referenced records already exist. Foreign-key rules may reject invalid references.

### A change appears unsaved
Check whether the operation was committed and whether the interface needs refreshing.

### Unexpected information appears
Avoid manually editing SQLite first. Investigate the application behavior and database structure.

### Nothing happens when I press the Delete key
The Delete key only works while the list of rows has the focus. Click a row first. The **Delete** button works at any time.

### A report or a search shows nothing
For a report that is usually good news: there is nothing to fix. For a search, try fewer letters; it finds partial matches.

### The Discogs lookup says no release was found
The lookup only knows the releases in the application's Discogs list. If the release is new, import a newer Discogs export first.

### A release cannot be linked to a record
A release can belong to one record only, and a record can have only one release. Look at the record or release that already holds the link.

## 16. Glossary

**Artist** — A performer or musical act.

**Song** — A musical track represented in the collection.

**Record** — A physical or collectible release containing one or more songs.

**Style** — A musical classification associated with songs.

**Primary key** — A value, or combination of values, uniquely identifying a database record.

**Foreign key** — A value connecting one database record to another.

**Junction/association table** — A table representing a relationship between entities, such as Song–Style or Artist–Song.

**SQLite** — The database technology used to store the collection.

**Program** — A planned sequence of songs; its ordered list of songs is the **Schedule**.

**Position** — On a record, free text saying where a song sits, such as `A1`. In a schedule, the whole number giving the song's place in the running order.

**Discogs release** — An item of your Discogs collection, identified by its release number.

## 17. Keyboard Shortcuts

| Keys | What it does |
| --- | --- |
| Ctrl+1 to Ctrl+5 | Go to Browse, Dashboard, Reports, Search or Discogs |
| Ctrl+F | Jump to the search or filter box of the current tab (Browse, Search, Discogs) |
| F5 | Reload what the current tab shows |
| Ctrl+E | Export the rows shown on the current tab to CSV, Excel or PDF |
| Ctrl+N | Start a new record (Browse) |
| Ctrl+S | Save the record being edited (Browse) |
| Alt+Up / Alt+Down | Move the selected rows of a Program's Schedule up or down |
| Delete | Delete the selected record, after asking you to confirm (only while the list of rows has the focus) |

Hovering over a tab or button shows its shortcut. The Delete key only acts while the list of rows has the focus, never while you are typing in a box, and it always asks for confirmation first.

## 18. Summary

MusicCollectionManager is a connected model of a music collection. Artists, songs, records, styles, programs, and schedules are structured data, while their associations are represented explicitly so the collection can remain consistent as it grows.
