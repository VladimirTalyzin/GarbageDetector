from os import path
from sys import argv
from json import dump

from config import modelFilename
from dataset import ImageDataset
from model import Model
from numpy import unique, argmax, where
from utility import prepareDataset, getResultsName

# название файла для разбора должно быть указано в командной строке, сразу после названия программы .py
if __name__ == '__main__' and len(argv) > 1:
    file = argv[1]

    if not path.isfile(file):
        print("File " + file + " not found!")
        exit(0)

    # вызываем модель в режиме работы на CPU
    model = Model(loadModelFromFile = modelFilename, cpuMode = True)

    # Файл проверяется несколько раз, из-за RandomResizedCrop(224),
    # применяемого к изображению. Желательно - нечётное количество
    fileRepeat = [file, file, file, file, file]
    checkDataset = ImageDataset(data = fileRepeat, forTraining = False, isCheckDataSet = True)

    classIndex = None
    certainty = None

    # обрабатываем сразу все варианты картинки
    batchSize = len(fileRepeat)
    for images in prepareDataset(checkDataset, False, specifiedBatchSize = batchSize):
        images = images.cpu()
        # предсказываем классы для картинок
        predictions = model.prediction(images)
        classIndexes, counts = unique(predictions.argmax(axis = 1), return_counts = True)

        # самый часто встретившийся класс
        classIndex = classIndexes[argmax(counts)]

        # метрика уверенности определения
        certainty = where(predictions.argmax(axis = 1) == 1, (predictions.amax(axis = 1) - predictions.mean(axis = 1)).detach().numpy(), -100).max()


    # выводим данные в папку с результатами
    result = {"class": int(classIndex), "certainty": round(float(certainty), 2)}
    with open(getResultsName(file), "w") as resultFile:
        dump(result, resultFile)

    print("CLASS: " + str(classIndex))