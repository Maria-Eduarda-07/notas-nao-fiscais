import sqlite3, os
p = os.path.abspath('notas.db')
print('DB path:', p)
conn = sqlite3.connect(p)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
rows = cur.fetchall()
print('Tables:', rows)
for (name,) in rows:
    cur.execute(f"PRAGMA table_info({name})")
    cols = cur.fetchall()
    print('Table', name, 'columns:')
    for c in cols:
        print(' ', c)
    print()
# ensure is_admin on user
if any(r[0]=='user' for r in rows):
    cur.execute("PRAGMA table_info(user)")
    cols = [r[1] for r in cur.fetchall()]
    print('user cols:', cols)
    if 'is_admin' not in cols:
        print('Adding is_admin column')
        cur.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0")
        conn.commit()
        cur.execute("PRAGMA table_info(user)")
        print('user cols after:', [r[1] for r in cur.fetchall()])
conn.close()
