import networkx as nx
import os
import re
import math
import numpy as np
import pandas as pd
from numpy import linalg as LA
import csv

from sklearn.cluster import spectral_clustering



from os import listdir


def load_egonet_files(path):
	onlyfiles = [fyle for fyle in listdir(path) if fyle.endswith('.egonet')]
	return onlyfiles

def edge_from_line(line , n):
	lst = line.split(':')
	friend_one = int(lst[0]) 
	friend_list = lst[1]
	friend_list = lst[1].split(' ')
	edge = []
	edge +=[ (n , friend_one)]
	friends = []
	nodes = [n,friend_one]
	for x in friend_list:
		if x != '' and x != '\n':
			friends += [int(x)]
	
	for x in friends:
		edge += [(n , x)]
		edge += [(friend_one, x)]
		nodes += [x]
		
	return edge,nodes


def build_graph(n):
	edges = []
	nodes = []
	path = 'D:\CODES\kaggle\circles\egonets\egonets'
	egonets = load_egonet_files(path)
	for egonet in egonets[n:n+1]:
		ego = int(re.match(r'([0-9]+).egonet', egonet).group(1))
		# print(ego)
		m = open(os.path.join(path,egonet) , "r")
		
		cnt = 0 ;
		for line in m.readlines():
			cnt += 1
			r = edge_from_line(line, n) 
			edges += r[0]
			nodes += r[1]
	edges = list(set(tuple(sorted(edge)) for edge in edges))
	nodes = list(set(nodes))
	G = nx.Graph() 
	G.add_nodes_from(nodes)
	G.add_edges_from(edges)

	return G , nodes, ego

def connectedness(A):
	P = np.exp(A)
	return P 
	

def compute_density(circle , nodes, A):
	for x in nodes:
		if(x not in circle):
			continue
		for y in circle:
			if x == y:
				continue
			if(y not in circle):
				continue
			


def compute(n):
	G , nodes , ego = build_graph(n)
	A = nx.to_numpy_matrix(G)
	C = connectedness(A)
	row , col = A.shape
	if row >= 350:
		clus = 10
	else:
		clus = 6
	L = spectral_clustering(C , n_clusters = clus)
	circles = []
	for x in range(0,clus):
		circles += [[]]
	
	tmp = 0
	for node in nodes:
		circles[L[tmp]] += [node]
		tmp += 1

	for circle in circles:
		den = compute_density(circle , nodes , A)

	# print(circles) 
	return ego , circles 
	
	

arr = [25708,2473,18844,19268,25283,21869,17748,5744,3656,17002,26827,10793,17497,23978,850,1813,15515,20050,22364,0,7983,11818,12178,26019,3581,14103,19608,14129,1310,18612,1099,22223,2630,20518,12535,13471,6934,3077,9199,3703,8338,3236,2976,21098,13687,15227,5087,8890,24812,23063]

def outformat(ego , circles):

	if ego not in arr:
		return "NO"
	out = ""
	out += str(ego)+","
	fl = 0 
	egofl = 0
	for circle in circles:
		if fl == 1:
			out += ';'
		fl = 1
		sfl = 0 
		for x in circle:
			if ego == x:
				egofl = 1
			if sfl == 1:
				out += ' '
			sfl = 1
			out += str(x)
		if egofl == 0:
			out +=" " +str(ego)

	# print(out)
	return out

def gen_graph():
	egos = []
	circless = []
	
	outfile = open("arksubmission.csv", "w")
	outfile.write('UserId,Predicted\n')
	for i in range(0,110):
		ego , circles = to_adjacency_matrix(i)
		out = outformat(ego , circles)

		if out == "NO":
			continue
		# print(out)
		outfile.write(out + '\n')
		# spamwriter.writerow([out])


	
	# df = pd.DataFrame(A, index=nodes, columns=nodes)
 #    df.to_csv('graph-{}.csv'.format(n),index=True)



if __name__ == '__main__':
	gen_graph()