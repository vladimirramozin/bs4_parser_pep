import datetime as dt
import logging

import pandas as pd
from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT


def control_output(results, cli_args):
    """функция вызывает вариант вывода из привиденных ниже"""
    output = cli_args.output
    if output == 'pretty':
        pretty_output(results)
    elif output == 'file':
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results):
    """функция выводит в терминале"""
    for row in results:
        print(*row)


def pretty_output(results):
    """функция выводит результаты парсинга в виде таблицы"""
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    """функция выводит результаты парсинга в файл"""
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8', newline=''):
        n = [[] for _ in range(len(results[0]))]
        for i in range(len(results[0])):
            for result in results:
                n[i].append(result[i])
        data = {head: values for head, *values in n}
        df = pd.DataFrame(data)
        df.to_csv(file_path, sep=';', index=False)
    logging.info(f'Файл с результатами был сохранён: {file_path}')
