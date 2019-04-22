import json
import numpy as np
import h5py
import faiss
import sqlite3
import csv




def query(database, key, k, index, dictionary_path):
	"""
	database: string - db to extract data from
	key : string - id of the item you want to query
	k: int - number of neighbors that you want, first neighbor will be the item itself
	index: faiss.IndexFlatL2(index_dim)
	embeddings_[path]: the trained model/vector space path
	dictionary: path of json file that maps vector to id

	EXAMPLE:
	database = 'biggraph.db'
	key = '/m/01c4pv'
	k = 5
	index = faiss.IndexFlatL2(400)
	embeddings_path = "model/fb15k/embeddings_all_0.v50.h5"
	dictionary_path = "data/FB15k/dictionary.json"
	"""

	result = []

	db = database
	con = sqlite3.connect(db)
	cur = con.cursor()
	cur.execute("SELECT * FROM id_to_vector WHERE id = ?", (key,))

	inst = cur.fetchone()
	print(inst)

	vector = np.array([np.frombuffer(inst[1],dtype=np.float32)])
	print(vector.shape)


	_, neighbors = index.search(vector.astype('float32'), k)

		
	with open(dictionary_path, "rt") as f:
		dictionary = json.load(f)

	for i in range(k):
		temp = dictionary["entities"]["all"][neighbors[0, i]]
		result.append(temp)

	return result

def id_to_index(entid):
	pass

database = 'biggraph.db'
key = '/m/01c4pv'
k = 5
index = faiss.IndexFlatL2(200)
embeddings_path = "fb15kentities_vector.npy"


embedding = np.load(embeddings_path)
index.add(embedding)


dictionary_path = "data/FB15k/dictionary.json"
print(query(database,key,k,index,dictionary_path))



# index = faiss.IndexFlatL2(400)

# with h5py.File("model/fb15k/embeddings_all_0.v50.h5", "r") as hf:
#     index.add(hf["embeddings"][...])
# con = sqlite3.connect('biggraph.db')
# cur = con.cursor()
# cur.execute("SELECT * FROM id_to_vector WHERE id = ?", ('/m/01c4pv',))
# inst = cur.fetchone()
# vector = np.array([np.frombuffer(inst[1],dtype=np.float32)])
# _, neighbors = index.search(vector.astype('float32'), 14000)


# with open("data/FB15k/dictionary.json", "rt") as f:
#     dictionary = json.load(f)


# elt1 = dictionary["entities"]["all"][neighbors[0, 0]]

# elt2 = dictionary["entities"]["all"][neighbors[0, 1]]

# elt3 = dictionary["entities"]["all"][neighbors[0, 2]]

# elt4 = dictionary["entities"]["all"][neighbors[0, 13999]]

# print(index.ntotal)

# elt1 = dictionary["entities"]["all"][neighbors[0, 0]]
# print(elt4)

