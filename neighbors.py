import json
import numpy as np
import h5py
import faiss
import sqlite3
import csv

#78404883	4151	200


def query(key, k, database, dictionary_path, embeddings_path):
	"""
	database: string - db to extract data from
	key : string - id of the item you want to query
	k: int - number of neighbors that you want, first neighbor will be the item itself
	dictionary: path of json file that maps vector to id

	EXAMPLE:
	database = 'biggraph.db'
	key = '/m/01c4pv'
	k = 5
	dictionary_path = "data/FB15k/dictionary.json"
	embeddings_path = 'fb15kentities_vector.npy'
	"""

	result = []

	index = faiss.IndexFlatL2(200)

	embedding = np.load(embeddings_path)
	index.add(embedding)

	vector = id_to_vector(database, key).astype('float32')


	_, neighbors = index.search(vector, k)

		
	with open(dictionary_path, "rt") as f:
		dictionary = json.load(f)

	for i in range(k):
		temp = dictionary["entities"]["all"][neighbors[0, i]]
		result.append(temp)

	return result

def closest_relations(key1, key2, k, database, dictionary_path, embeddings_path):
	"""
	database: string - db to extract data from
	key : string - id of the item you want to query
	k: int - number of neighbors that you want, first neighbor will be the item itself
	dictionary: path of json file that maps vector to id

	EXAMPLE:
	database = 'biggraph.db'
	key = '/m/01c4pv'
	k = 5
	dictionary_path = "data/FB15k/dictionary.json"
	embeddings_path = 'fb15krelations_vector.npy'
	"""

	result = []

	index = faiss.IndexFlatL2(200)

	embedding = np.load(embeddings_path)
	index.add(embedding)

	vector1 = id_to_vector(database, key1).astype('float32')
	vector2 = id_to_vector(database, key2).astype('float32')
	forward = vector1 - vector2
	backward = vector2 - vector1

	_, neighbors = index.search(forward, k)

		
	with open(dictionary_path, "rt") as f:
		dictionary = json.load(f)

	for i in range(k):
		#print(neighbors) #2690 which is 1345*2
		#print(len(dictionary["relations"])) # 1345
		if neighbors[0,i] < len(dictionary["relations"]):
			temp = dictionary["relations"][neighbors[0, i]]
		else:
			temp = None
		result.append(temp)

	return result

def id_to_vector(database, key):
	'''
	database: name of the database; ex: 'biggraph.db'
	key: entitity id such as '/m/01c4pv'
	'''
	con = sqlite3.connect(database)
	cur = con.cursor()
	cur.execute("SELECT * FROM id_to_vector WHERE id = ?", (key,))

	inst = cur.fetchone()
	vector = np.array([np.frombuffer(inst[1],dtype='<U12')])
	

	return vector


dictionary_path = "data/FB15k/dictionary.json"
entitity_embeddings = "fb15kentities_vector.npy"
relation_embeddings = 'fb15krelations_vector.npy'


database = 'biggraph.db'
key = '/m/01c4pv'
k = 5
#print(query(key,k,database,dictionary_path, entitity_embeddings))

database = 'biggraph.db'
key1 = '/m/01c4pv'
key2 = '/m/0494n'
k = 5
#print(closest_relations(key1,key2,k,database,dictionary_path,relation_embeddings))


