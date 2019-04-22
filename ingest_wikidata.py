import json
import csv
import numpy as np
import sqlite3

con = sqlite3.connect("biggraph.db")
cur = con.cursor()
cur.execute("CREATE TABLE wiki_data (id, vector);") # use your column names here



with open("/Downloads/wikidata_translation_v1.tsv") as fd:
	read = list(csv.reader(fd, delimiter="\t",quoting=csv.QUOTE_NONE))

	m = len(read)
	n = 200
	to_db = []
	for i in range(m):
		key = read[i][0]
		vector = np.array(read[i][1:], dtype=np.float32)
		to_db.append((key,vector))

cur.executemany("INSERT INTO wiki_data (id, vector) VALUES (?, ?);", to_db)
print('INSERTED')

con.commit()
con.close()