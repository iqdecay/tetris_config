import requests


def get_request(api_url: str) -> dict:
    """
    Send an HTTP GET request to an address, and return its JSON content as dict
    :param api_url: address of the API endpoint returning JSON content
    :return: dictionary corresponding to the JSON of the response
    """
    try:
        response = requests.get(api_url)
        if response.status_code in (200, 204):
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            raise Exception(f"Error with GET request to {api_url} : status "
                            f"code {response.status_code}")
    except Exception as e:
        print(f"Error with GET request to {api_url} : {e}")
        raise


def post_request(api_url: str, json_content: dict) -> dict:
    """
    Send an HTTP POST request to address with the json_content body and return
    the response of the server
    :param api_url: address of the API endpoint accepting JSON content
    :param json_content: to transmit to the API
    :return: the response of the server
    """
    try:
        response = requests.post(api_url, json=json_content)
        if response.status_code in (200, 204):
            return response.text
        else:
            raise Exception(f"Error with POST request to {api_url} : status "
                            f"code {response.status_code}")
    except Exception as e:
        print(f"Error with POST request to {api_url} : {e}")
        raise
