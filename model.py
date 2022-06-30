import torch
from torchvision import models
import torch.nn as nn

class Model:
    # режим работы модели
    # GPU - False, CPU - True
    # на слабых VPS нет GPU, при этом есть отличия в данных, сохраняемых Torch в моделях
    cpuMode = False

    # loadModelFromFile - имя файла, из которого будет загружена натренированная модель
    # или None для новой тренировки
    # cpuMode - режим работы. GPU - False, CPU - True
    def __init__(self, loadModelFromFile, cpuMode):

        # опытным путём было определено, что ResNet50
        # оптимально для решения задачи конкурса
        resnet = models.resnet50(pretrained=True)
        #resnet = models.resnet101(pretrained=True)

        # указываем настройки модели ResNet
        # 2048 входных параметров (изначально задано для для ResNet50)
        # 3 варианта класса изображения. 0 - нет, 1 - есть, 2 - плохое качество
        resnet.fc = nn.Linear(2048, 3)

        self.cpuMode = cpuMode

        # в зависимости от режима инициализируем модель
        if cpuMode:
            self.__model__ = resnet.cpu()
        else:
            self.__model__ = resnet.cuda()
            # для режима GPU необходимо очистить кэш, чтобы освободить всю доступную память видеокарты
            # иначе её может нехватить
            torch.cuda.empty_cache()

        # если указан файл загрузки модели
        # то загружаем оттуда веса
        if loadModelFromFile is not None:
            self.__model__.load_state_dict(torch.load(loadModelFromFile))
            self.__model__.eval()

    # сохранить модель в файл
    def save(self, saveModelFileName):
        torch.save(self.__model__.state_dict(), saveModelFileName)

    # по правилам ООП, которые мало кто знает и ещё меньше кто выполняет,
    # обращаться к свойствам класса напрямую нельзя вообще никогда
    # я стараюсь придерживаться этого правила, если хватает времени
    # Python не имеет ключевых слов для определения доступности
    # членов класса, но в IDE PyCharm принято соглашение, что
    # для private свойств и методов имя начинается на __

    def getModelForTraining(self):
        return self.__model__

    def prediction(self, images):
        return self.__model__(images)

    def parameters(self):
        return self.__model__.fc.parameters()