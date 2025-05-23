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

    def upsert(self, id, vectors, int_field=None, index_type="FLAT"):
        payload = {
            "id": id,
            "vectors": vectors,
            "indexType": index_type
        }
        if int_field is not None:
            payload["int_field"] = int_field

        return self._send_request("upsert", payload)

    def search(self, vectors, k, index_type="FLAT", field_name=None, value=None, op=None):
        payload = {
            "vectors": vectors,
            "k": k,
            "indexType": index_type
        }
        if field_name is not None and value is not None and op is not None:
            payload["filter"] = {
                "fieldName": field_name,
                "value": value,
                "op": op
            }

        return self._send_request("search", payload)
