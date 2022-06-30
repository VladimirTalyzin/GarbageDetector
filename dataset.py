from torchvision import transforms
from PIL import Image
from torch.utils.data import Dataset

from torch import tensor
import cv2

from utility import processImage
from config import pathTraining, pathCheckData
from pandas import DataFrame

# класс подготовки набора изображений для тренировки или распознавания
class ImageDataset(Dataset):
    # data - список названий изображений
    # forTraining - True, если в данных указаны и нужны метки распределения по классам.
    # Так должно быть для обучения
    # isCheckDataSet - тип папки файлов
    def __init__(self, data, forTraining, isCheckDataSet):
        self.data = data
        self.forTraining = forTraining
        self.isCheckDataSet = isCheckDataSet
        self.transform = transforms.Compose\
        ([
            # выбирается случайная область изображения размером 224x224
            # Resnet умеет работать только с такими изображениями
            # изображения других размеров будут изменяться в размере
            # что может испортить определение класса "плохого качества"
            transforms.RandomResizedCrop(224),
            transforms.ToTensor(),
            # обесцвечиваем и поднимаем резкость
            transforms.Normalize(mean = [0.241, 0.691, 0.068],
                                  std = [0.229, 0.224, 0.225]),
        ])

    # Итератор. Выдаёт на каждом цикле или тензор картинки или тензор и класс
    def __getitem__(self, index):
        if self.forTraining:
            imageName, label = self.data.iloc[index]["ID_img"], self.data.iloc[index]["class"]
        elif isinstance(self.data, DataFrame):
            imageName = self.data.iloc[index]["ID_img"]
            label = None
        elif isinstance(self.data, list) and len(self.data) > 0:
            imageName = self.data[0]
            label = None
        else:
            return None

        # подготовить изображение и загрузить его в OpenCV-формате
        # noinspection PyUnresolvedReferences
        image = cv2.imread(processImage(pathCheckData if self.isCheckDataSet else pathTraining,
                                        imageName if "." in imageName else imageName + ".jpg", self.isCheckDataSet))

        # изменить порядок бит в цвете и загрузить изображение как тензор
        # noinspection PyUnresolvedReferences
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        # подготовить изображение согласно указанным правилам
        # для Resnet
        image = self.transform(image)

        # вернуть тензор изображения или тензор изображения и тензор класса (одномерный)
        if self.forTraining:
            return image, tensor(label).long()
        else:
            return image

    def __len__(self):
        return len(self.data)