from scipy.stats import norm
def num6():
    # Данные
    mean_X = 5.5  # средняя выработка на одного рабочего
    sigma = 1.5   # стандартное отклонение
    n = 150       # размер выборки
    confidence_level = 0.99

    # Нахождение z-значения
    z_value = norm.ppf((1 + confidence_level) / 2)

    # Вычисление доверительного интервала
    margin_error = z_value * (sigma / (n**0.5))
    lower_bound = mean_X - margin_error
    upper_bound = mean_X + margin_error

    print(lower_bound, upper_bound, z_value)
def num7():
    from scipy.stats import norm

    # Уровень доверия
    confidence_level = 0.90

    # Если уровень доверия составляет 90%, то по каждую сторону остаётся 5% (в сумме 10%).
    # Следовательно, z-оценку, которая оставляет 5% справа, что соответствует 95% всех значений слева от этой точки

    """n = (Z * σ / E)^2 где 
    n – размер выборки, 
    Z – значение стандартного нормального распределения для заданного уровня доверия, 
    σ – стандартное отклонение популяции
    E – требуемая точность."""

    z_score = norm.ppf((1 + confidence_level) / 2)
    sigma = 150
    E = 10

    print(f"z = {z_score:.4f} для {confidence_level * 100}%")
    print("n = ", round((z_score * sigma / E) ** 2))