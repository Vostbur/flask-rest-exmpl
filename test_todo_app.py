from unittest import TestCase, TestSuite, defaultTestLoader, TextTestRunner

# HTTPBasicAuth settings
USERNAME = 'alex'
PASSWORD = 'python'


class AMainTestCase(TestCase):
    def test_python_file_exists(self):
        try:
            import todo_app
        except ModuleNotFoundError:
            self.fail('Module todo_app.py not exists')


class BGetTestCase(TestCase):
    def test_get_tasks(self):
        import requests
        from requests.auth import HTTPBasicAuth
        result = requests.get('http://localhost:5000/todo/api/v1.0/tasks',
                              auth=HTTPBasicAuth(USERNAME, PASSWORD))
        self.assertEqual(result.status_code, 200)

    def test_get_task(self):
        import requests
        from requests.auth import HTTPBasicAuth
        result = requests.get('http://localhost:5000/todo/api/v1.0/tasks/1',
                              auth=HTTPBasicAuth(USERNAME, PASSWORD))
        self.assertEqual(result.status_code, 200)

    def test_get_not_exists_task(self):
        import json
        import requests
        from requests.auth import HTTPBasicAuth
        result = requests.get('http://localhost:5000/todo/api/v1.0/tasks/100',
                              auth=HTTPBasicAuth(USERNAME, PASSWORD))
        self.assertEqual(json.loads(result.text), {'error': 'Not found'})


class CPostPutTestCase(TestCase):
    def test_create_task(self):
        import requests
        from requests.auth import HTTPBasicAuth
        result = requests.post('http://localhost:5000/todo/api/v1.0/tasks',
                               json={'title': 'test task'},
                               auth=HTTPBasicAuth(USERNAME, PASSWORD))
        self.assertEqual(result.status_code, 201)

    def test_update_title_task(self):
        import requests
        from requests.auth import HTTPBasicAuth
        result = requests.put('http://localhost:5000/todo/api/v1.0/tasks/3',
                              json={'title': 'update test task'},
                              auth=HTTPBasicAuth(USERNAME, PASSWORD))
        self.assertEqual(result.status_code, 200)

    def test_update_description_task(self):
        import requests
        from requests.auth import HTTPBasicAuth
        result = requests.put('http://localhost:5000/todo/api/v1.0/tasks/3',
                              json={'description': 'update desc'},
                              auth=HTTPBasicAuth(USERNAME, PASSWORD))
        self.assertEqual(result.status_code, 200)

    def test_update_done_field_task(self):
        import requests
        from requests.auth import HTTPBasicAuth
        result = requests.put('http://localhost:5000/todo/api/v1.0/tasks/3',
                              json={'done': True},
                              auth=HTTPBasicAuth(USERNAME, PASSWORD))
        self.assertEqual(result.status_code, 200)

    def test_update_bad_request(self):
        import requests
        from requests.auth import HTTPBasicAuth
        result = requests.put('http://localhost:5000/todo/api/v1.0/tasks/3',
                              json={'done': 'True'},
                              auth=HTTPBasicAuth(USERNAME, PASSWORD))
        self.assertEqual(result.status_code, 400)


class DDeleteTestCase(TestCase):
    def test_delete_task(self):
        import requests
        from requests.auth import HTTPBasicAuth
        result = requests.delete('http://localhost:5000/todo/api/v1.0/tasks/3',
                                 auth=HTTPBasicAuth(USERNAME, PASSWORD))
        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    suite = list()
    suite.append(defaultTestLoader.loadTestsFromTestCase(AMainTestCase))
    suite.append(defaultTestLoader.loadTestsFromTestCase(BGetTestCase))
    suite.append(defaultTestLoader.loadTestsFromTestCase(CPostPutTestCase))
    suite.append(defaultTestLoader.loadTestsFromTestCase(DDeleteTestCase))

    todoTestSuite = TestSuite()
    todoTestSuite.addTests(suite)

    runner = TextTestRunner(verbosity=2)
    runner.run(todoTestSuite)
