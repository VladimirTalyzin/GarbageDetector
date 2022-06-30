import os
from math import sqrt

from PIL import Image, ImageFilter, ImageStat, ImageEnhance
from torch import utils
from config import normalBrightnessFile, pathPreparedTraining, pathPreparedCheck, pathPreparedUser, pathUserResults

# корректировка яркости изображения
def brightness(filename):
   image = Image.open(filename)
   stat = ImageStat.Stat(image)
   red, green, blue = stat.mean
   # учитывается, что цвета RGB имеют разную яркость
   # взвешенное среднеквадратичное
   return sqrt(0.241 * (red * red) + 0.691 * (green * green) + 0.068 * (blue * blue))


# при первом вызове модуля, расчитываем яркость
# эталонного файла
standardBrightness = brightness(normalBrightnessFile)

def processImage(imagePath, imageName, isCheckImage):
    # получаем имя изображения
    # в csv-файлах изображения указаны без пути
    # но для предсказания класса на VPS, указывается полный путь
    if "/" in imageName:
        filename = imageName
        preparedPath = pathPreparedUser + imageName.split("/")[-1]
    elif "\\" in imageName:
        filename = imageName
        preparedPath = pathPreparedUser + imageName.split("\\")[-1]
    else:
        filename = imagePath + imageName
        preparedPath = (pathPreparedCheck if isCheckImage else pathPreparedTraining) + imageName

    if not os.path.isfile(preparedPath):
        image = Image.open(filename)
        # увеличиваем общую резкость изображения
        image = image.filter(ImageFilter.SHARPEN)
        # увеличиваем резкость мелких деталей изображения
        image = image.filter(ImageFilter.DETAIL)
        # нормализуем яркость по яркости эталона
        image = ImageEnhance.Brightness(image).enhance(standardBrightness / brightness(filename))
        image.save(preparedPath)

    return preparedPath

# получение имени файла для сохранения результатов предсказания
# затем внешние программы могут зайти в папку pathUserResults
# и прочитать там результаты
def getResultsName(imageName):
    if "/" in imageName:
        return pathUserResults + (imageName.split("/")[-1]).split(".")[0:-1][0] + ".json"

    elif "\\" in imageName:
        return pathUserResults + (imageName.split("\\")[-1]).split(".")[0:-1][0] + ".json"

    else:
        return pathUserResults + imageName

# подготовка списка изображений для тренировки или распознавания класса
# Torch применяет единую функцию для работы
# поэтому здесь она дополнена параметрами, но также
# единая для тренировки и распознавания
def prepareDataset(dataset, isTrainDataset, specifiedBatchSize = None):
    # noinspection PyUnresolvedReferences
    return utils.data.DataLoader(dataset = dataset,
                                 batch_size = 16 if specifiedBatchSize is None else specifiedBatchSize,
                                 shuffle = isTrainDataset,
                                 pin_memory = True,
                                 num_workers = 2)