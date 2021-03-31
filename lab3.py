from lab2 import *
import math

#Параметри з методички
probs = [0.5, 0.6, 0.7, 0.8, 0.85, 0.90, 0.92, 0.94]

# probs = [0.16, 0.36, 0.28, 0.58, 0.27, 0.93, 0.48, 0.20, 0.35]

P = round(P, 6)    # ймовірність відмови, яку берему з минулої роботи
T = 1000           # час
K1, K2 = 1, 1      # кратності резервування

Q = 1 - P

Tsystem = round(-T/math.log1p(P-1))

def reservation_quality_criteria(Qr, Pr, Tr):
    Gq = round(Qr/Q, 2)
    Gp = round(Pr/P, 2)
    Gt = round(Tr/Tsystem, 2)

    return Gq, Gp, Gt

def general_unloaded(q, K):
    qr = round(1/math.factorial(K+1) * q, 6)

    return qr

def separate_loaded(p, K):
    qr = round((1 - p) ** (K + 1), 6)

    return qr

def general_loaded(p, K):
    pr = round(1 - (1-p) ** (K + 1), 6)

    return pr

print("Скористаємося результатами попередноьої роботи\nPsystem({}) = {}\nQsystem({}) = {}\nTsystem = {}".format(T, P, T, Q, Tsystem))

Qreserved_system = general_unloaded(Q, K1)
Preserved_system = 1 - Qreserved_system
# Preserved_system = general_loaded(P, K1)
# Qreserved_system = 1 - Preserved_system
Treserved_system = round(-T/math.log1p(Preserved_system-1))
print("Обрахуємо ймовірність відмови на час {} годин системи з загальним навантаженням і кратністю {}\n"
      "Qreserved system({}) = {}\nЗвідси знайдемо ймовірність безвідмовної роботи і значення середнього наробітку\n"
      "Preserved system = {}\n"
      "Treserved system = {}".format(T, K1, T, Qreserved_system, Preserved_system, Treserved_system))

Gq, Gp, Gt = reservation_quality_criteria(Qreserved_system, Preserved_system, Treserved_system)
print("Також розрахуємо виграш надійності протягом часу {} годин за ймовірностю відмов:\nGq = {}\n"
      "виграш надійності протягом часу {} годин за ймовірностю безвідмовної роботи:\nGp = {}\n"
      "виграш надійності за середнім часом безвідмовної роботи:\nGt = {}".format(T, Gq, T, Gp, Gt))

Qreserved = [[] for _ in range(len(probs))]
Preserved = dict()
# for i in range(len(Qreserved)):
#     Qreserved[i] = general_unloaded(1 - probs[i], K2)
#     Preserved.update({str(i+1) : round(1 - Qreserved[i], 6)})
for i in range(len(Qreserved)):
    Qreserved[i] = separate_loaded(probs[i], K2)
    Preserved.update({str(i+1) : 1 - Qreserved[i]})

print("Обрахуємо ймовірність відмови та безвідмовної роботи кожного елемента системи при його "
      "ненавантаженому резервуванні з кратністю {}\nQreserved = {}\nPreserved = {}".format(K2, Qreserved, Preserved.values()))

# Ймовірність в цілому, шляхом перебору
all_probabilities = []
for i in all_system_states:
    probability = 1
    for k in graph.keys():
        if k in i and k !="end" and k !="start":
            probability *= Preserved[k]
        elif k not in i and k !="end" and k !="start":
            probability *= 1 - Preserved[k]
    all_probabilities.append(probability)

Preserved_system = round(sum(all_probabilities), 6)

Qreserved_system = round(1 - Preserved_system, 6)

Treserved_system = round(-T/math.log1p(Preserved_system-1))

Gq, Gp, Gt = reservation_quality_criteria(Qreserved_system, Preserved_system, Treserved_system)

print("Використавши метод перебору з минулої роботи розрахуємо"
      "ймовірність безвідмовної роботи в цілому:\nPreserved system = {}\n"
      "ймовірність безвідмовної роботи і значення середнього наробітку\n"
      "Qreserved system = {}\n"
      "Treserved system = {}\n"
      "Також розрахуємо виграш надійності протягом часу {} годин за ймовірностю відмов:\nGq = {}\n"
      "виграш надійності протягом часу {} годин за ймовірностю безвідмовної роботи:\nGp = {}\n"
      "виграш надійності за середнім часом безвідмовної роботи:\nGt = {}".format(Preserved_system, Qreserved_system, Treserved_system,
                                                                                 T, Gq, T, Gp, Gt))

