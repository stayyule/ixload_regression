import pytest
import logging
import requests
import json
import time


class TestTencent:

    def wait_success(self, api_server, location):
        headers = {
            'content-type': 'application/json'
        }
        # url = api_server + ret.headers["Location"]
        url = api_server + location
        result = self.session.get(url, headers=headers, verify=False)

        while result.json()["state"] != "SUCCESS":
            if result.json()['state'] == 'ERROR':
                break
            time.sleep(5)
            result = self.session.get(url, headers=headers, verify=False)

    @pytest.fixture
    def logger(self):
        return logging.getLogger()

    @pytest.fixture
    def api_server(self):
        self.server = 'http://127.0.0.1:8080'
        return self.server

    @pytest.fixture
    def headers(self):
        self.headers = {
            'content-type': 'application/json'
        }
        return self.headers

    @pytest.fixture
    def session(self, logger, api_server, headers):
        # http request session
        self.session = requests.session()
        # linux optional
        # session.mount('https://', TlsAdapter())

        url = api_server + '/api/v1/sessions'
        body = {
            "applicationVersion": "9.30.115.98"
        }
        ret = self.session.post(url, headers=headers, data=json.dumps(body))
        self.session_id = ret.headers["Location"]
        logger.info(f'session id:{self.session_id}')

        url = api_server + self.session_id + "/operations/start"
        ret = self.session.post(url, headers=headers, verify=False)
        self.wait_success(api_server, ret.headers['Location'])

    @pytest.mark.parametrize('protocol', ['http', 'https', 'http2', 'http3'])
    @pytest.mark.parametrize('file_size', ['4K', '16K', '1M'])
    @pytest.mark.parametrize('objective', ['cps', 'cc', 'qps'])
    @pytest.mark.parametrize('req_type', ['get', 'post'])
    def test_one_arm(self, protocol, file_size, objective, req_type, api_server, session):

        if protocol == 'http':
            # psudo code
            # load_config('http1.rxf')
            pass
        if protocol == 'https':
            pass
        if protocol == 'http2':
            pass

    @pytest.mark.parametrize('protocol', ['http', 'https', 'http2'])
    @pytest.mark.parametrize('file_size', ['4K', '16K', '1M'])
    @pytest.mark.parametrize('objective', ['cps', 'cc', 'qps'])
    @pytest.mark.parametrize('req_type', ['get', 'post'])
    def test_2_arm(self, protocol, file_size, objective, req_type, api_server, logger, session):
        logger.info(api_server)

    def setup_method(self):
        logging.getLogger().info('setup')
        return

    def teardown_method(self):
        logging.getLogger().info('teardown')
        url = self.server + "/api/v1/sessions/"
        self.session.delete(url, headers=self.headers, verify=False)
        return
