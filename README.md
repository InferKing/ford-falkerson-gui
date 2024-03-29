# Алгоритм Форда-Фалкерсона.

## Установка и запуск программы

Для начала клонируем репозиторий (необходим Git на компьютере)

```
mkdir my-folder
cd my-folder
git init
git clone https://github.com/InferKing/ford-falkerson-gui.git
```

Или клонируем в уже существующую папку

```
git init
git clone https://github.com/InferKing/ford-falkerson-gui.git
```

Далее **ОБЯЗАТЕЛЬНО** создайте и активируйте виртуальное окружение для работы проекта

```
cd ford-falkerson-gui
python -m venv .venv
source .venv/scripts/activate
```

Теперь устанавливаем в виртуальное окружение необходимые модули

```
pip install -r requirements.txt
```

Последний шаг - запуск программы. 

```
python main.py
```

Наслаждаемся программой и читаем дальше как работать с ней!

## Исток
В поле "Исток" нужно указывать с какой вершиной графа происходит соединение, 
а также поток, который может передаваться по этому пути (дуге). 

Пример указания значений в поле "Исток":

```
A=200, B=400, C=350
```
Как это выглядит в самом приложении:

![Поле исток](images/picture1.png "Исток (O): A=200, B=400, C=350")

Учтите, что программа сама выбирает имена для всех вершин. 
Исток всегда называется O, сток всегда Z. 
Остальные вершины называются согласно латинскому алфавиту в ВЕРХНЕМ РЕГИСТРЕ. 

На данный момент программа поддерживает только 26 вершин. 

## Правило указания дуг и пропускной способности
Для того чтобы указать соединение между вершинами (дугами), 
необходимо в поле ввода прописать наименование вершины, а также число - пропускную способность.

Данные должны разделяться знаком равно (=). 

Пары должны разделяться запятой (,)

Пример ввода данных выглядит следующим образом:
```
A=200, B=300, C=400, D=800
```
Данные могут разделяться большим количеством пробелов или вообще без них. 
Главное условие правильной обработки ввода - наличие знака (=) между наименованием вершины и пропускной способностью, а также (,) между парами данных.

### Пример правильного заполнения данных

К примеру, необходимо составить граф следующего вида и найти его пропускную способность:

![Правильное заполнение данных](images/picture2.png "Поиск максимальной пропускной способности")

Заполним данные в графическом интерфейсе:

![Заполняем данные в GUI](images/picture3.png "Заполняем данные")

Теперь нажимаем кнопку **"Перейти к графу"**:

![Результат](images/picture4.png "Получаем результат")

Наслаждаемся результатом! Если вас не устраивает как выглядит граф, 
вы можете закрыть открывшееся окно и нажать заново **"Перейти к графу"**, чтобы получить другое отображение графа.
