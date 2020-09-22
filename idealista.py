import requests

URL = ' https://api.idealista.com/3.5/es/search'


def get_properties(bearer, type_of_operation, latitude, longitude, num_page):



    headers = {'Authorization': 'Bearer ' + bearer,
               'Content-Type' : 'application/x-www-form-urlencoded'
            }

    payload = {
        'country': 'es',
        'operation': type_of_operation,
        'propertyType': 'homes',
        'locale': 'es',
        #'center': str(latitude) + ',' + str(longitude),
        'locationId': '0-EU-ES-46-02-002-250',
        'distance': 30000.0,
        'maxItems': 50,
        'numPage': num_page
    }

    r = requests.post(URL, data = payload, headers = headers)
    if r.status_code != 200:
        return False
    return r.json()