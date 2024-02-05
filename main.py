import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gamma


# Функция для вычисления параметров a и scale (sc) на основе математического ожидания (mexp) и дисперсии (v)
def calc_a_and_scale(mexp, v):
    sc = v / mexp
    a = mexp / sc
    return a, sc


# Функция для создания и сохранения графика гамма-распределения и гистограммы выборки
def calc_gamma_distr(a, sc, loc, anom, anom_min, anom_max, hours, n):
    # Создаем фигуру и ось для графика
    fig, ax = plt.subplots(1, 1)

    # Вычисляем моменты распределения гамма
    mean, var, skew, kurt = gamma.stats(a, loc=loc, scale=sc, moments='mvsk')
    print(f"mean:{mean}, var:{var}, skew:{skew}, kurt:{kurt}")

    # Генерируем значения для построения плотности вероятности гамма-распределения
    x = np.linspace(0, anom_max - loc, 100)
    ax.plot(hours - x, gamma.pdf(x, a, loc=loc, scale=sc), 'r-', lw=5, alpha=0.6, label='gamma pdf')

    # Генерируем случайную выборку из гамма-распределения
    r = list(filter(lambda i: 0 < i <= 168, [hours - i for i in gamma.rvs(a, loc=loc, scale=sc, size=n)]))

    # Добавляем аномалии к выборке
    r += [np.random.randint(anom_min, anom_max) for _ in range(anom)]

    # Создаем гистограмму выборки
    ax.hist(r, density=True, bins=int(hours - loc - 1), histtype='stepfilled', alpha=0.2, color= 'purple')

    # Устанавливаем ограничения для оси x
    ax.set_xlim([x[0], x[-1]])

    # Добавляем легенду
    ax.legend(loc='best', frameon=False)

    # Сохраняем график как изображение
    plt.savefig('distribution.png')

    # Сохраняем выборку в файл
    with open("out.txt", 'w') as out:
        [out.write(str(i) + '\n') for i in r]


def main():
    try:
        print("Введите данные (Enter для значений по умолчанию)")

        # Запрашиваем исходные данные у пользователя
        hours = input("Кол-во выделенных часов (168): ") or 168
        hours = int(hours)

        mexp = input(f"Мат ожидание ({hours - 45}): ") or (hours - 45)
        mexp = float(mexp)

        loc = input("Сдвиг (0): ") or 0.0
        loc = float(loc)

        v = input("Дисперсия (1350): ") or 1350.0
        v = float(v)

        n = input("Кол-во значений выборки (15000): ") or 15000

        anom = input("Кол-во аномалий (0): ") or 0
        anom = int(anom)

        if anom != 0:
            anom_min_p = int(input("Минимальный % отклонения аномалии (0): ")) / 100
            anom_max_p = int(input("Максимальный % отклонения аномалии (5): ")) / 100
            anom_min = int(hours * (1 + anom_min_p))
            anom_max = int(hours * (1 + anom_max_p))
        else:
            anom_min = anom_max = hours
        # меняем мат ожидание кол-ва часов до выполенения на мат ожидание кол-ва часов до дедлайна
        mexp = hours - mexp

        a, sc = calc_a_and_scale(mexp, v)

        # Вызываем функцию для создания графика и сохранения данных
        calc_gamma_distr(a, sc, loc, anom, anom_min, anom_max, hours, n)

    except ValueError as err:
        print("Ошибка: Некорректный ввод. ", err.args)


if __name__ == "__main__":
    main()
