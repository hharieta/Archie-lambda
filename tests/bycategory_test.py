import sys
import os
import unittest
import json
from unittest.mock import patch, MagicMock
# Add the path to the sys.path for execute 
# python /tests/*_test.py in the root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lambda_function.index import lambda_handler
from data import BodyTestResponse, BodyMockResponse



class TestByCategory(unittest.TestCase):
    @patch('lambda_function.index.DYNAMODB_TABLE.scan')
    def test_lambda_handler(self, mock_scan):
        
        mock_scan.return_value = BodyMockResponse().get_scan()

        event = {
            'httpMethod': 'GET',
            'path': '/templates/bycategory'
        }
        response = lambda_handler(event, context=None)

        response_body = json.loads(response['body'])
        expected_body = BodyTestResponse().get_categories()

        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(
            response_body,
            expected_body
            )
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        self.assertEqual(response['headers']['Access-Control-Allow-Origin'], '*')

def main():
    unittest.main()

if __name__ == '__main__':
    main()
