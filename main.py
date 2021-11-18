from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
from pprint import pprint


def get_word_type_of_age(age):
    if age[-2] == '1' or age[-1] in ['5', '6', '7', '8', '9']:
        result = 'лет'
    elif age[-1] == '1':
        result = 'год'
    else:
        result = 'года'
    return result


def get_age_of_winery():
    year_of_foundation = 1920
    years = str(datetime.date.today().year - year_of_foundation)
    word_type_of_age = get_word_type_of_age(years)
    result = f'Уже {years} {word_type_of_age} с вами'
    return result


def get_wines_categories(filepath):
    drinks_from_excel = pandas.read_excel(
        filepath, na_values=['N/A', 'NA', 'NaN', 'nan'], keep_default_na=False)
    drinks_info = drinks_from_excel.to_dict('records')
    wines_by_categories = collections.defaultdict(list)
    for drink in drinks_info:
        category = drink['Категория']
        wines_by_categories[category].append(drink)
    return wines_by_categories


if __name__ == '__main__':
    wines = get_wines_categories('wine2.xlsx')
    pprint(wines)
    env = Environment(loader=FileSystemLoader('.'),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')
    rendered_page = template.render(
        age_of_winery=get_age_of_winery(),
        wines=wines
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
