from django.test import TestCase, Client
from .views import DATA


class testTopServers(TestCase):
    maxDiff = None  # 获取完整的diff输出

    @classmethod
    def setUpClass(cls):
        DATA.update({
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 6,
            8: 7,
            9: 9,
            10: 12,
            11: 11,
            12: 13,
            13: 14,
            100: 100
        })

    @classmethod
    def tearDownClass(cls):
        DATA.update({})

    def test_api_query_top(self):
        client = Client()
        # 1. success
        data = {
            'client_id': 100,
        }
        response = client.get("/api/top_servers/query_top/",
                              data, content_type='application/json')
        actual = response.json()
        expected = {
            "status": 1,
            "data": [
                {"no": 1, "client_id": 100, "grade": 100},
                {"no": 2, "client_id": 13, "grade": 14},
                {"no": 3, "client_id": 12, "grade": 13},
                {"no": 4, "client_id": 10, "grade": 12},
                {"no": 5, "client_id": 11, "grade": 11},
                {"no": 6, "client_id": 9, "grade": 9},
                {"no": 7, "client_id": 8, "grade": 7},
                {"no": 8, "client_id": 6, "grade": 6},
                {"no": 9, "client_id": 7, "grade": 6},
                {"no": 10, "client_id": 5, "grade": 5}
            ]
        }
        self.assertEqual(expected, actual)

        # 2. client not in top 10
        data = {
            'client_id': 1,
        }
        response = client.get("/api/top_servers/query_top/",
                              data, content_type='application/json')
        actual = response.json()
        expected = {
            "status": 1,
            "data": [
                {"no": 1, "client_id": 100, "grade": 100},
                {"no": 2, "client_id": 13, "grade": 14},
                {"no": 3, "client_id": 12, "grade": 13},
                {"no": 4, "client_id": 10, "grade": 12},
                {"no": 5, "client_id": 11, "grade": 11},
                {"no": 6, "client_id": 9, "grade": 9},
                {"no": 7, "client_id": 8, "grade": 7},
                {"no": 8, "client_id": 6, "grade": 6},
                {"no": 9, "client_id": 7, "grade": 6},
                {"no": 10, "client_id": 5, "grade": 5},
                {"no": 14, "client_id": 1, "grade": 1}
            ]
        }
        self.assertEqual(expected, actual)

    def test_api_upload_success(self):
        # client = Client()
        # 1. success
        data = {
            'client_id': 100,
            'grade': 99
        }
        response = self.client.get("/api/top_servers/upload/",
                                   data, content_type='application/json')
        actual = response.json()
        expected = {
            'status': 1,
            'data': {
                "100": 99
            }
        }
        self.assertEqual(expected, actual)
        self.assertIn(100, DATA)
        self.assertEqual(DATA[data.get('client_id')], data.get('grade'))

    def test_api_upload_field(self):
        # 1. 缺少grade参数
        client = Client()
        data = {
            'client_id': 100
        }
        response = client.get("/api/top_servers/upload/",
                              data, content_type='application/json')
        actual = response.json()
        expected = {
            'status': 0,
            'data': {}
        }
        self.assertEqual(expected, actual)
        # 2. 缺少client_id参数
        client = Client()
        data = {
            'grade': 99
        }
        response = client.get("/api/top_servers/upload/",
                              data, content_type='application/json')
        actual = response.json()
        expected = {
            'status': 0,
            'data': {}
        }
        self.assertEqual(expected, actual)

        # 3. grade参数范围小于
        client = Client()
        data = {
            'client_id': 100,
            'grade': -1
        }
        response = client.get("/api/top_servers/upload/",
                              data, content_type='application/json')
        actual = response.json()
        expected = {
            'status': 0,
            'data': {}
        }
        self.assertEqual(expected, actual)

        # 4. grade参数范围大于
        client = Client()
        data = {
            'client_id': 100,
            'grade': 100000000
        }
        response = client.get("/api/top_servers/upload/",
                              data, content_type='application/json')
        actual = response.json()

        expected = {
            'status': 0,
            'data': {}
        }
        self.assertEqual(expected, actual)

        # 5. grade参数类型
        client = Client()
        data = {
            'client_id': 100,
            'grade': 'two'
        }
        response = client.get("/api/top_servers/upload/",
                              data, content_type='application/json')
        actual = response.json()

        expected = {
            'status': 0,
            'data': {}
        }
        self.assertEqual(expected, actual)
