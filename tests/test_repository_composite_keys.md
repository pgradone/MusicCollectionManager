I created the Milestone 2F test script based on the current repository API and actual schema, rather than inventing a separate testing interface.

What the test covers

It tests the three real association tables:

Belong (SongID, StyleID)
Contain (RecordID, SongID)
Sing (ArtistID, SongID)

Specifically:

Verifies the expected composite primary keys.
Verifies SQLite foreign-key enforcement is enabled.
Finds unused combinations of real parent IDs, so the test doesn't collide with existing relationships.
Belong: INSERT → GET → DELETE.
Sing: INSERT → GET → DELETE.
Contain: INSERT → GET → UPDATE → DELETE.
Invalid composite-key lengths → PrimaryKeyError.
Invalid None composite key → PrimaryKeyError.
Invalid Belong.SongID → QueryError.
Invalid Belong.StyleID → QueryError.
Invalid Sing.ArtistID → QueryError.
Invalid Contain.RecordID → QueryError.
PRAGMA integrity_check.
PRAGMA foreign_key_check.
Final verification that all temporary rows have been removed.
One deliberate schema-specific decision

Belong and Sing contain only their composite primary-key columns, so there is no legitimate non-PK field to update.

Contain, however, has:

RecordID
SongID
Position

so it provides the appropriate real-world test of UPDATE against a composite-key record.

I also deliberately did not test Contain.SongID as an enforced foreign key, because your actual schema does not declare that FK. That preserves the existing database design rather than imposing a relationship that isn't there.