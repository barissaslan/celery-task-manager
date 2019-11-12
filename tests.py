import unittest
from test.support import EnvironmentVarGuard
from unittest import mock


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.env = EnvironmentVarGuard()
        self.env.set('CELERY_BROKER_URL',
                     'amqp://pyizcpcy:i8-DLpC9lKVReHWD0--fNDPT_QOJzNCJ@orangutan.rmq.cloudamqp.com/pyizcpcy')

        self.env.set('CALLBACK_URL',
                     'http://127.0.0.1:8080/callback/{}')

    @mock.patch('requests.get')
    def test_multiply(self, mock_get):
        with self.env:
            from app import multiply
            res = multiply(2, 3)
            self.assertDictEqual(res, {'result': 6})

    @mock.patch('requests.get')
    def test_multiply_type_error(self, mock_get):
        with self.env:
            from app import multiply, TYPE_ERROR_MESSAGE
            res = multiply("2", "3")
            self.assertDictEqual(res, {'error': TYPE_ERROR_MESSAGE.format("2", "3")})


if __name__ == '__main__':
    unittest.main()
