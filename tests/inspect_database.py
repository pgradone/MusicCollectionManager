import sqlite3

DATABASE = "Musi.db"

db = sqlite3.connect(DATABASE)

tables = db.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
      AND name NOT LIKE 'sqlite_%'
    ORDER BY name
    """
).fetchall()

print("Tables in Musi.db:")
print()

for row in tables:
    print(f"  {row[0]}")

db.close()