#Лабораторная работа №8
# Жидков А. В.
# ДПИ22-1
import numpy as np
import multiprocessing
import os
import time

def generate_matrix(size):
    """Генерирует случайную квадратную матрицу заданного размера."""
    return np.random.rand(size, size)

def write_element_to_file(filename, element):
    """Записывает элемент в файл."""
    with open(filename, 'a') as f:
        f.write(f"{element}\n")

def multiply_elements(queue, output_file, stop_event):
    """Перемножает элементы матриц, получая их из очереди."""
    while not stop_event.is_set():
        try:
            a, b, row, col = queue.get(timeout=1)  # Ждет элемент из очереди
            result = a[row][col] * b[row][col]
            write_element_to_file(output_file, result)
        except Exception as e:
            # Если очередь пуста и произошла ошибка, просто продолжаем
            if str(e) != 'Queue is empty':
                print(f"Ошибка: {e}")

def main(matrix_size, output_file):
    # Создание очереди для передачи данных
    queue = multiprocessing.Queue()
    
    # Событие для остановки процесса перемножения
    stop_event = multiprocessing.Event()
    
    # Запуск процесса перемножения
    multiplier_process = multiprocessing.Process(target=multiply_elements, args=(queue, output_file, stop_event))
    multiplier_process.start()

    try:
        while True:
            # Генерация двух случайных матриц
            matrix_a = generate_matrix(matrix_size)
            matrix_b = generate_matrix(matrix_size)

            # Заполнение очереди поэлементными задачами
            for row in range(matrix_size):
                for col in range(matrix_size):
                    queue.put((matrix_a, matrix_b, row, col))

            # Задержка для имитации времени генерации
            time.sleep(1)

    except KeyboardInterrupt:
        print("Остановка процесса перемножения...")
        stop_event.set()  # Устанавливаем событие остановки
        multiplier_process.join()  # Ждем завершения процесса

if __name__ == "__main__":  # Исправлено имя на __name__
    matrix_size = 3  # Задайте размерность матрицы (например, 3x3)
    output_file = "result_matrix.txt"  # Путь к файлу для записи результата

    # Удаление файла результата, если он существует
    if os.path.exists(output_file):
        os.remove(output_file)

    # Определение количества процессов на основе доступных ядер
    num_processes = multiprocessing.cpu_count()

    print(f"Используется {num_processes} процессов.")
    
    main(matrix_size, output_file)
