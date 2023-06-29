class knn:
    class point:
        def __init__(self, attributes, main_attribute):
            # Конструктор класса point, инициализирует атрибуты объекта
            self.attributes = attributes  # Атрибуты точки
            self.main_attribute = main_attribute  # Главный атрибут точки

    def read_lines(self, path):
        # Метод для чтения строк из файла
        with open(path, 'r') as file:
            self.lines = [line.rstrip('\n') for line in file.readlines()]
            # Чтение всех строк из файла и сохранение в self.lines

    def line_to_point(self, line):
        # Метод для преобразования строки в объект point
        parts = line.strip().split(',')
        # Разделение строки на части по запятой
        attributes = parts[:-1]
        # Атрибуты - все части строки, кроме последней
        main_attribute = parts[-1]
        # Главный атрибут - последняя часть строки
        return self.point(attributes, main_attribute)
        # Возвращение нового объекта point с указанными атрибутами и главным атрибутом

    def train(self):
        # Метод для обучения модели
        self.points = [self.line_to_point(line) for line in self.lines]
        # Создание списка объектов point из строк self.lines

    def get_testset(self, path):
        # Метод для получения тестового набора данных
        with open(path, 'r') as file:
            self.testlines = [line.rstrip('\n') for line in file.readlines()]
            # Чтение всех строк из файла и сохранение в self.testlines
        self.testset = [self.line_to_point(line) for line in self.testlines]
        # Создание списка объектов point из строк self.testlines

    def set_k(self, k):
        # Метод для установки значения k
        self.k = k
        # Установка значения k

    def find_distance(self, p1, p2):
        # Метод для вычисления расстояния между двумя точками
        distance = 0
        for i in range(0, len(p1.attributes)):
            # Проход по всем атрибутам точки
            distance += (float(p1.attributes[i]) - float(p2.attributes[i])) ** 2
            # Добавление квадрата разности значений атрибутов к расстоянию
        return distance
        # Возвращение вычисленного расстояния

    def test_point(self, point):
        # Метод для классификации точки на основе ближайших соседей
        distances = []
        for i in self.points:
            # Проход по всем точкам из обучающего набора
            distances.append((self.find_distance(i, point), i.main_attribute))
            # Добавление пары (расстояние, главный атрибут точки) в список distances
        distances.sort(key=lambda x: x[0])
        # Сортировка расстояний по возрастанию
        k_nearest = distances[:self.k]
        # Выбор k точек с наименьшими расстояниями
        attribute_counts = {}
        for _, attribute in k_nearest:
            # Проход по выбранным точкам с наименьшими расстояниями
            if attribute in attribute_counts:
                attribute_counts[attribute] += 1
            else:
                attribute_counts[attribute] = 1
            # Подсчет количества точек каждого класса
        max_count = 0
        max_attribute = None
        for attribute, count in attribute_counts.items():
            # Проход по подсчитанным количествам точек каждого класса
            if count > max_count:
                max_count = count
                max_attribute = attribute
                # Обновление значения максимального количества и главного атрибута
        return max_attribute
        # Возвращение главного атрибута класса с наибольшим количеством точек

    def test(self):
        # Метод для выполнения тестирования модели
        correct = 0
        all = 0
        for i in self.testset:
            # Проход по всем точкам в тестовом наборе
            if self.test_point(i) == i.main_attribute:
                correct = correct + 1
            all = all + 1
            # Подсчет количества правильно классифицированных точек и общего количества точек
        return correct/all*100
        # Возвращение точности классификации в процентах

my_knn = knn()
# Создание экземпляра класса knn
my_knn.read_lines("iris.data")
# Чтение строк из файла "iris.data"
my_knn.train()
# Обучение модели
my_knn.get_testset("iris.test.data")
# Получение тестового набора данных из файла "iris.test.data"

for i in range(1, 50):
    # Цикл для каждого значения k от 1 до 49
    my_knn.set_k(i)
    # Установка значения k
    print("With k " + str(i) + " result is " + str(my_knn.test()))
    # Вывод результата классификации с использованием текущего значения k

while True:
    # Бесконечный цикл
    vector = input("Enter your vector:\n")
    # Ввод вектора от пользователя
    print(my_knn.test_point(my_knn.line_to_point(vector)))
    # Классификация введенного вектора и вывод результата
