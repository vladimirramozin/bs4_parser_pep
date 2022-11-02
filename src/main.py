import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PEP_DOC_URL,
                       STATUS)
from exceptions import ParserFindTagException
from outputs import control_output
from utils import find_tag, get_response


def pep(session):
    """функция парсит страницы документации PEP (конечные страницы),
       и собирает статусы версий"""
    result_for_common_page = main_pep(session)
    result_for_end_point = {}
    if response_end_point is None:
        raise ConnectionError
    for key in tqdm(
        result_for_common_page,
        desc='процесс загрузки информации'
        'с конечных  страниц документации PEP'
    ):
        url_end_point_pep = urljoin(PEP_DOC_URL, key)
        response_end_point = get_response(session, url_end_point_pep)
        soup_end_point = BeautifulSoup(
            response_end_point.text,
            features='lxml'
        )
        dd = soup_end_point.find('dl')
        status = dd.find(string='Status')
        status_value = (
            status.next_element.next_element.
            next_element.next_element.text
        )
        if status_value is None:
            raise ParserFindTagException
        result_for_end_point[key] = status_value
    result = [('Статус', 'Количество')]
    result_for_end_point_values = list(result_for_end_point.values())
    for i in STATUS:
        result.append((i, result_for_end_point_values.count(i)))
    result.append(('Total', len(result_for_end_point_values)))
    for i in result_for_end_point:
        if result_for_end_point.get(i) not in result_for_common_page.get(i):
            logging.info(f'Ожидаемые статусы:: {result_for_common_page.get(i)}'
                         f'статус в карточке {result_for_end_point.get(i)}')
    return result


def main_pep(session):
    """функция парсит главную страницу документации PEP,
    и собирает статусы версий"""
    url_info_pep = PEP_DOC_URL
    response = get_response(session, url_info_pep)
    if response is None:
        raise ConnectionError
    soup = BeautifulSoup(response.text, features='lxml')
    tags_tr = soup.find_all('a')
    pattern = r'/pep-\d+'
    key = []
    for tag_tr in tags_tr:
        text_match = re.search(pattern, tag_tr['href'])
        if text_match is not None:
            version = tag_tr['href']
            key.append(version)
    status = soup.find_all('abbr')
    keys = key[1::2]
    result_for_common_page = {}
    for i in zip(keys, status):
        if len(i[1].text) == 2:
            result_for_common_page[i[0]] = EXPECTED_STATUS[i[1].text[-1]]
            continue
        if len(i[1].text) == 1:
            result_for_common_page[i[0]] = EXPECTED_STATUS['']
    return result_for_common_page


def whats_new(session):
    """функция собирает данные о нововведениях в крайней версии Python"""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    if response is None:
        raise ConnectionError
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )
    result = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(
        sections_by_python,
        desc='процесс загрузки информации с сайта документации python'
    ):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        result.append((version_link, h1.text, dl_text))
    return result


def latest_versions(session):
    """функция парсит версии Python и выводит в каком они статусе"""
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        raise ConnectionError
    soup = BeautifulSoup(response.text, features='lxml')
    sidebar = soup.find_all('div', attrs={'class': 'sphinxsidebarwrapper'})
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    ul_tags = []
    results = []
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for i in sidebar:
        ul_tags = i.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            for a_tag in a_tags:
                if 'All' in str(a_tag.text):
                    link = a_tag['href']
                    version, status = a_tag.text, ''
                    results.append((link, version, status))
                    break
                res = []
                link = a_tag['href']
                text_match = re.search(pattern, a_tag.text)
                res.append(link)
                buf = list(text_match.group(1, 2))
                version, status = (
                    text_match.groups() if text_match else (a_tag.text, '')
                )
                results.append((link, version, status))
            break
    else:
        raise Exception('Ничего не нашлось')
    return results


def download(session):
    """функция скачивает архив с документацией Python"""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        raise ConnectionError
    soup = BeautifulSoup(response.text, 'lxml')
    tags = soup.find_all('td')
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    for tag in tags:
        res = tag.find('a', attrs={'href': re.compile(r'.+pdf-a4\.zip$')})
        if res is not None:
            archive_url = urljoin(MAIN_DOC_URL, res['href'])
            filename = archive_url.split('/')[-1]
            archive_path = downloads_dir / filename
            response = session.get(archive_url)
            with open(archive_path, 'wb') as file:
                file.write(response.content)
            logging.info(f'Архив был загружен и сохранён: {archive_path}')


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    """функция управляет конфигурацией парсера"""
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
