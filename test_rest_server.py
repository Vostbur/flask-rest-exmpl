from unittest import TestCase, TestSuite, defaultTestLoader, TextTestRunner


class AMainTestCase(TestCase):
    def test_python_file_exists(self):
        try:
            import rest_server
        except ModuleNotFoundError:
            self.fail('Module rest_server.py not exists')


class BPostPutTestCase(TestCase):
    def test_create_task(self):
        import requests
        result = requests.post('http://localhost:5000/todo/api/v1.0/tasks',
                               json={'title': 'test task'})
        self.assertEqual(result.status_code, 201)

    def test_update_done_field_task(self):
        import requests
        result = requests.put('http://localhost:5000/todo/api/v1.0/tasks/1',
                              json={'done': True})
        self.assertEqual(result.status_code, 200)

    def test_update_bad_request(self):
        import requests
        result = requests.put('http://localhost:5000/todo/api/v1.0/tasks/3',
                              json={'done': 'True'})
        self.assertEqual(result.status_code, 404)


class CGetTestCase(TestCase):
    def test_get_tasks(self):
        import requests
        result = requests.get('http://localhost:5000/todo/api/v1.0/tasks')
        self.assertEqual(result.status_code, 200)

    def test_get_task(self):
        import requests
        result = requests.get('http://localhost:5000/todo/api/v1.0/tasks/1')
        self.assertEqual(result.status_code, 200)

    def test_get_not_exists_task(self):
        import json
        import requests
        result = requests.get('http://localhost:5000/todo/api/v1.0/tasks/100')
        self.assertEqual(json.loads(result.text), {'error': 'Not found'})


class DDeleteTestCase(TestCase):
    def test_delete_task(self):
        import requests
        result = requests.delete('http://localhost:5000/todo/api/v1.0/tasks/1')
        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    suite = list()
    suite.append(defaultTestLoader.loadTestsFromTestCase(AMainTestCase))
    suite.append(defaultTestLoader.loadTestsFromTestCase(BPostPutTestCase))
    suite.append(defaultTestLoader.loadTestsFromTestCase(CGetTestCase))
    suite.append(defaultTestLoader.loadTestsFromTestCase(DDeleteTestCase))

    todoTestSuite = TestSuite()
    todoTestSuite.addTests(suite)

    runner = TextTestRunner(verbosity=2)
    runner.run(todoTestSuite)
