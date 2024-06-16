import random
import re

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


def process_text_file(file_path):
    # 读取文本文件
    with open(file_path, 'r') as file:
        text = file.read()

    # 将换行符替换为空格
    text = text.replace('\n', '\x20')

    # 将标点符号替换为空格
    text = re.sub(r'[^\w\s]', '\x20', text)

    # 忽略非字母字符
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # 转换为小写
    text = text.lower()

    # 分割成单词
    words = text.split()

    return words


def showDirectedGraph(words, number, path=None):
    G = nx.DiGraph()
    for a in range(len(words) - 1):
        G.add_edge(words[a], words[a + 1], weight=digraph[number[a]][number[a + 1]])
    pos = nx.circular_layout(G)
    options = {
        "font_size": 8,
        "node_size": 300,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 2,
        "width": 2}
    nx.draw(G, pos, **options, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    if path:
        edge_list = []
        for i in range(len(path) - 1):
            edge_list.append((path[i], path[i + 1]))
        nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='r', node_size=300, width=2)
    plt.savefig('graph.png')
    plt.show()


def queryBridgeWords(str1, str2, list, graph):
    bridge_list = []
    if str1 not in list or str2 not in list:
        return bridge_list

    str1number = list.index(str1)
    str2number = list.index(str2)
    for i in range(len(list)):
        if graph[str1number][i] != 0 and graph[i][str2number] != 0:
            # print("The bridge word from", str1, "to", str2, "is:", list[i])
            bridge_list.append(i)
    return bridge_list


def generateNewText(inputText, list, graph):
    temptext = []
    for i in range(len(inputText) - 1):
        bridge_list = queryBridgeWords(inputText[i], inputText[i + 1], list, graph)
        temptext.append(inputText[i])
        if bridge_list:
            bridge = bridge_list[random.randrange(len(bridge_list))]
            temptext.append(list[bridge])
    temptext.append(inputText[-1])
    return temptext


def calcShortestPath(start, end, list, graph):
    # 创建一个字典来存储每个节点的最短距离和是否已访问
    distances = {node: float('inf') for node in list}
    distances[start] = 0
    visited = {node: False for node in list}

    # 初始化一个待处理的节点列表，按照距离排序
    unvisited = [(0, list.index(start))]

    # 创建一个字典来跟踪每个节点的父节点
    parents = {node: None for node in list}

    while unvisited:
        # 取出距离最小的节点
        current_distance, current_index = unvisited.pop(0)

        # 如果当前节点已经被访问过，或者它不是当前未访问节点中距离最小的，则跳过
        if visited[list[current_index]]:
            continue

        # 标记当前节点为已访问
        visited[list[current_index]] = True

        # 更新当前节点的邻居距离
        for neighbor_index in range(graph.shape[1]):  # 遍历所有可能的邻居索引
            if neighbor_index != current_index and graph[current_index][neighbor_index] != 0:  # 如果没有边
                neighbor = list[neighbor_index]  # 根据索引找到邻居节点的标识符
                old_distance = distances[neighbor]
                new_distance = current_distance + graph[current_index][neighbor_index]

                # 如果找到了更短的路径，则更新距离和父节点
                if new_distance < old_distance:
                    distances[neighbor] = new_distance
                    parents[neighbor] = list[current_index]

                    # 将新的邻居节点添加到未访问列表中，并保持其按距离排序
                    for i, (d, n) in enumerate(unvisited):
                        if new_distance < d:
                            unvisited.insert(i, (new_distance, neighbor_index))
                            break
                    else:
                        unvisited.append((new_distance, neighbor_index))

    # 构建并返回最短路径
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parents[current]
    path.reverse()

    return path, distances[end]  # 返回最短路径和最短距离


def get_outgoing_edges(node, list, graph, visited_edges):
    """检查节点是否有出边，并且这些出边是否已经被访问过"""
    outgoing_edges = []
    # 遍历当前节点的所有邻居
    for neighbor_index in range(graph.shape[1]):  # 假设graph的列数表示节点数
        if graph[list.index(node)][neighbor_index] != 0 and (node, list[neighbor_index]) not in visited_edges:
            outgoing_edges.append(list[neighbor_index])
    return outgoing_edges


def randomWalk(graph, wordlist):
    """执行随机游走并返回遍历的节点和边"""

    # 初始化已访问的节点和边
    visited_nodes = set()
    visited_edges = set()

    # 初始化遍历结果
    walk_nodes = []
    walk_edges = []

    # 随机选择一个起点
    start_node = random.choice(wordlist)
    current_node = start_node
    visited_nodes.add(start_node)
    walk_nodes.append(start_node)

    try:
        # 遍历过程
        while True:
            # 获取当前节点的所有出边
            outgoing_edges = get_outgoing_edges(current_node, wordlist, graph, visited_edges)
            if not outgoing_edges:
                break  # 如果没有出边，则退出循环

            # 随机选择一个出边
            chosen_edge = random.choice(outgoing_edges)

            # 添加到已访问的节点和边
            neighbor = chosen_edge
            walk_nodes.append(neighbor)
            walk_edges.append((current_node, neighbor))
            visited_nodes.add(neighbor)
            visited_edges.add((current_node, neighbor))

            # 更新当前节点为邻居节点
            current_node = neighbor

    # 这里可以检查用户是否想要停止遍历（例如，通过捕获Ctrl+C）
    # 如果在遍历过程中按下Ctrl+C，则会抛出KeyboardInterrupt异常
    except KeyboardInterrupt:
        print("遍历已被用户停止。")

    return walk_nodes, walk_edges


def randomWalk1(graph, wordlist, start):
    # 初始化已访问的节点和边
    visited_nodes = set()
    visited_edges = set()

    # 初始化遍历结果
    walk_nodes = []
    walk_edges = []

    if start not in wordlist:
        return walk_nodes

    start_node = start
    current_node = start_node
    visited_nodes.add(start_node)
    walk_nodes.append(start_node)

    while True:
        # 获取当前节点的所有出边
        outgoing_edges = get_outgoing_edges(current_node, wordlist, graph, visited_edges)
        if not outgoing_edges:
            break  # 如果没有出边，则退出循环

        # 随机选择一个出边
        chosen_edge = random.choice(outgoing_edges)

        # 添加到已访问的节点和边
        neighbor = chosen_edge
        walk_nodes.append(neighbor)
        walk_edges.append((current_node, neighbor))
        visited_nodes.add(neighbor)
        visited_edges.add((current_node, neighbor))

        # 更新当前节点为邻居节点
        current_node = neighbor

    return walk_nodes


def menu():
    print("1. 读取文件并生成有向图")
    print("2. 查询桥接词")
    print("3. 生成新文本")
    print("4. 计算最短路径")
    print("5. 随机游走")


# # 文本预处理
# processed_words = process_text_file("a.txt")
# print(processed_words)
# if not processed_words:
#     print("There are no words.")
#     exit(0)
#
# # 生成单词表
# wordlist = []
# for i in processed_words:
#     if i not in wordlist:
#         wordlist.append(i)
#
# # 将文本用数字数组表示
# wordnumber = []
# for i in processed_words:
#     for j in range(len(wordlist)):
#         if wordlist[j] == i:
#             wordnumber.append(j)
#
# # 生成有向图矩阵
# digraph = np.zeros((len(wordlist), len(wordlist)))
# print(digraph.shape)
# for i in range(len(wordnumber) - 1):
#     temp1 = wordnumber[i]
#     temp2 = wordnumber[i + 1]
#     digraph[temp1][temp2] = digraph[temp1][temp2] + 1
#
# # 命令行操作
# menu()
# lang = input("选择操作：")  # 里边填序号以及对应操作
# if lang == "1":
#     # print(digraph)
#     showDirectedGraph(processed_words, wordnumber)
#
# elif lang == "2":
#     Stringword1 = input("写入单词1：")
#     Stringword2 = input("写入单词2：")
#     # 检测是否存在此单词
#     if Stringword1 not in wordlist:
#         if Stringword2 not in wordlist:
#             print("No", Stringword1, "and", Stringword2, "in the graph!")
#         else:
#             print("No", Stringword1, "in the graph!")
#     elif Stringword2 not in wordlist:
#         print("No", Stringword2, "in the graph!")
#     else:
#         result = queryBridgeWords(Stringword1, Stringword2, wordlist, digraph)
#         if not result:
#             print("No bridge words from", Stringword1, "to", Stringword2)
#         elif len(result) == 1:
#             print("The bridge word from", Stringword1, "to", Stringword2, "is:", wordlist[result[0]])
#         else:
#             print("The bridge words from", Stringword1, "to", Stringword2, "are:")
#             for i in range(len(result) - 1):
#                 print(str(wordlist[result[i]]) + ',')
#             print(str(wordlist[result[-1]]))
#
# elif lang == "3":
#     text = input("输入新文本：")
#     # 文本处理
#     text = text.lower()
#     text = text.split()
#     newtext = generateNewText(text, wordlist, digraph)
#     newtext_string = ' '.join(newtext)
#     print(newtext_string)
#
# elif lang == "4":
#     Stringword1 = input("写入单词1：")
#     Stringword2 = input("写入单词2：")
#     # 检测是否存在此单词
#     if Stringword1 not in wordlist:
#         if Stringword2 not in wordlist:
#             print("No", Stringword1, "and", Stringword2, "in the graph!")
#         else:
#             print("No", Stringword1, "in the graph!")
#     elif Stringword2 not in wordlist:
#         print("No", Stringword2, "in the graph!")
#     else:
#         shortest_path, shortest_distance = calcShortestPath(Stringword1, Stringword2, wordlist, digraph)
#         if shortest_distance < float('inf'):
#             print(shortest_path)
#             print(shortest_distance)
#             showDirectedGraph(processed_words, wordnumber, shortest_path)
#         else:
#             print("Unreachable.")
#
# elif lang == "5":
#     walk_nodes, walk_edges = randomWalk(digraph, wordlist)
#     with open("walk_results.txt", "w") as f:
#         for node in walk_nodes:
#             f.write(str(node) + " ")
#
# elif lang == "6":
#     start = input("333:")
#     walk_nodes = randomWalk1(digraph, wordlist, start)
#     print(walk_nodes)
#
# else:
#     print("输入有误")
