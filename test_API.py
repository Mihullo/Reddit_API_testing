import unittest
import requests
import requests.auth as auth

'''Global variables'''
BASE_URL_NO_AUTH = 'https://www.reddit.com'
PERSONAL_ID = 'zQpVbSN7IQ7YcjOcxKMDaw'
SECRET_TOKEN = '9gLP0XqaRkfdlO5LXV3fOSexpDnEeA'
ACCESS_TOKEN = 'api/v1/access_token'
BASE_URL = 'https://oauth.reddit.com'
HEADERS = {'user-agent': 'MyTestScript by For_test_API'}
USER_DATA = {'grant_type': 'password',
             'username': 'For_test_API',
             'password': '1qaz@WSX'}
TROPHIES = ['Verified Email', 'New User']

HTTP_STATUS_OK = 200
HTTP_STATUS_NOT_FOUND = 404


class TestRedditAPI(unittest.TestCase):

    def test_1_auth(self):
        """Checking request a temporary OAuth token from Reddit"""
        global HEADERS
        auth_request = auth.HTTPBasicAuth(PERSONAL_ID, SECRET_TOKEN)
        request_token = requests.post(f'{BASE_URL_NO_AUTH}/{ACCESS_TOKEN}',
                                      auth=auth_request, data=USER_DATA, headers=HEADERS)
        self.assertEqual(request_token.status_code, HTTP_STATUS_OK, 'Token not received!')
        token = request_token.json()['access_token']
        HEADERS = {**HEADERS, 'Authorization': f'bearer {token}'}

    def test_2_account(self):
        """Checking account actions"""
        ident = requests.get(f'{BASE_URL}/api/v1/me', headers=HEADERS)
        self.assertEqual(ident.status_code, HTTP_STATUS_OK, 'Identification failed!')
        self.assertEqual(ident.json()['name'], USER_DATA['username'], 'The user\'s name does not match!')

        friends = requests.get(f'{BASE_URL}/api/v1/me/friends', headers=HEADERS)
        self.assertEqual(friends.status_code, HTTP_STATUS_OK, 'Request error!')
        self.assertTrue(friends.json()['kind'] and friends.json()['data'], 'The data format does not match!')
        self.assertTrue(friends.json()['data'], 'No data available!')

        karma = requests.get(f'{BASE_URL}/api/v1/me/karma', headers=HEADERS)
        self.assertEqual(karma.status_code, HTTP_STATUS_OK, 'Request error!')
        self.assertEqual(karma.json()['kind'], 'KarmaList', 'The title does not match!')

        trophies = requests.get(f'{BASE_URL}/api/v1/me/trophies', headers=HEADERS)
        self.assertEqual(trophies.status_code, HTTP_STATUS_OK, 'Request error!')
        self.assertEqual(trophies.json()['kind'], 'TrophyList', 'The title does not match!')
        for i in trophies.json()['data']['trophies']:
            self.assertIn(i['data']['name'], TROPHIES, f'{i["data"]["name"]} is not in the TrophyList')
