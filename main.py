import networkx as nx 
import matplotlib as mpl 
import matplotlib.pyplot as plt

INF = 1e9

def bit(mask, pos):
	return (mask >> pos) & 1

def TSP_Solution(G):
	dp = [];
	for u in range(n):
		dp.append([])
		for mask in range(1 << n):
			dp[u].append([INF, [u]])

	s = 0
	dp[s][1 << s][0] = 0

	pos = nx.spring_layout(G)
	nx.draw_networkx(G, pos, with_labels=True, font_weight='bold')
	labels = nx.get_edge_attributes(G, 'weight')
	nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

	for mask in range(0, 1 << n):
		for v in range(n):
			for u in range(n):
				if bit(mask, u):
					continue
				newmask = mask | (1 << u)
				if (G.has_edge(v,u) or G.has_edge(u,v)):
					if (dp[v][mask][0] + int(G.get_edge_data(v, u, default=0)['weight']) < dp[u][newmask][0]):
						dp[u][newmask][0] = dp[v][mask][0] + int(G.get_edge_data(v, u, default=0)['weight'])
						dp[u][newmask][1] = dp[v][mask][1] + [u]

	mask = (1 << n) - 1
	path_weight = INF
	last = -1
	for u in range(n):
		if (G.has_edge(s,u) or G.has_edge(u,s)):
			dp[u][mask][0] = dp[u][mask][0] + int(G.get_edge_data(u, s, default=0)['weight'])
			dp[u][mask][1] = dp[u][mask][1] + [s]
		else:
			dp[u][mask][0] = INF

	for u in range(n):
		if dp[u][mask][0] < path_weight:
			path_weight = dp[u][mask][0]
			last = u

	if (path_weight == INF):
		print('В заданном графе не существует гамильтонова цикла')
	else:
		print('Самый дешёвый гамильтонов путь: ' + str(path_weight))
		print('Путь коммивояжера: ')
		print(dp[last][(1 << n) - 1][1])
		colored_edges = []
		for i in range(n):
			u, v = dp[last][(1 << n) - 1][1][i], dp[last][(1 << n) - 1][1][i+1]
			colored_edges.append((u, v))

		nx.draw_networkx_edges(G, pos, edgelist=colored_edges, edge_color='r')
	
	plt.show()


G = nx.Graph()
type = -1
while type != 0:
	print('Выберите действие из предложенных:')
	print('0 - Выход | 1 - Ввести новый граф | 2 - Запустить решение задачи')
	type = int(input())
	if type == 1:
		G = nx.Graph()
		print('Введите число вершин в графе (до 22): ')
		n = int(input())

		for i in range(n):
			G.add_node(i)

		print('Введите количество рёбер: ')
		m = int(input())

		print('Введите сами рёбра (обратите внимание, рёбра вводятся в 0-индексации): ')
		for i in range(m):
			u, v, w = map(int, input().split())
			G.add_edge(u, v)
			G[u][v]["weight"] = w 
		
		print('Граф успешно задан')
	elif type == 2:
		if not G:
			print('Сначала введите граф!')
		else:
			TSP_Solution(G)
	elif type == 0:
		break
	else:
		print('Заданной команды не существует')
