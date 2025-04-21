import os
from typing import Optional, Dict, Any, Union

import pandas as pd
from dotenv import load_dotenv
import requests
import json

class ApiHandler:

    def __init__(self, base_url: str, api_key_env_name: str):
        load_dotenv()

        self.base_url = base_url.rstrip('/')
        self.api_key_env_name = api_key_env_name
        self.api_key = os.getenv(api_key_env_name)

        if not self.api_key:
            raise ValueError(f"API key not found in environment variables: {api_key_env_name}")

    def _get_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        if additional_headers:
            headers.update(additional_headers)

        return headers

    def make_request(
            self,
            endpoint: str,
            method: str = 'GET',
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Union[Dict[str, Any], str]] = None,
            headers: Optional[Dict[str, str]] = None,
            json_data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=self._get_headers(headers),
                params=params,
                data=data,
                json=json_data
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            raise

    def get_json(
            self,
            endpoint: str,
            method: str = 'GET',
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Union[Dict[str, Any], str]] = None,
            headers: Optional[Dict[str, str]] = None,
            json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        response = self.make_request(endpoint, method, params, data, headers, json_data)
        try:
            return response.json()
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from response: {response.text}")
            raise

    def get_dataframe(
            self,
            endpoint: str,
            method: str = 'GET',
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Union[Dict[str, Any], str]] = None,
            headers: Optional[Dict[str, str]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            json_normalize_path: Optional[str] = None
    ) -> pd.DataFrame:

        json_response = self.get_json(endpoint, method, params, data, headers, json_data)


        if json_normalize_path:
            nested_data = json_response
            for key in json_normalize_path.split('.'):
                nested_data = nested_data[key]
            return pd.json_normalize(nested_data)

        if isinstance(json_response, list):
            return pd.DataFrame(json_response)

        elif isinstance(json_response, dict):
            if len(json_response) == 1 and isinstance(list(json_response.values())[0], list):
                return pd.DataFrame(list(json_response.values())[0])
            else:

                return pd.json_normalize(json_response)

        else:
            raise ValueError(f"Cannot convert response to DataFrame: {type(json_response)}")
