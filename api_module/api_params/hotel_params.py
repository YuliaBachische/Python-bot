from typing import Dict, Optional, List, Any
import json
from api_module.api_handler import make_request
from settings import site_api, site_api_key


def custom(data: dict) -> Optional[List[dict]]:
    hotels: List[dict] = hotel_params(
        data['city_id'],
        data['date_check_in'],
        data['date_check_out'],
        data['hotels_num'],
        'DISTANCE',
        data['min_price'],
        data['max_price']
    )
    return hotels


def low_price(data: dict) -> Optional[List[dict]]:
    return hotel_params(
        data['city_id'],
        data['date_check_in'],
        data['date_check_out'],
        data['hotels_num']
    )


def high_price(data: dict) -> Optional[List[dict]]:
    hotels: List[dict] = hotel_params(
        data['city_id'],
        data['date_check_in'],
        data['date_check_out'],
        data['hotels_num'],
        'DISTANCE'
    )
    return sorted(hotels, key=lambda x: x['price'], reverse=True)


def hotel_params(city_id: str,
                 date_check_in: str,
                 date_check_out: str,
                 hotels_num: int,
                 sort: Optional[str] = None,
                 min_price: Optional[int] = None,
                 max_price: Optional[int] = None
                 ) -> Optional[List[Dict[str, str]]]:
    url = f'https://{site_api}/properties/v2/list'
    day_in, month_in, year_in = map(int, date_check_in.split('/'))
    day_out, month_out, year_out = map(int, date_check_out.split('/'))

    payload = {
        'currency': 'USD',
        'eapid': 1,
        'locale': 'ru_RU',
        'siteId': 300000001,
        'destination': {'regionId': city_id},
        'checkInDate': {
            'day': day_in,
            'month': month_in,
            'year': year_in
        },
        'checkOutDate': {
            'day': day_out,
            'month': month_out,
            'year': year_out
        },
        "rooms": [
            {
                "adults": 1
            }
        ],
        'resultsStartingIndex': 0,
        'resultsSize': int(hotels_num),
        'sort': 'PRICE_LOW_TO_HIGH'
    }
    headers = {
        'X-RapidAPI-Key': site_api_key,
        'X-RapidAPI-Host': site_api
    }

    payload['filters'] = {
        'price': {
            'max': max_price,
            'min': min_price
        }
    }

    if sort:
        payload['sort'] = sort

    response = make_request(method='POST', url=url, headers=headers,
                            json=payload)
    if response:
        result = json.loads(response)
        result = unpack(result, ['data', 'propertySearch', 'properties'])
        if result is None:
            return None

        hotels = list()
        for hotel in result:
            hotels.append({
                'hotel_id': hotel.get('id'),
                'hotel': hotel.get('name'),
                'price': float(unpack(hotel, ['price', 'lead', 'amount'])),
            })
        return hotels


def unpack(the_dict: dict, keys: list) -> Any:
    value = the_dict
    for key in keys:
        value = value.get(key)
        if value is None:
            break
    return value
