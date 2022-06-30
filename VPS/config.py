# последний обработанный тренировочный файл
trainFilename = "train_manual_0.96.csv" #"new_train.csv" #"train_manual_0.91.csv"
# файл со списком названий файлов для распознавания классов
checkFilename = "sample_solution.csv"


# Файл с результатами для загрузки на leaderboard
resultFilename = "result.csv"
# Файл с результатами уверенности определения
uncertainFilename = "uncertain.csv"

# Файл сохранения и загрузки модели
# modelFilename = "trained_model.zip"
# Файл модели для CPU
modelFilename = "trained_model_cpu.zip"

# папка с файлами для обучения
pathTraining  = "train/"
# папка с файлами для определения класса
pathCheckData = "check/"

# папка с кэшируемыми обработанными изображениями для обучения
pathPreparedTraining  = "prepared_training_images/"
# папка с кэшируемыми обработанными изображениями для определения класса
pathPreparedCheck = "prepared_check_images/"
# папка с кэшируемыми пользовательскими изображениями
pathPreparedUser = "prepared_users_images/"
# папка с результатами проверок пользовательских изображений
pathUserResults = "users_results/"

# файл, выбранный как эталон яркости. Яркость остальных файлов будет подстроена под этот
# normalBrightnessFile = "train/220301123646_56e2844ea32dc657c742a803a8b3035e.jpg"
# файл-эталон яркости для работы на VPS
normalBrightnessFile = "/var/www/morfo/data/www/0v.ru/garbage/normal_brightness.jpg"