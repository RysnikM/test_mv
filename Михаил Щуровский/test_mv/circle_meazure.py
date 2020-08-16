import cv2
import numpy as np

file = 'image_1.jpg'
# читаем файл
img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
# конвертируем в оттенки серого
img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# устанавливаем пороговое значение по цвету
# для преобразования в двоичное изображение
thresh = 100
# получаем бинарное изображение
ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
# ищем контуры объектов на изображении
contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# создаем контейнер для полученных контуров всех объектов
img_contours = np.zeros(img.shape)
# гасим все объекты кроме лазерной отметки на трубе
image = cv2.drawContours(img_contours, contours[1], -1, (255, 255, 255), 3)
# сохраняем контуры в новый файл что бы не изменять исходник
cv2.imwrite('contours.jpg', img_contours)
# читаем файл contours для подготовки к измерениям
arc_image = cv2.imread('contours.jpg')
# конвертируем в серый
arc_image = cv2.cvtColor(arc_image, cv2.COLOR_BGR2GRAY)
# конвертируем в двоичный формат
ret2, arc_image = cv2.threshold(arc_image, 21, 255, cv2.THRESH_BINARY)
# измеряем лазерный маркер на трубе
x, y, width, height = cv2.boundingRect(arc_image)
# радиус
diametr = int(height * 0.2636)
rad = int((height/2) * 0.2636)
# считаем длину окружности 2пR
len_circle_px = int(2 * 3.14 * (height / 2))
# пиксели в милиметры 1px = 0.2636 mm
len_circle_mm = int(len_circle_px * 0.2636)
# кладем данные в словарь
D = {'имя файла': file,'диаметр окружности(мм)': diametr,
     'радиус окружности(мм)': rad,
     'длина окружности (мм)': len_circle_mm}
# выводим результат
print(D)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()