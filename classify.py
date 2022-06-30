from csv import reader
from shutil import rmtree
from os import mkdir

# noinspection PyUnresolvedReferences
from config import pathTraining, pathCheckData

# удалить все файлы и папки внутри указанной папки
def clearPath(path):
    rmtree(path, ignore_errors = True)
    mkdir(path)

# распределить файлы по указанным папкам, в зависимости от их класса
def classify(csvFilename, path, pathEmpty, pathBad, pathNormal):
    # все старые файлы и папки удаляются
    clearPath(pathEmpty)
    clearPath(pathBad)
    clearPath(pathNormal)

    # считываем их csv-файла все названия файлов и их классы
    with open(csvFilename) as csvFile:
        csvReader = reader(csvFile, delimiter=',')
        csvReader.__next__()
        for row in csvReader:
            fileName = row[0]
            imageType = int(float(row[1]))

            # в csv-файле может не быть расширения. В этом случае, добавляем его
            realFilename = fileName if "." in fileName else fileName + ".jpg"

            # в зависимости от класса, распределяем файл в нужную папку
            if imageType == 0:
                open(pathEmpty + fileName, 'wb').write(open(path + realFilename , 'rb').read())
                print(realFilename + " is empty")
            elif imageType == 1:
                open(pathNormal + fileName, 'wb').write(open(path + realFilename, 'rb').read())
                print(realFilename + " is normal")
            elif imageType == 2:
                open(pathBad + fileName, 'wb').write(open(path + realFilename, 'rb').read())
                print(realFilename + " is bad")


# классифицируем последний обработанный тренировочный файл
classify("train_manual_0.96.csv", pathTraining, "classify_train/empty/", "classify_train/bad/", "classify_train/normal/")

# если раскомментировать, можно также посмотреть, какое распределение получилось
# после тренировки и предсказания классов
#classify("result.csv", pathCheckData, "classify/empty/", "classify/bad/", "classify/normal/")