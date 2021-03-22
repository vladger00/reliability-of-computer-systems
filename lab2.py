import itertools
# start - початок, end - кінець
graph = {
    "start": ["1", "2"],
    "1": ["3", "4"],
    "2": ["3", "5"],
    "3": ["4", "5"],
    "4": ["7", "8"],
    "5": ["6"],
    "6": ["7", "9"],
    "7": ["8", "9"],
    "8": ["end"],
    "9": ["end"],
    "end": []
}

# Задані ймовірності кожного стану
probabilities = {"start": 0.0, "1": 0.16, "2": 0.36, "3": 0.28, "4": 0.58, "5": 0.27, "6": 0.93, "7": 0.48, "8": 0.20,"9": 0.35, "end": 0.0}

# Параметри з прикладу в методичці

# graph = {
#     "start": ["1"],
#     "1": ["2", "3"],
#     "2": ["4", "5"],
#     "3": ["4", "6", "8"],
#     "4": ["5", "6", "8"],
#     "5": ["6", "7"],
#     "6": ["7", "8"],
#     "7": ["end"],
#     "8": ["end"],
#     "end": []
# }
#
# # Задані ймовірності кожного стану
# probabilities = {"start": 0.0, "1": 0.5, "2": 0.6, "3": 0.7, "4": 0.8, "5": 0.85, "6": 0.90, "7": 0.92, "8": 0.94, "end": 0.0}

# Функція для знаходження усіх можлививх шляхів, якими можна прпойти від початку до кінця
def paths(first_state, last_state, graph, curr_path = []):
    curr_path = curr_path + [first_state]
    all_paths = []
    if first_state == last_state:
        return [curr_path]
    if first_state not in graph:
        return []
    for i in graph[first_state]:
        if i not in curr_path:
            create_paths = paths(i, last_state, graph, curr_path)
            for j in create_paths:
                all_paths.append(j)
    return all_paths

# Знаходимо всі шляхи за допомогою функції
all_paths = paths("start", "end", graph)

# Для зручності, зробимо масив з усіма можливими комбінаціями наших станів
# а потім зкомбінуємо їх з всіма можливими шляхами

comb = []
full_list_comb = []
all_states = graph.keys()
for i in range(1, len(graph.keys()) + 1):
    comb.append(list(itertools.combinations(all_states, i)))
for j in comb:
    for i in j:
        full_list_comb.append(i)

# Знайдемо усі можливі стани системи
all_system_states = []
for i in full_list_comb:
    for j in all_paths:
        if set(j).issubset(set(i)):
            all_system_states.append(i)
all_system_states = set(all_system_states)

# Розрахуємо ймовірності для кожного стану
all_probabilities = []
string = ""
for i in all_system_states:
    probability = 1
    for k in graph.keys():
        if k in i and k !="end" and k !="start":
            string += "+    "
            probability *= probabilities[k]
        elif k not in i and k !="end" and k !="start":
            string += "-    "
            probability *= 1 - probabilities[k]
    string += str(round(probability, 6)) + "\n"
    all_probabilities.append(probability)

# Визначимо ймовірність безвідмовної роботи системи як суму ймовірностей знаходження системи в працездатних станах
P = sum(all_probabilities)
print("Ймовірність безвідмовної роботи системи: ", round(P, 6))

# Також виведу матрицю зв'язків та усі можливі стани системи з їх ймовірностями

title = ""
for i in range(len(graph) - 2):
    title += "E" + str(i+1) + "   "

print("Таблиця зв'язків системи")
print("   ", title)
matrix = ""
for i in range(1, len(graph) -  1):
    matrix += "E" + str(i) + "  "
    for j in range(1, len(graph) -  1):
        if str(j) in graph[str(i)]:
            matrix += "1    "
        else:
            matrix += "0    "
    matrix += "\n"
print(matrix)

print("Усі можливі шляхи")
path_string = ""
for i in all_paths:
    for j in i:
        path_string += "E" + str(j) + "->"
    path_string += "\n"
print(path_string)

print("Таблиця працездатних станів системи")
print(title + "Pstate")
print(string)
