import requests
import json
import logging

class VectorDatabaseSDK:
    def __init__(self, host, port, jwt_token=None):
        self.base_url = f"http://{host}:{port}"
        self.headers = {'Content-Type': 'application/json'}
        self.jwt_token = jwt_token
        self.logger = logging.getLogger(__name__)

    # 新增或修改授权方法
    def authenticate(self, username, password):
        url = f"{self.base_url}/getJwtToken"
        payload = {"username": username, "password": password}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        self.jwt_token = response.json().get('jwtToken')


    def _send_request(self, endpoint, payload):
        if self.jwt_token:
            self.headers['Authorization'] = f'Bearer {self.jwt_token}'
        try:
            response = requests.post(f"{self.base_url}/{endpoint}", json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            return None

    def upsert(self, id, vectors, int_field, index_type):
        payload = {
            "id": id,
            "vectors": vectors,
            "int_field": int_field,
            "indexType": index_type
        }
        return self._send_request("upsert", payload)

    def search(self, vectors, k, index_type, field_name, value, op):
        payload = {
            "vectors": vectors,
            "k": k,
            "indexType": index_type,
            "filter": {
                "fieldName": field_name,
                "value": value,
                "op": op
            }
        }
        return self._send_request("search", payload)
