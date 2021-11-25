import matplotlib.pyplot as plt
import control as ctrl
import colorama as color
import numpy as np
import sympy as sp

# Выбор типа обратной связи
def choice_feedback():
    hard_feedback = 'Жесткая обратная связь (Ж)'
    flexible_feedback = 'Гибкая обратная связь (Г)'
    aperiodic_hard_feedback = 'Апериодическая жесткая обратная связь (АЖ)'
    aperiodic_flexible_feedback = 'Апериодическая гибкая обратная связь (АГ)'

    needNewChoice = True
    while needNewChoice:
        print(color.Style.RESET_ALL)
        userInput = input(color.Fore.CYAN + 'Выберите тип обратной связи:\n'
                          '1 - ' + hard_feedback + ';\n'
                          '2 - ' + flexible_feedback + ';\n'
                          '3 - ' + aperiodic_hard_feedback + ';\n'
                          '4 - ' + aperiodic_flexible_feedback + '.\n'
                          'Ваш выбор:'
                          )
        if userInput.isdigit():
            needNewChoice = False
            userInput = int(userInput)
            if userInput == 1:
                feedback = hard_feedback
            elif userInput == 2:
                feedback = flexible_feedback
            elif userInput == 3:
                feedback = aperiodic_hard_feedback
            elif userInput == 4:
                feedback = aperiodic_flexible_feedback
            else:
                print(color.Fore.RED + '\nНедопустимое значение!')
                needNewChoice = True
        else:
            print(color.Fore.RED + '\nВведите числовое значение!')
            needNewChoice = True
    return feedback

# Выбор типа турбина
def choice_turbine():
    hydraulic_turbine = 'Гидравлическая турбина'
    steam_turbine = 'Паровая турбина'

    needNewChoice = True
    while needNewChoice:
        print(color.Style.RESET_ALL)
        userInput = input(color.Fore.CYAN + 'Выберите тип турбина:\n'
                          '1 - ' + hydraulic_turbine + ';\n'
                          '2 - ' + steam_turbine + '.\n'
                          'Ваш выбор:'
                          )
        if userInput.isdigit():
            needNewChoice = False
            userInput = int(userInput)
            if userInput == 1:
                turbine = hydraulic_turbine
            elif userInput == 2:
                turbine = steam_turbine
            else:
                print(color.Fore.RED + '\nНедопустимое значение!')
                needNewChoice = True
        else:
            print(color.Fore.RED + '\nВведите числовое значение!')
            needNewChoice = True
    return turbine

# Установка параметров и создание передаточной функции
def tf_generator(feedback, turbine):
    needNewChoice = True
    while needNewChoice:
        needNewChoice = False
        print(color.Fore.CYAN + '\nВведите значение в соответствии с параметром и замените отсутствующий параметр на 0!')
        Ku = input(color.Fore.CYAN + 'Введите коэффициент Kу:')
        Koc = input(color.Fore.CYAN + 'Введите коэффициент Kос:')
        Kpt = input(color.Fore.CYAN + 'Введите коэффициент Kпт:')
        Tg = input(color.Fore.CYAN + 'Введите коэффициент Tг:')
        Tu = input(color.Fore.CYAN + 'Введите коэффициент Tу:')
        Tgt = input(color.Fore.CYAN + 'Введите коэффициент Tгт:')
        Tpt = input(color.Fore.CYAN + 'Введите коэффициент Tпт:')
        Toc = input(color.Fore.CYAN + 'Введите коэффициент Tос:')

        if Ku.replace('.', '').isdigit()\
            and Koc.replace('.', '').replace('-', '').isdigit()\
            and Kpt.replace('.', '').replace('-', '').isdigit()\
            and Tg.replace('.', '').replace('-', '').isdigit()\
            and Tu.replace('.', '').replace('-', '').isdigit()\
            and Tgt.replace('.', '').replace('-', '').isdigit()\
            and Tpt.replace('.', '').replace('-', '').isdigit()\
            and Toc.replace('.', '').replace('-', '').isdigit():
            Ku = float(Ku)
            Koc = float(Koc)
            Kpt = float(Kpt)
            Tg = float(Tg)
            Tu = float(Tu)
            Tgt = float(Tgt)
            Tpt = float(Tpt)
            Toc = float(Toc)
            if feedback == 'Жесткая обратная связь (Ж)':
                W1 = ctrl.tf([Koc], [1])
            elif feedback == 'Гибкая обратная связь (Г)':
                W1 = ctrl.tf([Koc, 0], [1])
            elif feedback == 'Апериодическая жесткая обратная связь (АЖ)':
                W1 = ctrl.tf([Koc], [Toc, 1])
            elif feedback == 'Апериодическая гибкая обратная связь (АГ)':
                W1 = ctrl.tf([Koc, 0], [Toc, 1])
            if turbine == 'Гидравлическая турбина':
                W3 = ctrl.tf([0.01*Tgt, 1], [0.05*Tg, 1])
            elif turbine == 'Паровая турбина':
                W3 = ctrl.tf([Kpt], [Tpt, 1])
            W2 = ctrl.tf([1], [Tg, 1])
            W4 = ctrl.tf([Ku], [Tu, 1])
            open_loop = ctrl.series(W4, W3, W2)
            F = W1
            closed_loop = ctrl.feedback(open_loop, F, sign=-1)
        else:
            print('Введите числовое значение!')
            needNewChoice = True
    return open_loop, closed_loop

# Выбор этап работы
def choice_step(G, W):
    step0 = 'Выйти'
    step1 = 'Снять переходную характеристику'
    step2 = 'Определить значения полюсов передаточной функции замкнутой'
    step3 = 'Разомкнуть САУ и оценить устойчивость по критерию Найквиста'
    step4 = 'Снять ЛАЧХ и ЛФЧХ разомкнутой системы'
    step5 = 'Определить запасы устойчивости по модулю и по фазе'
    step6 = 'Построить годограф Михайлова'

    while True:
        needNewChoice = True
        while needNewChoice:
            print(color.Style.RESET_ALL)
            userInput = input(color.Fore.CYAN + 'Выберите этап работы:\n'
                              '0 - ' + step0 + ';\n'
                              '1 - ' + step1 + ';\n'
                              '2 - ' + step2 + ';\n'
                              '3 - ' + step3 + ';\n'
                              '4 - ' + step4 + ';\n'
                              '5 - ' + step5 + ';\n'
                              '6 - ' + step6 + '.\n'
                              'Ваш выбор:'
                              )

            if userInput.isdigit():
                needNewChoice = False
                userInput = int(userInput)
                if userInput == 0:
                    print('\nСпасибо за использование!')
                    exit()

                elif userInput == 1:
                    time_line = np.linspace(0, 500, 100001)
                    t, rec = ctrl.step_response(W, time_line)
                    plt.plot(t, rec)
                    plt.grid(linestyle='--', alpha=0.5)
                    plt.title('Переходная характеристика')
                    plt.xlabel('t')
                    plt.ylabel('A(t)')
                    plt.show()

                elif userInput == 2:
                    # Метод 1
                    coef = W.den[0][0]
                    D = np.poly1d(coef)
                    print(color.Fore.YELLOW + f'\nЗначения полюсов передаточной функции замкнутой:\n{D.roots}')
                    # Метод 2
                    # root = ctrl.pole(W)
                    # print(color.Fore.YELLOW + f'Значения полюсов передаточной функции замкнутой:\n{roots}')

                elif userInput == 3:
                    ctrl.nyquist(G)
                    plt.title('Кривая Найквиста')
                    plt.show()

                elif userInput == 4:
                    w = np.logspace(-3, 1, 100)
                    mag, phase, omega = ctrl.bode(G, omega=w, plot=False)
                    fig, axe = plt.subplots(nrows=2, ncols=1)

                    # ЛАЧХ
                    axe[0].semilogx(w, mag, color='blue')
                    axe[0].set_title('ЛАЧХ')
                    axe[0].set_xlabel('ω')
                    axe[0].set_ylabel('А(ω)')
                    axe[0].grid(alpha=0.5, linestyle='--')

                    # ЛФЧХ
                    axe[1].semilogx(w, phase, color='magenta')
                    axe[1].set_title('ЛФЧХ')
                    axe[1].set_xlabel('ω')
                    axe[1].set_ylabel('Ф(ω)')
                    axe[1].grid(alpha=0.5, linestyle='--')

                    plt.tight_layout()
                    plt.show()

                elif userInput == 5:
                    pass

                elif userInput == 6:
                    coef_nums = W.num[0][0]
                    coef_dens = W.den[0][0]
                    w = sp.symbols('w')
                    N, D = 0 * w, 0 * w
                    for i in range(len(coef_nums)):
                        N += coef_nums[i] * w**(len(coef_nums) - i - 1)
                    for i in range(len(coef_dens)):
                        D += coef_dens[i] * w**(len(coef_dens) - i - 1)
                    U, V = [], []
                    for i in np.linspace(0, 100, 10001):
                        f = (N/D).subs(w, (i* 1j))
                        U.append(sp.re(f))
                        V.append(sp.im(f))
                    plt.plot(U, V)
                    plt.grid()
                    plt.title('Кривая Михайлова')
                    plt.show()

                else:
                    print(color.Fore.RED + '\nНедопустимое значение!')
                    needNewChoice = True
            else:
                print(color.Fore.RED + '\nВведите числовое значение!')
                needNewChoice = True

feedback = choice_feedback()
turbine = choice_turbine()
G, W = tf_generator(feedback, turbine)
print(color.Fore.YELLOW + f'\nПередаточная функция разомкнутого контура:{G}\nПередаточная функция замкнутого контура:{W}',end='')
choice_step(G, W)