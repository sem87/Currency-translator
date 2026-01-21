class A:
    x = 22


class Cal:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def delenie(self) -> float:
        """Деление"""
        try:
            if self.y == 0:
                raise ZeroDivisionError("деление на ноль")
            elif not (isinstance(self.x, (int, float)) and isinstance(self.y, (int, float))):
                raise TypeError("Неверный тип данных")
            return self.x / self.y
        except ZeroDivisionError as e:
            print(f"Ошибка деления: {e}")
            raise
        except TypeError as e:
            print(f"Ошибка типа: {e}")
            raise  # повторно выбрасываем исключение
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            raise

    def ymnozen(self) -> float:
        """Умножение"""
        return self.x * self.y

    def add(self) -> float:
        """Сложение"""
        return self.x + self.y

    def razn(self) -> float:
        """Разность"""
        return self.x - self.y

    def __str__(self):
        return str(self.add())


if __name__ == "__main__":
    print(Cal(3.02, 0).delenie())
