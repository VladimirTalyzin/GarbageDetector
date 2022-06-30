from csv import writer, reader
from os import listdir
from os.path import isfile, join

# получить все файлы из указанной папки
def getAllFiles(path):
    return [file for file in listdir(path) if isfile(join(path, file))]

# создать csv-файл с распределением классов в зависимости от файлов в папках
def declassify(resultCSV, sampleCSV, pathEmpty, pathBad, pathNormal):
    declassified = {}
    for file in getAllFiles(pathEmpty):
        declassified[file] = 0

    for file in getAllFiles(pathNormal):
        declassified[file] = 1

    for file in getAllFiles(pathBad):
        declassified[file] = 2

    result = []

    # считываем все строки из файла-примера, чтобы выдать результат по тем же файлам и в том же порядке
    with open(sampleCSV) as csvFile:
        csvReader = reader(csvFile, delimiter = ',')
        csvReader.__next__()
        for row in csvReader:
            fileName = row[0]
            resultRow = [fileName]
            if fileName in declassified:
                resultRow.append(declassified[fileName])
            else:
                # если такой файл был не найден в папке
                resultRow.append(-1)

            result.append(resultRow)

    # вывести полученные данные в указанный новый csv-файл
    with open(resultCSV, "w", encoding = "utf8", newline = "") as csvFile:
        csvWriter = writer(csvFile, delimiter = ",")
        csvWriter.writerow(["ID_img", "class"])
        for row in result:
            csvWriter.writerow(row)


# сформировать новый тренировочный файл по папкам с файлами
declassify("new_train.csv", "train.csv", "classify_train/empty/", "classify_train/bad/", "classify_train/normal/")