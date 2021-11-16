import sys
import matplotlib.pyplot as plt
from math import sin, cos, tan, pi, factorial
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit


class Frac:

    def __init__(self, num=0, dem=1):

        # разделяем обыкновенную дробь на числитель и знаменатель

        if dem == 0:
            raise ValueError("Знаменатель не может быть равен 0")
        if num % dem == 0:
            self.n = int(num / dem)
            self.d = 1
        else:
            self.n = num
            self.d = dem

    def __str__(self):

        # "склеивем" числитель и знаменатель
        c = ''
        if self.n < 0:
            c = '- '
        if self.d == 1:
            return c + str(abs(self.n))
        else:
            return c + (f'{abs(self.n)}/{self.d}')

    def Reduce(self):

        # сокращаем обыкновенную дробь, если это возможно

        n = min(abs(self.n), abs(self.d))
        if self.n == 0:
            return Frac(0)
        while n > 0:
            if abs(self.n) % n == 0 and abs(self.d) % n == 0:
                return Frac(int(self.n / n), int(self.d / n))
            else:
                n -= 1

    # стандартные операции с обыкновенными дробями

    def __add__(self, other):
        new_n = self.n * other.d + self.d * other.n
        new_d = self.d * other.d
        return Frac(new_n, new_d).Reduce()

    def __mul__(self, other):
        new_n = self.n * other.n
        new_d = self.d * other.d
        return Frac(new_n, new_d).Reduce()

    def __sub__(self, other):
        new_n = self.n * other.d - self.d * other.n
        new_d = self.d * other.d
        return Frac(new_n, new_d).Reduce()

    def __truediv__(self, other):
        new_n = self.n * other.d
        new_d = self.d * other.n
        return Frac(new_n, new_d).Reduce()

    def __pow__(self, p):
        new_n = self.n ** p
        new_d = self.d ** p
        return Frac(new_n, new_d).Reduce()


class str_frac(Frac):

    # создаем конвертер десятичных и смешанных дробей в обыкновенные

    def __init__(self, text):
        c = 1
        if '/' in text and '_' not in text:
            n, d = text.split('/')
            if '-' in n and ' ' not in n:
                n = '- ' + n[1:]
            if '-' in n:
                s, n = n.split(' ')
                n = int(n) * (-1)
            super().__init__(int(n), int(d))
        elif '/' in text and '_' in text:
            c_n, n_d = text.split('_')[0], text.split('_')[1]
            n, d = n_d.split('/')
            n = int(n)
            if '-' in c_n and ' ' not in c_n:
                c_n = '- ' + c_n[1:]
            if '-' in c_n:
                c = -1
                s, c_n = c_n.split(' ')
            n += int(c_n) * int(d)
            super().__init__(n * c, int(d))
        elif ',' in text:
            c_n, n_d = text.split(',')
            if '-' in c_n and ' ' not in c_n:
                c_n = '- ' + c_n[1:]
            c = 1
            if '-' in c_n:
                c = -1
                s, c_n = c_n.split(' ')
            c_n = int(c_n)
            n = int(n_d)
            d = 10 ** len(n_d)
            n += c_n * d
            super().__init__(n * c, d)
        else:
            if '-' in text and ' ' not in text:
                text = '- ' + text[1:]
            if '-' in text:
                s, text = text.split(' ')
                text = int(text) * (-1)
            super().__init__(int(text))

    def f_sin(self):
        c = ''
        a = sin(self.num())
        if a < 0:
            c = ' '
        a = str(round(a, 2))
        a = a.replace('.', ',')
        bb = str_frac(c + a).Reduce()
        return bb

    def f_cos(self):
        a = int(self.n) / int(self.d)
        a = cos(a)
        a = str(round(a, 2))
        a = a.replace('.', ',')
        return str_frac(a).Reduce()

    def f_tan(self):
        a = int(self.n) / int(self.d)
        a = tan(a)
        a = str(round(a, 2))
        a = a.replace('.', ',')
        return str_frac(a).Reduce()

    def f_ctg(self):
        a = int(self.n) / int(self.d)
        a = 1 / tan(a)
        a = str(round(a, 2))
        a = a.replace('.', ',')
        return str_frac(a).Reduce()

    def f_convert(self):
        a = f'{self.d}/{self.n}'
        return str_frac(str(a)).Reduce()

    def f_fact(self):
        aa = int(self.n) % int(self.d)
        a = int(self.n) / int(self.d)
        if aa != 0 or a < 0 or '-' in a:
            return 'Аргумент должен быть натуральным числом'
        else:
            a = factorial(int(a))
            return a

    def f_sqrt(self):
        a = int(self.n) / int(self.d)
        if a < 0:
            a = f'sqrt({-1 * a}) * i'
            return a
        else:
            a = str(round(float(a) ** (1 / 2), 2)).replace('.', ',')
            return str_frac(a).Reduce()

    def num(self):
        return float(self.n / self.d)


class F(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.calc = ''

    def initUI(self):

        # визуализируем калькулятор

        self.setGeometry(500, 150, 400, 520)
        self.setWindowTitle('Калькулятор')
        self.tx = QLineEdit(self)
        self.tx.resize(387, 80)
        self.tx.move(6, 10)
        self.btn = QPushButton('--graphics--', self)
        self.btn.resize(190, 36)
        self.btn.move(6, 395)
        self.btn.clicked.connect(self.Graph)
        self.btn = QPushButton('Set parameters', self)
        self.btn.resize(190, 36)
        self.btn.move(202, 395)
        self.btn.clicked.connect(self.set_p)
        self.btn = QPushButton('y = ax + b', self)
        self.btn.resize(190, 36)
        self.btn.move(6, 436)
        self.btn.clicked.connect(self.linear)
        self.btn = QPushButton('Построить прямую', self)
        self.btn.resize(190, 36)
        self.btn.move(202, 436)
        self.btn.clicked.connect(self.set_linear)
        self.btn = QPushButton('y = ax^2 + bx + c', self)
        self.btn.resize(190, 36)
        self.btn.move(6, 477)
        self.btn.clicked.connect(self.par)
        self.btn = QPushButton('Построить параболу', self)
        self.btn.resize(190, 36)
        self.btn.move(202, 477)
        self.btn.clicked.connect(self.set_par)
        self.btn = QPushButton('1', self)
        self.btn.resize(70, 70)
        self.btn.move(5, 100)
        self.btn.clicked.connect(self.one)
        self.btn = QPushButton('2', self)
        self.btn.resize(70, 70)
        self.btn.move(78, 100)
        self.btn.clicked.connect(self.two)
        self.btn = QPushButton('3', self)
        self.btn.resize(70, 70)
        self.btn.move(151, 100)
        self.btn.clicked.connect(self.tree)
        self.btn = QPushButton('4', self)
        self.btn.resize(70, 70)
        self.btn.move(5, 173)
        self.btn.clicked.connect(self.four)
        self.btn = QPushButton('7', self)
        self.btn.resize(70, 70)
        self.btn.move(5, 246)
        self.btn.clicked.connect(self.seven)
        self.btn = QPushButton('C', self)
        self.btn.resize(70, 70)
        self.btn.move(5, 319)
        self.btn.clicked.connect(self.C)
        self.btn = QPushButton('5', self)
        self.btn.resize(70, 70)
        self.btn.move(78, 173)
        self.btn.clicked.connect(self.five)
        self.btn = QPushButton('6', self)
        self.btn.resize(70, 70)
        self.btn.move(151, 173)
        self.btn.clicked.connect(self.six)
        self.btn = QPushButton('8', self)
        self.btn.resize(70, 70)
        self.btn.move(78, 246)
        self.btn.clicked.connect(self.eight)
        self.btn = QPushButton('9', self)
        self.btn.resize(70, 70)
        self.btn.move(151, 246)
        self.btn.clicked.connect(self.nine)
        self.btn = QPushButton('+', self)
        self.btn.resize(50, 51)
        self.btn.move(224, 208)
        self.btn.clicked.connect(self.plus)
        self.btn = QPushButton('-', self)
        self.btn.resize(50, 51)
        self.btn.move(224, 154)
        self.btn.clicked.connect(self.minus)
        self.btn = QPushButton(':', self)
        self.btn.resize(50, 51)
        self.btn.move(224, 100)
        self.btn.clicked.connect(self.div)
        self.btn = QPushButton('*', self)
        self.btn.resize(50, 54)
        self.btn.move(224, 262)
        self.btn.clicked.connect(self.mul)
        self.btn = QPushButton('tg', self)
        self.btn.resize(70, 54)
        self.btn.move(277, 262)
        self.btn.clicked.connect(self.tg)
        self.btn = QPushButton('sin', self)
        self.btn.resize(70, 51)
        self.btn.move(277, 100)
        self.btn.clicked.connect(self.sinn)
        self.btn = QPushButton('ctg', self)
        self.btn.resize(70, 51)
        self.btn.move(277, 208)
        self.btn.clicked.connect(self.ctg)
        self.btn = QPushButton('cos', self)
        self.btn.resize(70, 51)
        self.btn.move(277, 154)
        self.btn.clicked.connect(self.cos)
        self.btn = QPushButton('pi', self)
        self.btn.resize(70, 70)
        self.btn.move(277, 319)
        self.btn.clicked.connect(self.pi)
        self.btn = QPushButton('^', self)
        self.btn.resize(45, 51)
        self.btn.move(350, 100)
        self.btn.clicked.connect(self.dig)
        self.btn = QPushButton('sqrt', self)
        self.btn.resize(45, 51)
        self.btn.move(350, 154)
        self.btn.clicked.connect(self.sqrt)
        self.btn = QPushButton('_', self)
        self.btn.resize(45, 51)
        self.btn.move(350, 208)
        self.btn.clicked.connect(self.l_br)
        self.btn = QPushButton('1/x', self)
        self.btn.resize(45, 54)
        self.btn.move(350, 262)
        self.btn.clicked.connect(self.convert)
        self.btn = QPushButton('0', self)
        self.btn.resize(70, 70)
        self.btn.move(78, 319)
        self.btn.clicked.connect(self.zero)
        self.btn = QPushButton(',', self)
        self.btn.resize(45, 33)
        self.btn.move(350, 319)
        self.btn.clicked.connect(self.com)
        self.btn = QPushButton('/', self)
        self.btn.resize(45, 33)
        self.btn.move(350, 356)
        self.btn.clicked.connect(self.slesh)
        self.btn = QPushButton('=', self)
        self.btn.resize(70, 70)
        self.btn.move(151, 319)
        self.btn.clicked.connect(self.eq)
        self.btn = QPushButton('x!', self)
        self.btn.resize(50, 70)
        self.btn.move(224, 319)
        self.btn.clicked.connect(self.fact)

    # прописываем работу кнопок

    def one(self):
        self.calc += '1'
        self.tx.setText(self.calc)

    def two(self):
        self.calc += '2'
        self.tx.setText(self.calc)

    def tree(self):
        self.calc += '3'
        self.tx.setText(self.calc)

    def four(self):
        self.calc += '4'
        self.tx.setText(self.calc)

    def five(self):
        self.calc += '5'
        self.tx.setText(self.calc)

    def six(self):
        self.calc += '6'
        self.tx.setText(self.calc)

    def seven(self):
        self.calc += '7'
        self.tx.setText(self.calc)

    def eight(self):
        self.calc += '8'
        self.tx.setText(self.calc)

    def nine(self):
        self.calc += '9'
        self.tx.setText(self.calc)

    def zero(self):
        self.calc += '0'
        self.tx.setText(self.calc)

    def plus(self):
        self.calc += ' + '
        self.tx.setText(self.calc)

    def minus(self):
        self.calc += ' - '
        self.tx.setText(self.calc)

    def div(self):
        self.calc += ' : '
        self.tx.setText(self.calc)

    def mul(self):
        self.calc += ' * '
        self.tx.setText(self.calc)

    def sqrt(self):
        a = self.calc
        if a == '':
            self.calc = 'No argument for "sqrt"'
            self.tx.setText(self.calc)
            self.calc = ''
        else:
            s = str_frac(str(a))
            s = s.f_sqrt()
            self.calc = str(s)
            self.tx.setText(self.calc)
            self.calc = ''

    def fact(self):
        a = self.calc
        if a == '':
            self.calc = 'No argument for "factorial"'
            self.tx.setText(self.calc)
            self.calc = ''
        elif '-' in a:
            self.calc = 'Аргемент должен быть натуральным числом'
            self.tx.setText(self.calc)
            self.calc = ''
        else:
            s = str_frac(str(a))
            s = s.f_fact()
            self.calc = str(s)
            self.tx.setText(self.calc)

    def dig(self):
        self.calc += ' ^ '
        self.tx.setText(self.calc)

    def cos(self):
        a = self.calc
        if a == '':
            self.calc = 'No argument for "cos"'
            self.tx.setText(self.calc)
            self.calc = ''
        else:
            s = str_frac(str(a))
            s = s.f_cos()
            self.calc = str(s)
            self.tx.setText(self.calc)

    def sinn(self):
        a = self.calc
        if a == '':
            self.calc = 'No argument for "sin"'
            self.tx.setText(self.calc)
            self.calc = ''
        else:
            s = str_frac(a)
            s = s.f_sin()
            self.calc = str(s)
            self.tx.setText(self.calc)

    def tg(self):
        a = self.calc
        if a == '':
            self.calc = 'No argument for "tg"'
            self.tx.setText(self.calc)
            self.calc = ''
        else:
            s = str_frac(str(a))
            s = s.f_tan()
            self.calc = str(s)
            self.tx.setText(self.calc)

    def ctg(self):
        a = self.calc
        if a == '':
            self.calc = 'No argument for "ctg"'
            self.tx.setText(self.calc)
            self.calc = ''
        else:
            s = str_frac(str(a))
            s = s.f_ctg()
            self.calc = str(s)
            self.tx.setText(self.calc)

    def pi(self):
        self.calc += 'pi'
        self.tx.setText(self.calc)

    def slesh(self):
        self.calc += '/'
        self.tx.setText(self.calc)

    def l_br(self):
        self.calc += '_'
        self.tx.setText(self.calc)

    def convert(self):
        a = self.calc
        if a == '' or a == '0':
            self.calc = 'No argument to convert'
            self.tx.setText(self.calc)
            self.calc = ''
        else:
            s = str_frac(str(a))
            s = s.f_convert()
            self.calc = str(s)
            self.tx.setText(self.calc)

    def com(self):
        self.calc += ','
        self.tx.setText(self.calc)

    def C(self):
        self.calc = ''
        self.tx.setText(self.calc)

    def Graph(self):
        self.calc = 'начало__конец__число точек: '
        self.tx.setText(self.calc)

    low = high = n = d = 0

    def set_p(self):
        global low, high, n, d
        if 'начало__конец__число точек: ' in self.calc:
            string, p = self.calc.split(': ')
            low, high, n = p.split('__')
            low = str_frac(low.lstrip()).num()
            high = str_frac(high.lstrip()).num()
            n = int(n)
            d = (high - low) / n
            self.calc = 'выберите график'
            self.tx.setText(self.calc)
        else:
            self.calc = 'Неправильная очередность действий'
            self.tx.setText(self.calc)
            self.calc = ''

    def linear(self):
        if self.calc == 'выберите график' or 'a__b' in self.calc:
            self.calc = 'a__b: '
            self.tx.setText(self.calc)
        else:
            self.calc = 'Неправильная очередность действий'
            self.tx.setText(self.calc)
            self.calc = ''

    def set_linear(self):
        x = []
        y = []
        if 'a__b' in self.calc:
            string, p = self.calc.split(': ')
            a, b = p.split('__')
            a = str_frac(a.lstrip()).num()
            b = str_frac(b.lstrip()).num()
            for i in range(n):
                xx = low + i * d
                yy = a * xx + b
                x.append(xx)
                y.append(yy)
            plt.plot(x, y)
            plt.show()
        else:
            self.calc = 'Неправильная очередность действий'
            self.tx.setText(self.calc)
            self.calc = ''

    def par(self):
        if self.calc == 'выберите график' or 'a__b' in self.calc:
            self.calc = 'a__b__c: '
            self.tx.setText(self.calc)
        else:
            self.calc = 'Неправильная очередность действий'
            self.tx.setText(self.calc)
            self.calc = ''

    def set_par(self):
        x = []
        y = []
        if 'a__b__c' in self.calc:
            string, p = self.calc.split(': ')
            a, b, c = p.split('__')
            a = str_frac(a.lstrip()).num()
            b = str_frac(b.lstrip()).num()
            c = str_frac(c.lstrip()).num()
            for i in range(n):
                xx = low + i * d
                yy = a * (xx ** 2) + b * xx + c
                x.append(xx)
                y.append(yy)
            plt.plot(x, y)
            plt.show()
        else:
            self.calc = 'Неправильная очередность действий'
            self.tx.setText(self.calc)
            self.calc = ''

    def eq(self):
        ss = str(self.calc)
        sp = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        c = ''
        n = 1
        for i in sp:
            if i in ss:
                n = 1
                break
            else:
                n = 0
        if n == 0 and ss != 'pi':
            a = 'Error'
        else:
            if ss[1] == '-':
                ss = ss[3:]
                c = '- '
            if ' + ' in ss:
                a, b = (ss).split(" + ")
                a = a.replace('pi', '3,141')
                b = b.replace('pi', '3,141')
                a = str_frac(c + a)
                b = str_frac(b)
                a += b
            elif ' * ' in ss:
                a, b = (ss).split(" * ")
                if a == 'pi':
                    a = '3,141'
                if b == 'pi':
                    b = '3,141'
                a = str_frac(c + a)
                b = str_frac(b)
                a *= b
            elif ' - ' in ss:
                a, b = (ss).split(" - ")
                if a == 'pi':
                    a = '3,141'
                if b == 'pi':
                    b = '3,141'
                a = str_frac(c + a)
                b = str_frac(b)
                a -= b
            elif ' : ' in ss:
                a, b = (ss).split(" : ")
                if b != '0':
                    if a == 'pi':
                        a = '3,141'
                    if b == 'pi':
                        b = '3,141'
                    a = str_frac(c + a)
                    b = str_frac(b)
                    a /= b
                else:
                    a = "Нельзя делить на 0"
            elif '^' in ss:
                a, b = (ss).split(" ^ ")
                if a == 'pi':
                    a = '3,141'
                if b == 'pi':
                    b = '3,141'
                a = str_frac(c + a)
                b = int(b)
                a = a ** b
            elif ss == 'pi':
                a = '3,141'
            else:
                a = 'Error'
            if a == 'None':
                a = '0'
        self.calc = str(a)
        self.tx.setText(self.calc)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = F()
    ex.show()
    sys.exit(app.exec())
