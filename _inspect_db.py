import sqlite3
conn = sqlite3.connect("Musi.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
tables = [row["name"] for row in cur.fetchall()]
print("Tables:", tables)
for t in tables:
    cur.execute("SELECT COUNT(*) as c FROM [{}]".format(t))
    cnt = cur.fetchone()["c"]
    print("  {}: {} rows".format(t, cnt))
    cur.execute("PRAGMA table_info([{}])".format(t))
    cols = [(r["name"], r["type"]) for r in cur.fetchall()]
    print("    Columns: {}".format(cols))
conn.close()
