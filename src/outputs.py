import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT


def control_output(results, cli_args):
    """функция вызывает вариант вывода из привиденных ниже.
    КАК ЗДЕСЬ ВЫВЕСТИ СЛОВАРЬ OUTPUTS В ФАЙЛ constatns.py, 
    ЧТОБЫ ИЗБЕЖАТЬ ЦИКЛИЧЕСКОГО ИМПОРТА???
    """
    try:
        OUTPUTS[cli_args.output](results, cli_args)
    except KeyError:
        default_output(results)


def default_output(results):
    """функция выводит в терминале"""
    for row in results:
        print(*row)


def pretty_output(results, cli_args):
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
    with open(file_path, 'w', encoding='utf-8') as f:
        
        writer = csv.writer(f, dialect='unix', escapechar=' ', quoting=csv.QUOTE_NONE) 
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {file_path}')


OUTPUTS = {
    'pretty': pretty_output,
    'file': file_output
}
