import os
import random
import threading
import time


FILE_STORAGE_PATH = os.path.expanduser('~')


def calc_signals_per_minute(signals: int) -> int:
    return int(60 / signals)


def calc_steps(minutes: int, sleep_len: int) -> int:
    return int((minutes * 60) / sleep_len)


def ensure_file_exists(category: str) -> None:
    path = os.path.join(FILE_STORAGE_PATH, category)

    with open(path, 'w') as _:
        pass


def write_to_file(category: str, contents: any) -> None:
    path = os.path.join(FILE_STORAGE_PATH, category)

    with open(path, 'a') as file:
        file.writelines([str(contents)])


def produce_signals(category: str, sleep_len: int, minutes: int, lo: int, hi: int) -> None:
    ensure_file_exists(category)

    steps = calc_steps(minutes, sleep_len)

    print(f'{steps} {category} steps will be produced...')

    for step in range(steps):
        temperature = random.uniform(lo, hi)

        print(f'Writing {category}, step {step}...')
        write_to_file(category, temperature)

        time.sleep(sleep_len)


def send_temperature_signal(sleep_len: int, minutes: int) -> None:
    produce_signals('temperature', sleep_len, minutes, 20, 30)


def send_wind_speed_signal(sleep_len: int, minutes: int) -> None:
    produce_signals('wind_speed', sleep_len, minutes, 0, 250)


def send_humidity_signal(sleep_len: int, minutes: int) -> None:
    produce_signals('humidity', sleep_len, minutes, 0, 100)


threads = [
    threading.Thread(
        target=send_temperature_signal,
        args=(calc_signals_per_minute(10), 1)),
    threading.Thread(
        target=send_wind_speed_signal,
        args=(calc_signals_per_minute(60), 1)),
    threading.Thread(
        target=send_humidity_signal,
        args=(calc_signals_per_minute(20), 1))]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
