import json

from requests import Session

with open('auth_file.json', 'r') as file:
    auth_dict = json.load(file)

def working_example():

    url1 = 'https://online.unicum.ru/n/'
    url2 = 'https://online.unicum.ru/wjson/getauth.json'
    with Session() as s:

        r = s.post(url1, auth_dict)
        print(r.content)
        print(r.cookies)
        print(r.status_code)

        r_auth = s.post(url2)
        print(r_auth.content)
        print(r_auth.cookies)
        print(r_auth.status_code)

        # r = s.post(URL2, data='username and password data payload')

def login(session):
    url_login = 'https://online.unicum.ru/n/'
    session.post(url_login, data=auth_dict)

def getauth():
    """
    Запрос возвращает информацию о пользователе, из-под которого осущеслвена авторизация.
    На входе: ничего (все данные игнорируются, запрос может быть даже отправлен в форме GET)
    Код страницы: 401. Текстовый код: Unauthorized. Содержимое: отсутствует. Требуется авторизация.
    Код страницы: 403. Текстовый код: Forbidden. Означает, что логин и пароль были введены неверно более 3-х раз. Вход заблокирован на час.
    Код страницы: 500. Текстовый код: Internal Server Error.Содержимое: {"error":3,"errors":"Not enough memory"}. Означает ошибку на сервере (мало памяти, невозможно обработать запрос).
    Код страницы: 500. Текстовый код: Internal Server Error.Содержимое: {"error":1001,"errors":"database error"}. Означает ошибку базы данных.
    Код страницы: 200. Текстовый код: OK. Содержимое:
    {
        "user":{....},	//см. запрос login.json
        "defaultpage":?,	//целое число, обозначающее дефолтную стартовую страницу (1 - страница маршрута, 0 - стандартная стартовая страница).
        "compbm":?,		//строка или null - букмарк компании, которой принадлежит пользователь. Значение null говорит о том, что пользователь принадлежит компании root.
        "route_guid":?		//строка или null - GUID маршрута, за которым закреплен пользователь. Значение null говорит о том, что пользователь не закреплен ни за каким маршрутом.
    }
    """
    url = 'https://online.unicum.ru/wjson/getauth.json'
    with Session() as session:
        login(session)
        request = session.post(url)
        return load_json_response(request)


def getmachines():
    """
    https://online.unicum.ru/(????/)wjson/getmachines.json
    Без прав доступа
    Запрос возвращает список автоматов по компании.
    На входе:
    {
        "compbm":?,		//Необязательный параметр: строка или null. Задает букмарк компании, автоматы которой нужны. Значение null (или отсутствие параметра) означает компанию,
                    //которой принадлежит запрашивающий логин.
        "machinebm":?,		//Необязательный параметр: строка. При наличии, параметры "compbm" и "subcompanies" игнорируются. Задает букмарк автомата, данные по которому нужно обновить.
        "subcompanies":?,	//Необязательный параметр: true или false. Указывает, требуется ли включать автоматы всех подкомпаний (true) или нет (false). При отсутвтсии считается равным false.
        "errorweight":?,	//Необязательный параметр: true или false. Указывает, требуется ли включать в ответ ошибки (true) или нет (false). При отсутвтсии считается равным false. При true, время обработки зарпоса увеличивается.
        "geo_auto":?,		//Необязательный параметр: true или false. Указывает, требуется ли включать в ответ автоматическую геолокацию (true) или нет (false). При отсутвтсии считается равным false. При true, время обработки зарпоса увеличивается.
        "lastEncashment":?,	//Необязательный параметр: true или false. Указывает, требуется ли включать в ответ время последней инкассации (true) или нет (false). При отсутвтсии считается равным false. При true, время обработки зарпоса увеличивается.
        "nextEncashment":?,	//Необязательный параметр: true или false. Указывает, требуется ли включать в ответ время следующего обслуживания (true) или нет (false). При отсутвтсии считается равным false. При true, время обработки зарпоса увеличивается.
        "products":?		//Необязательный параметр: true или false. Указывет требуется ли включать в ответ данные по заканчивающимся товарам, числу и стоимости продаж или нет. Если указано true, требуется право доступа "Текущий аналих". При этом, время обработки зарпоса увеличивается.
    }
    На выходе:
    что на выходе смотри описание в nvmc_json.txt, там куча текста
    """
    url = 'https://online.unicum.ru/wjson/getmachines.json'
    with Session() as session:
        login(session)
        request = session.post(url)
        return load_json_response(request)


def json_to_pretty_print_string(json_content):
    pretty_print_json = json.dumps(json_content, indent=4, sort_keys=True)
    return pretty_print_json


def load_json_response(request):
    json_content = json.loads(request.content)
    return json_content


if __name__ == '__main__':
    json_content = getmachines()
    print(json_to_pretty_print_string(json_content))
