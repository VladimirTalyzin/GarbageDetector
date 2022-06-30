from torch import no_grad
from tqdm import tqdm

def train(model, criterion, optimizer, trainData, checkData, epochsCount):

    # подготавливаем красивый ProgressBar для аккуратного вывода информации в консоли
    progressBar = tqdm(range(epochsCount))
    for _ in progressBar:

        model.getModelForTraining().train()
        trainLoss = 0
        trainSize = 0

        trainPrediction = 0

        for images, labels in trainData:
            # освободить текущие градиенты модели из памяти
            optimizer.zero_grad()

            # в зависимости от режима работы
            # переводим тензоры в режим, пригодный для работы на имеющемся оборудовании
            if model.cpuMode:
                images = images.cpu()
                labels = labels.cpu()
            else:
                images = images.cuda()
                labels = labels.cuda()

            trainingDataset = model.getModelForTraining()(images)

            # считаем энтропию полученных результатов и тех, что
            # выдало предсказание
            loss = criterion(trainingDataset, labels)
            # сбросить градиенты этого расчёта энтропии,
            # чтобы не накапливать их на каждом этапе
            loss.backward()

            # суммируем энтропию обучающей выборки для эпохи
            trainLoss += loss.item()
            # считаем размер обучающей выборки для эпохи
            trainSize += trainingDataset.size(0)

            # подсчитываем, сколько классов с максимальным значением предсказания
            # совпало с заданным классом в обучающей выборке
            # это будет метрика "аккуратности предсказания"
            # тут считается количество совпадений, а в loss считался уровень энтропии
            # noinspection PyUnresolvedReferences
            trainPrediction += (trainingDataset.argmax(1) == labels).sum()

            # выполнить следующий шаг оптимизации
            # в данном решении это делает алгоритм Adam(0.001)
            optimizer.step()


        checksLoss = 0
        checksSize = 0

        checksPrediction = 0

        # обновить веса модели, согласно данным последней тренировки
        model.getModelForTraining().eval()

        # отключить режим тренировки и перевести модель в режим предсказания
        with no_grad():
            for images, labels in checkData:

                # в зависимости от режима работы
                # переводим тензоры в режим, пригодный для работы на имеющемся оборудовании
                if model.cpuMode:
                    images = images.cpu()
                    labels = labels.cpu()
                else:
                    images = images.cuda()
                    labels = labels.cuda()

                # получаем от модели предсказания классов
                checkDataset = model.getModelForTraining()(images)

                # считаем энтропию полученных результатов и тех, что
                # выдало предсказание
                loss = criterion(checkDataset, labels)

                # суммируем энтропию обучающей выборки для эпохи
                checksLoss += loss.item()
                # считаем размер обучающей выборки для эпохи
                checksSize += checkDataset.size(0)

                # подсчитываем, сколько классов с максимальным значением предсказания
                # совпало с заданным классом в обучающей выборке
                # это будет метрика "аккуратности предсказания"
                # тут считается количество совпадений, а в loss считался уровень энтропии
                # noinspection PyUnresolvedReferences
                checksPrediction += (checkDataset.argmax(1) == labels).sum()


        # Выводим полученные для эпохи параметры обучения в ProgressBar
        # аккуратность ниже 85 означает, что модель обучилась плохо
        # аккуратность выше 90 означает переобучение
        # оптимально - около 88
        # noinspection PyUnresolvedReferences
        progressBar.set_postfix_str("Train loss: " + format((trainLoss / trainSize) * 100, '.2f') +
                                    " check loss: " + format((checksLoss / checksSize) * 100, '.2f') +
                                    " train accuracy: " + format(((trainPrediction / trainSize) * 100).item(), '.1f') +
                                    " check accuracy: " + format(((checksPrediction / checksSize) * 100).item(), '.1f'))