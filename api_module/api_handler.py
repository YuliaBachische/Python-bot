from typing import Dict, Optional

import requests
from loguru import logger


def make_request(method: str, url: str, headers: Dict[str, str], **kwargs) -> Optional[str]:
    try:
        response = requests.request(method=method, url=url, headers=headers, timeout=10, **kwargs)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}")
        raise
    except requests.exceptions.ConnectionError as errc:
        logger.error(f"Error Connecting: {errc}")
        raise
    except requests.exceptions.Timeout as errt:
        logger.error(f"Timeout Error: {errt}")
        raise
    except requests.exceptions.RequestException as err:
        logger.error(f"Request Exception: {err}")
        raise



