import json
import csv
import numpy as np
import sqlite3

# def create_ingest(tablename, embeddings_tsv):
# 	con = sqlite3.connect('biggraph')
# 	cur = con.cursor()
# 	cur.execute("CREATE TABLE tablename (id,vector);")
# 	with open(embeddings_tsv) as fd:
# 		read = list(csv.reader(fd, delimiter="\t",quoting=csv.QUOTE_NONE))

# 	m = len(read)
# 	n = len(read[0]) - 1
# 	to_db = []
# 	for i in range(m):
# 		key = read[i][0]
# 		vector = np.array(read[i][1:], dtype = np.float32)
# 		to_db.append((key,vector))

# 	cur.executemany("INSERT INTO ? (id, vector) VALUES (?, ?);", (tablename, to_db))
# 	print('INSERTED')

# 	con.commit()
# 	con.close()


con = sqlite3.connect("biggraph.db")
cur = con.cursor()
cur.execute("CREATE TABLE id_to_vector (id, vector);") # use your column names here


fb15kall_vectors = np.load('fb15k_all_vectors.npy')
fb15kall_ids = np.load('fb15k_all_id.npy')

#expected to be 200
m = len(fb15kall_vectors)

to_db = []
for i in range(m):
	key = fb15kall_ids[i]

	vector = fb15kall_vectors[i]
	print(key)
	print(vector)
	to_db.append((key,vector))


cur.executemany("INSERT INTO id_to_vector (id, vector) VALUES (?, ?);", to_db)
print('INSERTED')

con.commit()
con.close()





