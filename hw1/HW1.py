from matplotlib import pyplot as plt


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def calculate_density(database):
    result = dict()
    for building,(x1,y1,space) in database.items():
        density = (space - 0.3 * space) / 18
        result[building] = [x1,y1,density]
    return (result)


def read_data(path: str) -> dict[str, tuple]:
    database = {}
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip().split("\t")
            database[line[0]] = tuple(float(x) for x in line[1:])
    return database

def task1(database: dict[str, tuple],res:list) -> list[tuple]:
    shops = dict()
    radius = 0.5
    for building, coords1 in database.items():
        x1, y1, space1 = coords1
        shops[building] = [x1, y1, 0]
        for next_building, coords2 in database.items():
            if building == next_building: continue
            x2, y2, space2 = coords2

            dist = distance(x1, y1, x2, y2)
            if dist < radius:
                shops[building][0] = x1
                shops[building][1] = y1
                shops[building][2] += 1
    temp = []
    for addr, (i, j, k) in shops.items():
        temp.append([addr, k, i, j])
    temp.sort(key=lambda x: x[1], reverse=True)
    for i in temp:
        res.append((i[2],i[3]))
    return res[0]



def task2(database: dict[str, tuple],res) -> list[tuple]:
    res2 = [res[0]]
    count = 0
    for i in res:
        flag = True
        if count == 10:
            break
        for j in res2:
            dist = distance(i[0], i[1], j[0], j[1])
            if dist <= 1:
                flag = False
                break
        if flag:
            res2.append(i)
            count +=1
    return res2


def task3(database: dict[str, tuple]) -> list[tuple]:
    shops = calculate_density(database)
    res = dict()
    for building,(x1,y1,density1) in shops.items():
        res[building] = [x1,y1,0]
        for next_building,(x2,y2,density2) in shops.items():
            if building == next_building:continue
            dist = distance(x1,y1,x2,y2)
            if dist <= 0.5:
                res[building][2] += density2
    temp = []
    for addr, (i, j, k) in res.items():
        temp.append([addr, k, i, j])
    temp.sort(key=lambda x: x[1], reverse=True)
    a = []
    for i in temp:
        a.append((i[2],i[3]))
    res2 = [a[0]]
    count = 0
    for i in a:
        flag = True
        if count == 15:
            break
        for j in res2:
            if distance(i[0],i[1],j[0],j[1]) < 1:
                flag = False
                break
        if flag:
            res2.append(i)
            count +=1
    return res2











def plot(database: dict[str, tuple], best_coords: list):
    """
    DO NOT CHANGE!
    Args:
        database (dict): изначальный датасет словарь, ключ адрес, значение (x, y, площадь)
        best_coords (list): для задачи 1 это (x, y), для задачи 2-3 это [(x1,y1), (x2,y2) ... (xn,yn)]
    """
    plt.close()
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.plot(
        [coord[0] for coord in database.values()],
        [coord[1] for coord in database.values()],
        '.', ms=5, color='k', alpha=0.5)
    if isinstance(best_coords[0], tuple):
        for x, y in best_coords:
            circle = plt.Circle((x, y), 0.5, color='r', fill=False, zorder=2)
            ax.add_patch(circle)
        plt.plot(
            [coord[0] for coord in best_coords],
            [coord[1] for coord in best_coords],
            '.', ms=15, color='r')
    elif isinstance(best_coords[0], float):
        x, y = best_coords
        circle = plt.Circle((x, y), 0.5, color='r', fill=False, zorder=2)
        ax.add_patch(circle)
        plt.plot(*best_coords, '.', ms=15, color='r')
    else:
        raise ValueError("Проверь, что подаёшь список кортежей или кортеж из двух координат")
    plt.show()


def homework():
    path = "buildings"
    database = read_data(path)
    res = []

    best_task1 = task1(database,res)
    plot(database, best_task1)
    best_task2 = task2(database,res)
    plot(database, best_task2)

    best_task3 = task3(database)
    plot(database, best_task3)


if __name__ == '__main__':
    homework()
