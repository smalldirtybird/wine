from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections


def get_word_type_of_age(age):
    if int(age[-2]) == 1 or int(age[-1]) in range(5, 10):
        return 'лет'
    elif int(age[-1]) == 1:
        return 'год'
    else:
        return 'года'


def get_age_of_winery():
    year_of_foundation = 1920
    years = str(datetime.date.today().year - year_of_foundation)
    word_type_of_age = get_word_type_of_age(years)
    result = f'Уже {years} {word_type_of_age} с вами'
    return result


def get_drinks_by_categories(filepath):
    drinks_from_excel = pandas.read_excel(
        filepath, na_values=['N/A', 'NA', 'NaN', 'nan'], keep_default_na=False)
    drinks_info = drinks_from_excel.to_dict('records')
    drinks_by_categories = collections.defaultdict(list)
    for drink in drinks_info:
        category = drink['Категория']
        drinks_by_categories[category].append(drink)
    drinks_sorted_by_categories = collections.OrderedDict(
        sorted(drinks_by_categories.items()))
    return drinks_sorted_by_categories.items()


if __name__ == '__main__':
    env = Environment(loader=FileSystemLoader('.'),
                      autoescape=select_autoescape(['html', 'xml'])
                      )
    template = env.get_template('template.html')
    rendered_page = template.render(
        age_of_winery=get_age_of_winery(),
        drinks_by_categories=get_drinks_by_categories('wine3.xlsx')
        )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
