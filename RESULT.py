import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PIL import Image, ImageEnhance, ImageDraw, ImageOps
from random import randint


class Window2(QMainWindow):
    def __init__(self):
        super(Window2, self).__init__()
        # второе (главное) окно
        uic.loadUi('main6.ui', self)
        self.setWindowTitle('Window2')

        # имя фотографии
        self.path = ""

        # главные кнопки
        self.w2_open.clicked.connect(self.openimage)
        self.w2_save.clicked.connect(self.saveimage)
        self.w2_reset.clicked.connect(self.resetimage)

        # фильтры

        # сепия
        self.btn_sepia.clicked.connect(self.sepia)
        # негатив
        self.btn_negative.clicked.connect(self.negative)
        # оттенки серого
        self.btn_shadesofgray.clicked.connect(self.shadesofgray)
        # черно-белый фильтр
        self.btn_blackwhite.clicked.connect(self.blackwhite)
        # шумы
        self.btn_noise.clicked.connect(self.noise)
        # небесный фильтр
        self.btn_sky.clicked.connect(self.sky)
        # сладкий персик
        self.btn_sweetpeach.clicked.connect(self.sweetpeach)
        # сумерки
        self.btn_twilight.clicked.connect(self.twilight)
        # золотой фильтр
        self.btn_gold.clicked.connect(self.gold)

        # ползунки

        # контрастность
        self.sl_contrast.valueChanged.connect(self.contrast)
        # яркость
        self.sl_brightness.valueChanged.connect(self.brightness)
        # резкость
        self.sl_sharpness.valueChanged.connect(self.sharpness)
        # контрастность
        self.sl_saturation.valueChanged.connect(self.saturation)

        # вид

        # перевертыши
        self.btn_rotate.clicked.connect(self.rotate)

        # отзеркаливание
        self.btn_mirror.clicked.connect(self.mirror)

        # уменьшение
        self.btn_shrunk.clicked.connect(self.shrunk)

    # открыть фото
    def openimage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.path = fname

        self.image.setPixmap(QPixmap(self.path))

        source = Image.open(self.path)
        source.save("image__0.png")  # сохранение фото в первоначальном виде для reset

        # сброс ползунков
        self.sl_contrast.setSliderPosition(50)
        self.sl_brightness.setSliderPosition(50)
        self.sl_sharpness.setSliderPosition(50)
        self.sl_saturation.setSliderPosition(50)

    # сохранить фото
    def saveimage(self):
        source = Image.open(self.path)

        source = Image.fromarray(source)
        source.save(self.path)

    # сбросить все изменения
    def resetimage(self):
        self.image.setPixmap(QPixmap("image__0.png"))

        source = Image.open("image__0.png")
        source.save(self.path)

        # возврат ползунков в первоначальное положение
        self.sl_contrast.setSliderPosition(50)
        self.sl_brightness.setSliderPosition(50)
        self.sl_sharpness.setSliderPosition(50)
        self.sl_saturation.setSliderPosition(50)

    # ползунок: контрастность
    def contrast(self):
        source = Image.open(self.path)

        # для процентов рядом с ползунками
        self.label_con.setText(str(
            (self.sl_contrast.value())) + "%")

        # модуль изменения контраста
        enhancer = ImageEnhance.Contrast(source)

        # значение контраста
        source = enhancer.enhance(
            float(float(self.sl_contrast.value()) / 50))

        source.save(self.path)
        del source  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))

    # ползунок: резкость
    def sharpness(self):
        source = Image.open(self.path)

        # для процентов рядом с ползунками
        self.label_sh.setText(str(
            (self.sl_sharpness.value())) + "%")

        # модуль изменения резкости
        enhancer = ImageEnhance.Sharpness(source)

        # значение резкости
        source = enhancer.enhance(
            float(float(self.sl_sharpness.value()) / 50))

        source.save(self.path)
        del source  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))

    # ползунок: насыщенность
    def saturation(self):
        source = Image.open(self.path)

        # для процентов рядом с ползунками
        self.label_sat.setText(str(
            (self.sl_saturation.value())) + "%")

        # модуль изменения баланса
        enhancer = ImageEnhance.Color(source)

        # значение баланса
        source = enhancer.enhance(
            float(float(self.sl_saturation.value()) / 60))

        source.save(self.path)
        del source  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))

    # ползунок: яркость
    def brightness(self):
        source = Image.open(self.path)

        # для процентов рядом с ползунками
        self.label_br.setText(str(
            self.sl_brightness.value()) + "%")

        # модуль контраста
        enhancer = ImageEnhance.Brightness(source)

        # значение контраста
        source = enhancer.enhance(
            float(float(self.sl_brightness.value()) / 50))

        source.save(self.path)
        del source  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))

    # фильтр: сепия
    def sepia(self):
        source = Image.open(self.path)
        draw = ImageDraw.Draw(source)

        width = source.size[0]  # ширина
        height = source.size[1]  # высота

        pix = source.load()  # пиксели

        # rgb
        for i in range(width):
            for j in range(height):
                red = pix[i, j][0]
                green = pix[i, j][1]
                blue = pix[i, j][2]
                # ср значение пикселей
                avg = (red + green + blue) // 3
                red = avg + 10 * 2
                green = avg + 10
                blue = avg
                # приведение к адекватным показателям(0 - 255)
                if red > 255:
                    red = 255
                if green > 255:
                    green = 255
                if blue > 255:
                    blue = 255
                    # прорисовывание
                draw.point((i, j), (red, green, blue))

        source.save(self.path)
        del source  # для более быстрой работы
        del draw  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))

    # фильтр: негатив
    def negative(self):
        source = Image.open(self.path)
        draw = ImageDraw.Draw(source)

        width = source.size[0]  # ширина
        height = source.size[1]  # высота

        pix = source.load()  # пиксели

        # rgb
        for i in range(width):
            for j in range(height):
                # задаем значения к каждому каналу соответсвующими
                # пикселями. Отнимаем 255, для негатива.
                red = pix[i, j][0]
                green = pix[i, j][1]
                blue = pix[i, j][2]

                draw.point((i, j), (255 - red, 255 - green, 255 - blue))

        source.save(self.path)
        del source  # для более быстрой работы
        del draw  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))

    # фильтр: черно-белый
    def blackwhite(self):
        source = Image.open(self.path)
        draw = ImageDraw.Draw(source)

        width = source.size[0]  # ширина
        height = source.size[1]  # высота

        pix = source.load()  # пиксели

        # rgb
        for i in range(width):
            for j in range(height):
                # rgb
                red = pix[i, j][0]
                green = pix[i, j][1]
                blue = pix[i, j][2]
                if (red + green + blue) > (((255 + 100) // 2) * 3):

                    draw.point((i, j), (255, 255, 255))
                else:
                    draw.point((i, j), (0, 0, 0))

        source.save(self.path)
        del source  # для более быстрой работы
        del draw  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))

    # фильтр: оттенки серого
    def shadesofgray(self):
        source = Image.open(self.path)
        enhancer = ImageEnhance.Color(source)
        source = enhancer.enhance(0.0)

        source.save(self.path)
        del source  # для более быстрой работы
        self.image.setPixmap(QPixmap(self.path))

    # фильтр: шумы
    def noise(self):
        source = Image.open(self.path)
        draw = ImageDraw.Draw(source)

        width = source.size[0]  # ширина
        height = source.size[1]  # высота

        pix = source.load()  # пиксели

        factor = 70

        # rgb
        for i in range(width):
            for j in range(height):
                rand = randint(-factor, factor)
                red = pix[i, j][0] + rand
                green = pix[i, j][1] + rand
                blue = pix[i, j][2] + rand

                if red > 255:
                    red = 255
                if green > 255:
                    green = 255
                if blue > 255:
                    blue = 255
                if red < 0:
                    red = 0
                if green < 0:
                    green = 0
                if blue < 0:
                    blue = 0

                draw.point((i, j), (red, green, blue))

        source.save(self.path)
        del source  # для более быстрой работы
        del draw  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))

    # фильтр: небесный
    def sky(self):
        source = Image.open(self.path)
        draw = ImageDraw.Draw(source)

        width = source.size[0]  # ширина
        height = source.size[1]  # высота

        pix = source.load()  # пиксели

        # rgb
        for i in range(width):
            for j in range(height):
                red = pix[i, j][0] + 15
                green = pix[i, j][1] + 40
                blue = pix[i, j][2] + 70

                if red > 255:
                    red = 255
                if green > 255:
                    green = 255
                if blue > 255:
                    blue = 255
                if red < 0:
                    red = 0
                if green < 0:
                    green = 0
                if blue < 0:
                    blue = 0

                draw.point((i, j), (red, green, blue))

        source.save(self.path)
        del source  # для более быстрой работы
        del draw  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))

    # фильтр: сладкий персик
    def sweetpeach(self):
        source = Image.open(self.path)
        draw = ImageDraw.Draw(source)

        width = source.size[0]  # ширина
        height = source.size[1]  # высота

        pix = source.load()  # пиксели

        # rgb
        for i in range(width):
            for j in range(height):
                red = pix[i, j][0] + 30
                green = pix[i, j][1] + 10
                blue = pix[i, j][2] + 10

                draw.point((i, j), (red, green, blue))

        source.save(self.path)
        del source  # для более быстрой работы
        del draw  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))

    # фильтр: сумерки
    def twilight(self):
        source = Image.open(self.path)
        draw = ImageDraw.Draw(source)

        width = source.size[0]  # ширина
        height = source.size[1]  # высота

        pix = source.load()  # пиксели

        # rgb
        for i in range(width):
            for j in range(height):
                red = pix[i, j][0] - 20
                green = pix[i, j][1] - 40
                blue = pix[i, j][2] + 10

                draw.point((i, j), (red, green, blue))

        source.save(self.path)
        del source  # для более быстрой работы
        del draw  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))

    # фильтр: золото
    def gold(self):
        source = Image.open(self.path)
        draw = ImageDraw.Draw(source)

        width = source.size[0]  # ширина
        height = source.size[1]  # высота

        pix = source.load()  # пиксели

        # rgb
        for i in range(width):
            for j in range(height):
                red = pix[i, j][0]
                green = pix[i, j][1]
                blue = pix[i, j][2]

                avg = (red + green + blue) // 2
                red = avg + 20 * 2
                green = avg + 25
                blue = avg

                if red > 255:
                    red = 255
                if green > 255:
                    green = 255
                if blue > 255:
                    blue = 255

                draw.point((i, j), (red, green, blue))

        source.save(self.path)
        del source  # для более быстрой работы
        del draw  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))

    # вид: поворот
    def rotate(self):
        source = Image.open(self.path)

        angle = 90
        source = source.rotate(angle)

        source.save(self.path)
        del source  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))

    # вид: отзеркаливание
    def mirror(self):
        source = Image.open(self.path)
        source = ImageOps.mirror(source)

        source.save(self.path)
        del source  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))

    # вид: уменьшение
    def shrunk(self):
        source = Image.open(self.path)

        source = ImageOps.expand(source, border=100, fill='black')

        source.save(self.path)
        del source  # для более быстрой работы

        self.image.setPixmap(QPixmap(self.path))


# открытие второе окно
class Window1(QMainWindow):
    def __init__(self):
        super().__init__()

        # первое (приветственное) окно
        uic.loadUi('main5.ui', self)
        self.setWindowTitle('Window1')

        # кнопка для старта работы редактора
        self.w1_start.clicked.connect(self.show_window_2)

    # открытие первого окна
    def show_window_1(self):
        self.w1 = Window1()
        self.w1.button.clicked.connect(self.show_window_2)
        self.w1.button.clicked.connect(self.w1.close)
        self.w1.show()

    # открытие второго окна
    def show_window_2(self):
        self.w2 = Window2()
        self.w2.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window1()
    w.show()
    sys.exit(app.exec_())
