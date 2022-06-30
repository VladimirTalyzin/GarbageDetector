from torch import nn, optim
from pandas import read_csv
from sklearn.model_selection import train_test_split

from model import Model
from train import train
from utility import prepareDataset
from dataset import ImageDataset
# noinspection PyUnresolvedReferences
from config import trainFilename, checkFilename, modelFilename

if __name__ == '__main__':
    # считываем названия файлов и их классов из файла для тренировки
    trainData = read_csv(trainFilename)

    # разбиваем тренировочную выборку на две части - одну для обучения, другую для проверки обучения
    # разбивка каждый раз разная, так как мы несколько раз ищем оптимальную модель
    trainData, checkData = train_test_split(trainData, test_size = 0.2)

    trainDataset = ImageDataset(data = trainData, forTraining = True, isCheckDataSet = True)
    checkDataset = ImageDataset(data = checkData, forTraining = True, isCheckDataSet = True)

    # создаём начальную модель Resnet для GPU
    model = Model(loadModelFromFile = None, cpuMode = False)

    # запускаем тренировку
    # начальные параметры - оптимизация Adam 0.001 и 15 эпох обучения, оказались оптимальными
    # целевая функция - уменьшение энтропии между определением данных для обучающей выборки и тестовой
    # среднеквадратичное отклонение вызывало переобучение, поэтому не используется
    train(model,
         criterion = nn.CrossEntropyLoss(),
         optimizer = optim.Adam(model.parameters(), lr = 0.001),
         trainData = prepareDataset(trainDataset, isTrainDataset = True),
         checkData = prepareDataset(checkDataset, isTrainDataset = False),
         epochsCount = 15)

    # сразу после обучения, сохранить драгоценную модель в файл
    model.save(saveModelFileName = modelFilename)