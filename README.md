# GarbageDetector

test_train.py - запустить обучение и сохранить модель
test_result.py - запустить распознавание по сохранённой модели
test_file.py - запустить распознавание файла, указанного в командной строке. Пример:

```
cd /var/www/morfo/data/www/0v.ru/garbage/
python test_file.py test_image_class1.jpg
```

classify.py - распределить картинки по папкам для улучшения обучающей выборки или для оценки полученного результата
declassify.py - собрать данные по картинкам из папок и записать их классы в csv-файл


Для решения задачи необходимо создать папки:

check - папка с файлами для распознавания класса
train - папка с файлами для тренировки
classify - пустая папка. Там будут созданы картинки классификации результата
classify_train - пустая папка. Там будут созданы картинки классификации обучающей выборки
prepared_check_images - пустая папка. Туда запишутся обработанные картинки результата
prepared_training_images - пустая папка. Туда запишутся обработанные картинки обучающей выборки

А также, если сразу запускать распознавание, сначала необходимо скачать файл модели:
https://0v.ru/garbage/trained_model.zip

Зависимости для тренировки моделей:

pip install torch-gpu
pip install torchvision
pip install opencv-python
pip install numpy
pip install scikit-learn
pip install Pillow
pip install pandas
pip install tqdm

# Установка на VPS

Необходимо установить на VPS содержимое папки "VPS". 
Туда же скачать файл модели: https://0v.ru/garbage/trained_model_cpu.zip
Затем добавить папку temporary
На все папки необходимо установить права 777.


Пример работы сайта, размещённого на VPS: https://0v.ru/garbage/
Работает на любых платформах. Desktop, Android, iOS

![Запуск сайта](https://0v.ru/garbage/screen-start.png)
![Помойка найдена](https://0v.ru/garbage/screen-1.png)
![Плохое качество](https://0v.ru/garbage/screen-2.png)

Зависимости для запуска на VPS:

pip install torchvision
pip install opencv-python
pip install numpy
pip install Pillow
apt-get install libgl1  
