import wmi
import time
import matplotlib.pyplot as plt
import numpy as np


def get_temperature():
    w = wmi.WMI(namespace="root\\OpenHardwareMonitor")

    # Получение температуры процессора
    temperature_info = w.Sensor()
    for sensor in temperature_info:
        if sensor.SensorType == 'Temperature' and 'CPU Package' in sensor.Name:
            return sensor.Value
    return None


def collect(interval, count):

    unit = []  # Cписок (время, значение температуры)
    current_time = 0  # Время от начала измерений

    print(
        f"Проводим измерение температуры процессора с интервалом"
        f" {interval} секунд ({count} измерений)."
    )
    for i in range(count):
        print(f"Измерение {i + 1}")
        temperature = get_temperature()

        if temperature is None:
            print("Температура процессора недоступна. Пропускаем измерение.")
            continue

        unit.append((current_time, temperature))  # Сохраняем время и температуру
        print(f"Время: {current_time}с, Температура: {temperature}°C")

        current_time += interval
        if i < count - 1:
            time.sleep(interval)

    print("\nСерия измерений проведена.")
    return unit


def main():
    # Количество измерений
    num_measurements = 50
    # Интервал измерений (секунды)
    interval = 0.5

    # Сбор данных
    measurements = collect(interval, num_measurements)

    # Разделение данных на время и температуру
    times, temperatures = zip(*measurements)

    # Вычисление математического ожидания и среднеквадратичного отклонения
    mean_temperature = np.mean(temperatures)
    std_temperature = np.std(temperatures)
    print(f"Математическое ожидание: {mean_temperature}°C")
    print(f"Среднеквадратичное отклонение: {std_temperature}°C")

    # График
    plt.figure(figsize=(16, 10))
    plt.plot(times, temperatures, marker='o', linestyle='-', color='r')
    plt.title('График изменения температуры CPU по времени')
    plt.xlabel('Время (секунды)')
    plt.ylabel('Температура (°C)')
    plt.grid(True)
    plt.show()

    # Гистограмма
    plt.figure(figsize=(16, 10))
    plt.hist(temperatures, bins=10, edgecolor='black')
    plt.title('Гистограмма распределения температуры CPU')
    plt.xlabel('Температура (°C)')
    plt.ylabel('Частота')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
