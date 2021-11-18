from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
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
    word_type = get_word_type_of_age(years)
    result = f'Уже {years} {word_type} с вами'
    return result


def get_wine_data_from_excel(filepath):
    excel_data_df = pandas.read_excel(filepath, na_values=['N/A', 'NA', 'NaN', 'nan'], keep_default_na=False)
    return excel_data_df.to_dict('records')


if __name__ == '__main__':
    wines = get_wine_data_from_excel('wine.xlsx')
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
