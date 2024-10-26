import sys
import os
import unittest
import json
from unittest.mock import patch, MagicMock
# Add the path to the sys.path for execute 
# python /tests/emotion_test.py in the root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lambda_function.index import lambda_handler
from data import BodyResponse


class TestByCategory(unittest.TestCase):
    @patch('lambda_function.index.DYNAMODB_TABLE.scan')
    def test_lambda_handler(self, mock_scan):
        
        mock_scan.return_value = {
            'Items': [
            {
                'actionName': 'AZURECreateLandingZoneArguments',
                'category': 'Networking'
            },
            {
                'actionName': 'AWSTemplateVpcProdArguments',
                'category': 'Networking'
            },
            {
                'actionName': 'GCPCreateNetworkFullArguments',
                'category': 'Networking'
            },
            {
                'actionName': 'AZURECreateVnetNonProdArguments',
                'category': 'Networking'
            },
            {
                'actionName': 'AWSTemplateVpcNonProd',
                'category': 'Networking'
            },
            {
                'actionName': 'AZURECreateVnetProdArguments',
                'category': 'Networking'
            },
            {
                'actionName': 'AWSCreateLoadBalancerFullArgumentsV2',
                'category': 'Load Balancing'
            },
            {
                'actionName': 'AZURECreateAppGatewayArguments',
                'category': 'Load Balancing'
            },
            {
                'actionName': 'AZURECreateVMArguments',
                'category': 'Compute'
            },
            {
                'actionName': 'AWSTemplateEc2InstanceProdArguments',
                'category': 'Compute'
            },
            {
                'actionName': 'AWSK8SClusterFullArguments',
                'category': 'Containers'
            },
            {
                'actionName': 'AksCreateNonManagedClusterArguments',
                'category': 'Containers'
            },
            {
                'actionName': 'AksCreateManagedClusterArguments',
                'category': 'Containers'
            },
            {
                'actionName': 'AWSK8SNginxServiceFullArguments',
                'category': 'Containers'
            },
            {
                'actionName': '',
                'category': 'DataBase'
            },
            {
                'actionName': '',
                'category': 'DataBase'
            }
            ]
        }

        event = {
            'httpMethod': 'GET',
            'path': '/templates/bycategory'
        }
        response = lambda_handler(event, context=None)

        response_body = json.loads(response['body'])
        expected_body = BodyResponse().get_categories()

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
