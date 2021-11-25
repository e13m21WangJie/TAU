import matplotlib.pyplot as pyplot
import control.matlab as matlab
import colorama as color
import numpy
import math

def choice():
    inertialess = 'Безынерционное звено'
    aperiodic = 'Апериодическое звено'
    intergration = 'Интегрирующее звено'
    ideal_differential = 'Идеальное дифференцирующее звено'
    real_differential = 'Реальное дифференцирующее звено'

    needNewChoice = True
    while needNewChoice:
        print(color.Style.RESET_ALL)
        userInput = input(color.Fore.CYAN + 'Введите номер команды:\n'
                          '1 - ' + inertialess + ';\n'
                          '2 - ' + aperiodic + ';\n'
                          '3 - ' + intergration + ';\n'
                          '4 - ' + ideal_differential + ';\n'
                          '5 - ' + real_differential + '.\n'
                          )
        if userInput.isdigit():
            needNewChoice = False
            userInput = int(userInput)
            if userInput == 1:
                name = 'Безынерционное звено'
            elif userInput == 2:
                name = 'Апериодическое звено'
            elif userInput == 3:
                name = 'Интегрирующее звено'
            elif userInput == 4:
                name = 'Идеальное дифференцирующее звено'
            elif userInput == 5:
                name = 'Реальное дифференцирующее звено'
            else:
                print(color.Fore.RED + '\nНедопустимое значение')
        else:
            print(color.Fore.RED + '\nВведите числовое значение!')
            needNewChoice = True
    return name

def getUnit(name):
    needNewChoice = True
    while needNewChoice:
        needNewChoice = False
        k = input(color.Fore.CYAN + 'Введите коэффициент k:')
        t = input(color.Fore.CYAN + 'Введите коэффициент t:')
        if k.isdigit() and t.isdigit():
            k = int(k)
            t = int(t)
            if name == 'Безынерционное звено':
                unit = matlab.tf([k], [1])
                continue
            elif name == 'Апериодическое звено':
                unit = matlab.tf([k], [t, 1])
                continue
            elif name == 'Интегрирующее звено':
                unit = matlab.tf([1], [t, 0])
                continue
            elif name == 'Идеальное дифференцирующее звено':
                unit = matlab.tf([k, 0], [1])
                continue
            elif name == 'Реальное дифференцирующее звено':
                unit = matlab.tf([k, 0], [t, 1])
        else:
            print('Введите числовое значение!')
    return unit, k, t

def graph(num, title, y, x):
    pyplot.subplot(2, 2, num)
    pyplot.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.4, hspace=0.5)
    pyplot.grid(True)
    if title == 'Переходная характеристика':
        pyplot.plot(x, y, 'blue')
        pyplot.ylabel('Амплитуда')
        pyplot.xlabel('Времия [c]')
    elif title == 'Импульсная характеристика':
        pyplot.plot(x, y, 'green')
        pyplot.ylabel('Амплитуда')
        pyplot.xlabel('Времия [c]')
    elif title == 'АЧХ':
        pyplot.plot(x, y, 'red')
        pyplot.ylabel('Амплитуда')
        pyplot.xlabel('ω [рад/с]')
    elif title == 'ФЧХ':
        pyplot.plot(x, y, 'purple')
        pyplot.ylabel('Фаз [град]')
        pyplot.xlabel('ω [рад/с]')
        # pyplot.ylim(-90, 90)
    pyplot.title(title)

unitName = choice()
unit, k, t = getUnit(unitName)

if unitName == 'Идеальное дифференцирующее звено':
    print(color.Fore.RED + 'Выходная функция представляет собой единичную импульсную функцию, которая не показана на графике!')
else:
    timeLine = []
    for i in range(0, 15000):
        timeLine.append(i/1000)
    [y, x] = matlab.step(unit, timeLine)
    graph(1, 'Переходная характеристика', y, x)
    [y, x] = matlab.impulse(unit, timeLine)
    graph(2, 'Импульсная характеристика', y, x)

omegaLine = []
for i in range(1, 15000):
    omegaLine.append(i/1000)
amb = []
phase = []
if unitName == 'Безынерционное звено':
    for omega in omegaLine:
        amb.append(k)
        phase.append(0)
elif unitName == 'Апериодическое звено':
    for omega in omegaLine:
        amb.append(k/((t*omega)**2+1)**0.5)
        phase.append(180*math.atan(-t*omega)/numpy.pi)
elif unitName == 'Интегрирующее звено':
    for omega in omegaLine:
        amb.append(1/(t*omega))
        phase.append(-90)
elif unitName == 'Идеальное дифференцирующее звено':
    for omega in omegaLine:
        amb.append(omega)
        phase.append(90)
elif unitName == 'Реальное дифференцирующее звено':
    for omega in omegaLine:
        amb.append(k*omega/((t*omega)**2+1)**0.5)
        phase.append(180*math.atan(1/(t*omega))/numpy.pi)

graph(3, 'АЧХ', amb, omegaLine)
graph(4, 'ФЧХ', phase, omegaLine)
pyplot.show()