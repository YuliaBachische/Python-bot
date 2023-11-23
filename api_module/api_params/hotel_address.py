from typing import Optional, List
import json
from api_module.api_handler import make_request
from api_module.api_params.hotel_params import unpack
from settings import site_api_key, site_api


def hotel_address(hotels: List[dict]) \
        -> Optional[List[dict]]:
    if hotels is None:
        return None

    url = f'https://{site_api}/properties/v2/detail'

    payload = {
        'currency': 'USD',
        'eapid': 1,
        'locale': 'ru_RU',
        'siteId': 300000001
    }
    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': site_api_key,
        'X-RapidAPI-Host': site_api
    }

    for index, hotel in enumerate(hotels):
        payload['propertyId'] = hotel['hotel_id']
        response = make_request(method='POST', url=url, headers=headers,
                                json=payload)
        address = None
        if response:
            result = json.loads(response)
            address = unpack(result, ['data', 'propertyInfo',
                                      'summary', 'location',
                                      'address', 'addressLine'])

        hotels[index]['address'] = address

    return hotels
