import os
import threading
import time

import matplotlib.pyplot as plt

from datetime import datetime
from typing import Callable


SIGNALS = [
    'temperature',
    'wind_speed',
    'humidity']
FILE_STORAGE_PATH = os.path.expanduser('~')
data = {
    'temperature': [],
    'humidity': [],
    'wind_speed': []
}


def put_data(category: str, signals: list[float]) -> None:
    data[category] = signals


def is_last_modification_30_secs_ago(path: str) -> bool:
    mod_time_epoch = os.path.getmtime(path)
    current_time = datetime.now()
    mod_time = datetime.fromtimestamp(mod_time_epoch)
    time_difference = (current_time - mod_time).total_seconds()

    return time_difference > 30


def reader(category: str, processing_func: Callable) -> None:
    path = os.path.join(FILE_STORAGE_PATH, category)

    while not is_last_modification_30_secs_ago(path):
        print(f'Reading data for {category}...')

        with open(path, 'r', newline=os.linesep) as file:
            content = file.readlines()
            lines = list(map(float, content))

            processing_func(category, lines)

        time.sleep(10)

    print(f'Terminating reader for {category}...')


def create_plot(category: str, data: list[float]) -> None:
    path = os.path.join(FILE_STORAGE_PATH, f'{category}.pdf')
    x = list(range(len(data)))

    plt.bar(x, data)
    plt.xlabel('Index')
    plt.ylabel(category)
    plt.title(f'{category} changes')
    plt.savefig(path)
    plt.close()


threads = []


for signal in SIGNALS:
    thread = threading.Thread(target=reader, args=(signal, put_data,))

    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()


print(data)

for key, val in data.items():
    create_plot(key, val)

