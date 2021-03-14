
sample = [58, 14, 23, 70, 297, 112, 237, 475, 279, 738,
          134, 4, 120, 90, 401, 13, 405, 52, 1007, 19,
          77, 12, 32, 259, 46, 518, 51, 0, 172, 512, 13,
          1, 119, 128, 310, 131, 235, 284, 79, 16, 69,
          18, 305, 461, 12, 93, 85, 348, 48, 146, 121,
          39, 126, 415, 419, 28, 39, 516, 65, 2, 36,
          192, 34, 21, 346, 622, 617, 59, 330, 580, 80,
          6, 960, 234, 52, 438, 170, 75, 92, 340, 403,
          177, 113, 55, 87, 51, 165, 58, 1271, 4, 51,
          300, 48, 56, 112, 139, 22, 226, 127, 186]

Y = 0.87
TIME_WITHOUT_FAILURE = 388  # безвідмовна робота на час
INTENSITY_FAILURE_TIME = 1012  # інтенсивність відмов на час

# Знаходимо середній наробіток до відмови та сортуємо вхідну вибірку
Tavr = sum(sample) / len(sample)
sample.sort()

# Ділимо інтервал від 0 до максимального значення та знаходимо межі для 10 інтервалів
intervals = 10
h = (sample[-1] - 0) / intervals
intervals_list = []
for i in range(10):
    intervals_list.append([round(h*i, 1), round(h*(i+1), 1)])

# Розподіляємо всі значення виборки по інтервалам
sample_intervals = [[] for _ in range(intervals)]

for i in range (len(intervals_list)):
    for j in sample:
        if intervals_list[i][0] <= j <= intervals_list[i][1]:
            sample_intervals[i].append(j)

# Рахуємо значення статичної щільності розподілу ймовірності відмови
fi = []
for i in sample_intervals:
    fi.append(round(len(i)/(len(sample)*h), 6))

# Ймовірність безвідмовної роботи пристрою для кожного інтервалу(на час правої межі інтервалу)
P_list = [1]
for i in range(intervals):
    square = 0
    for j in range(i+1):
        square += (fi[j] * h)
    P_list.append(round(1 - square, 6))

# Відсотковий наробіток на відмову Ту
for i in range(len(P_list)+1):
    if P_list[i-1] > Y >= P_list[i]:
        d = round((P_list[i-1] - Y) / (P_list[i-1] - P_list[i]), 2)
        T = round(fi[i-1] + h*d, 2)

# Функція для визначення інтервалу заданого часу
def which_interval(interval, time):
    for i in range(interval+1):
        if intervals_list[i][0] <= time <= intervals_list[i][1]:
            return i

# Функція для розрахунку ймовірностей
def probability(time, interval):
    index = which_interval(interval, time)
    P = 1
    for i in range(interval):
        if i != index:
            P -= fi[i]*h
        else:
            P -= fi[i]*(time - intervals_list[i][0])
            return round(P, 6)

def intensity(interval, time):
    index = which_interval(interval, time)
    p = probability(time, intervals)
    return round(fi[index] / p, 6)

P = probability(TIME_WITHOUT_FAILURE, intervals) # Ймовірність безвідмовної роботи на час 388 год

Lambda = intensity(intervals, INTENSITY_FAILURE_TIME) # Знайдемо інтенсивність відмов на час 1012 год

print("Середній наробіток до відмови Tср = {}.".format(Tavr))
print("y-відсотковий наробіток на відмову при y = {}. Ty = {}.".format(Y, T))
print("Ймовірність безвідмовної роботи на час {} годин: P = {}.".format(TIME_WITHOUT_FAILURE, P))
print("Інтенсивність відмов на час {} годин: lambda = {}.".format(INTENSITY_FAILURE_TIME, Lambda))

