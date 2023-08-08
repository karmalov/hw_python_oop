class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        """"Вернуть сообщение о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:0.3f} ч.; '
                f'Дистанция: {self.distance:0.3f} км; '
                f'Ср. скорость: {self.speed:0.3f} км/ч; '
                f'Потрачено ккал: {self.calories:0.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MINS_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist: float = self.action * self.LEN_STEP / self.M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return 0

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message: InfoMessage = InfoMessage(type(self).__name__,
                                                self.duration,
                                                self.get_distance(),
                                                self.get_mean_speed(),
                                                self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Вернуть количество затраченных калорий."""
        spent_calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                 * self.get_mean_speed()
                                 + self.CALORIES_MEAN_SPEED_SHIFT)
                                 * self.weight / self.M_IN_KM
                                 * self.duration * self.MINS_IN_HOUR
                                 )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WGHT_MULTIPLIER1: float = 0.035
    CALORIES_WGHT_MULTIPLIER2: float = 0.029
    KMPH_TO_MPS: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height / self.CM_IN_M

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.CALORIES_WGHT_MULTIPLIER1 * self.weight
                                 + (self.get_mean_speed() * self.KMPH_TO_MPS)
                                 ** 2 / self.height
                                 * self.CALORIES_WGHT_MULTIPLIER2 * self.weight
                                  ) * self.duration * self.MINS_IN_HOUR)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_SPEED_SHIFT: float = 1.1
    CALORIES_DOUBLE: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Вернуть среднюю скорость."""
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = (
            (self.get_mean_speed() + self.CALORIES_SPEED_SHIFT)
            * self.CALORIES_DOUBLE * self.weight * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_code_class: dict = {'SWM': Swimming,
                                 'RUN': Running,
                                 'WLK': SportsWalking}
    value = training_code_class[workout_type](*data)
    return value


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
