import sqlite3
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute("PRAGMA table_info(api_gasto)")
cols = [r[1] for r in c.fetchall()]
print('Columns:', cols)
print('Has data_competencia:', 'data_competencia' in cols)
conn.close()
