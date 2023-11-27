from typing import Dict, Optional
import re
import json
from api_module import api_handler
import settings


def city_location(city: str) -> Optional[Dict[str, str]]:
    """
    Поиск города в апи
    :param city: название города
    :return: список городов
    """
    url = f'https://{settings.site_api}/locations/v3/search'

    querystring: dict = {
        'q': city,
        'locale': 'ru_RU',
        'langid': '1033',
        'siteid': '300000001'
    }

    headers: dict = {
        'X-RapidAPI-Key': settings.site_api_key,
        'X-RapidAPI-Host': settings.site_api
    }

    response = api_handler.make_request(method='GET', url=url, headers=headers,
                                        params=querystring)
    if response:
        pattern = r'"@type":.*"gaiaRegionResult"'
        find_result = re.search(pattern, response)

        if find_result:
            result = json.loads(response)
            cities = {}

            for sr in result.get('sr', []):
                if sr.get('@type') == 'gaiaRegionResult':
                    city = sr['regionNames']['shortName']
                    city_id = sr['gaiaId']
                    cities[city_id] = city

            return cities

    return {}
