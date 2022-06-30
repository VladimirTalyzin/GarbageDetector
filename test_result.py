from numpy import array, unique, argmax
from csv import writer

from pandas import read_csv
from tqdm import tqdm

from model import Model
from dataset import ImageDataset
from config import checkFilename, resultFilename, modelFilename, uncertainFilename
from utility import prepareDataset

if __name__ == '__main__':

    # вызываем обученную модель для GPU
    model = Model(loadModelFromFile = modelFilename, cpuMode = False)

    # считываем список картинок для предсказания, уже указанный там класс отбрасываем
    checkData = read_csv(checkFilename).drop(["class"], axis = 1)

    checkDataset = ImageDataset(data = checkData, forTraining = False, isCheckDataSet = True)

    certaintyImages = {}
    certainty = {}
    imageList = []

    preparedDataset = prepareDataset(checkDataset, False, specifiedBatchSize = 8)

    for stage in range(25):
        classes = {}
        counter = 0
        # разбор картинок
        progressBar = tqdm(preparedDataset)
        for images in progressBar:
            images = images.cuda()
            prediction = model.prediction(images)

            predictions = prediction.cpu().detach().numpy()

            # из полученных данных предсказаний вероятности классов,
            # выбираем класс с самым большим весом и считаем метрику "уверенности" предсказания
            for classItem in predictions:
                average = array(classItem).mean()
                classIndex, classPower = max(enumerate(classItem), key = lambda item: item[1])

                imageName = checkData["ID_img"][counter]
                if stage == 0:
                    imageList.append(imageName)

                if not imageName in certainty:
                    certainty[imageName] = {}

                if not classIndex in certainty[imageName]:
                    certainty[imageName][classIndex] = []
                certainty[imageName][classIndex].append(round(classPower - average, 2))

                if not imageName in certaintyImages:
                    certaintyImages[imageName] = []

                certaintyImages[imageName].append(classIndex)

                # суммируем количество классов на данном этапе. Как дополнительная информация.
                classes[classIndex] = classes[classIndex] + 1 if classIndex in classes else 1
                counter += 1

            progressBar.set_postfix_str("Found classes: " + ', '.join(str(classCounter) for classCounter in classes.values()) + " of " + str(len(imageList)))

    # получаем классы для каждой картинки
    resultImages = {}
    for imageName in imageList:
        # классы и частота их предсказания
        classIndexes, counts = unique(array(certaintyImages[imageName]), return_counts=True)
        # выбираем самый часто встретившийся класс
        classIndex = classIndexes[argmax(counts)]
        resultImages[imageName] = classIndex

    # получаем самую лучшую степень уверенности по всем картинкам для их выбранного ранее класса
    resultCertainty = {}
    for imageName in imageList:
        classIndex = resultImages[imageName]
        resultCertainty[round(array(certainty[imageName][classIndex]).max(), 2)] = [imageName, classIndex]


    # выводим результаты предсказаний в файл, пригодный для загрузки на leaderboard
    with open(resultFilename, "w", encoding = "utf8", newline = "") as csvFile:
        csvWriter = writer(csvFile, delimiter = ",")
        csvWriter.writerow(["ID_img", "class"])
        for imageName in imageList:
            csvWriter.writerow([imageName, resultImages[imageName]])

    # выводим результаты уверенности предсказаний, с сортировкой от
    # самого неуверенного предсказания к самому уверенному
    with open(uncertainFilename, "w", encoding = "utf8", newline = "") as csvFile:
        csvWriter = writer(csvFile, delimiter = ",")
        csvWriter.writerow(["image", "uncertain", "maybe class"])
        for uncertainValue, data in dict(sorted(resultCertainty.items())).items():
            csvWriter.writerow([data[0], data[1], uncertainValue])
