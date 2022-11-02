# Проект парсинга pep


## Описание проекта:
Парсер документации PEP, c офицального сайта документации Python

## Основные возможности:

скачивание архива документации Python, парсинг статусов документации PEP, парсинг обновлений версий Python. 
Для начала работы, после установки зависимостей в териманале 
ввести команду (будут выведены параметры).

python main.py -h

Парсинг статусов PEP
```
python main.py pep
```
Парсинг новвоведений Python
```
python main.py wats-new
```
Загрузка документации
```
python main.py download
```
Парсинг статусов версий Python
```
python main.py latest-versions
```
## Системные требования:
appdirs==1.4.4
atomicwrites==1.4.1
attrs==21.4.0
beautifulsoup4==4.9.3
cattrs==22.2.0
certifi==2021.10.8
chardet==4.0.0
charset-normalizer==2.0.12
colorama==0.4.6
exceptiongroup==1.0.0
flake8==4.0.1
idna==2.10
importlib-metadata==4.2.0
iniconfig==1.1.1
itsdangerous==2.1.1
lxml==4.6.3
mccabe==0.6.1
numpy==1.23.4
packaging==21.3
pandas==1.5.1
pluggy==1.0.0
prettytable==2.1.0
py==1.11.0
pycodestyle==2.8.0
pyflakes==2.4.0
pyparsing==3.0.7
pytest==7.1.0
python-dateutil==2.8.2
pytz==2022.5
requests==2.27.1
requests-cache==0.6.3
requests-mock==1.9.3
six==1.16.0
soupsieve==2.3.1
tomli==2.0.1
tqdm==4.61.0
typing_extensions==4.1.1
url-normalize==1.4.3
urllib3==1.26.8
wcwidth==0.2.5
zipp==3.7.0

