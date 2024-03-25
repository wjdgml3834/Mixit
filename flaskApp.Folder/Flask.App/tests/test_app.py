import pytest
import sys
from flask_testing import TestCase
from unittest.mock import patch, MagicMock
sys.path.append('..')
from app import app
import app_config  

class MyTest(TestCase):
    def create_app(self):
        app.config.from_object(app_config)  
        app.config['TESTING'] = True
        return app

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_app_config_loading(self):
        self.assertEqual(app.config['CLIENT_ID'], app_config.CLIENT_ID)
        self.assertEqual(app.config['AUTHORITY'], app_config.AUTHORITY)
        self.assertEqual(app.config['ENDPOINT'], app_config.ENDPOINT)
        
    def test_xss_vulnerability(self):
        malicious_script = "<script>alert('XSS')</script>"
        response = self.client.post('/', data={'input_field': malicious_script})
        self.assertNotIn(malicious_script, response.data.decode())
        
    @patch('requests.get')
    def test_graphcall(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'value': [{'start': {'dateTime': '2023-01-01T12:00:00'}, 'end': {'dateTime': '2023-01-01T13:00:00'}}]}
        mock_get.return_value = mock_response

        with patch('cache._get_token_from_cache', return_value={'access_token': 'fake_token'}):
            response = self.client.get('/graphcall')
            self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    pytest.main()
