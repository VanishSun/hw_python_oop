from __future__ import annotations
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Создание информационного сообщениея о тренировке"""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65       # Длинна одного шага.
    M_IN_KM: int = 1000          # Перевод км в метры.
    HOURS_TO_MIN = 60            # Перевод часов в минуты.

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_RUN_1 = 18     # Два коэффициента для расчета каллорий бега.
    COEFF_CALORIE_RUN_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return (
            (self.COEFF_CALORIE_RUN_1 * self.get_mean_speed()
             - self.COEFF_CALORIE_RUN_2) * self.weight / self.M_IN_KM
            * self.duration * self.HOURS_TO_MIN
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_WLK_1 = 0.035     # Два коэффициента для расчета
    COEFF_CALORIE_WLK_2 = 0.029     # каллорий спортивной ходьбы.

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.COEFF_CALORIE_WLK_1 * self.weight
             + (self.get_mean_speed() ** 2 // self.height)
             * self.COEFF_CALORIE_WLK_2 * self.weight) * self.duration
            * self.HOURS_TO_MIN
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38             # Длинна одного гребка.
    COEFF_CALORIE_SWM_1 = 1.1   # Два коэффициента для расчета
    COEFF_CALORIE_SWM_2 = 2     # каллорий плавания.

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.COEFF_CALORIE_SWM_1)
            * self.COEFF_CALORIE_SWM_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings: dict[str, object] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return trainings[workout_type](*data)
    except KeyError:
        print(
            f'KeyError: Тип тренировки {workout_type} '
            f'не может быть обработан.'
        )


def main(training: Training) -> None:
    """Главная функция."""
    try:
        info = training.show_training_info()
        result: str = info.get_message()
        print(result)
    except AttributeError:
        return


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
