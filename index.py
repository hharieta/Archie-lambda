from os import getenv
from decimal import Decimal
from typing import Any, List, Dict
from json import JSONEncoder, dumps as json_dumps
from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

TABLE_NAME = getenv('TableName')
DYNAMODB = resource('dynamodb')
DYNAMODB_TABLE = DYNAMODB.Table(TABLE_NAME)

class DecimalEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Decimal):
            if o % 1 == 0:
                return int(o)
            else:
                return float(o)            
        return super(DecimalEncoder, self).default(o)


def build_response(status_code, body) -> Dict[str, Any]:
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json_dumps(body, cls=DecimalEncoder)
    }


def scan_db_records(params: Dict[str, Any], item: List[Any]) -> List[Dict[str, Any]]:
    response = DYNAMODB_TABLE.scan(**params)
    item.extend(response.get('Items', []))

    if 'LastEvaluatedKey' in response:
        params['ExclusiveStartKey'] = response['LastEvaluatedKey']
        return scan_db_records(params, item)
    else:
        print('Items:', item)
        return item


### CRUD operations ###
def get_template_category(event: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if event['queryStringParameters'].get('category'):
            scan_params = {
                'TableName': DYNAMODB_TABLE.name,
                'FilterExpression': Attr('category').eq(event['queryStringParameters']['category'])
            }

        items = scan_db_records(scan_params, [])
        return build_response(200, items)
    except ClientError as e:
        print(e)
        return build_response(400, e.response['Error']['Message'])


def get_latest_templates(event) -> Dict[str, Any]:
    try:
        response = DYNAMODB_TABLE.scan()
        items = sorted(response['Items'], key=lambda x: x['dateAdded'], reverse=True )[:12]
        print('Items:', items)
        return build_response(200, items)
    except ClientError as e:
        print(e)
        return build_response(403, e.response['Error']['Message'])


def get_templates(event) -> Dict[str, Any]:
    try:
        if event.get('queryStringParameters'):
            query_params = event['queryStringParameters']
            if query_params.get('provider'):
                provider = query_params.get('provider').strip()
                scan_params = {
                    'TableName': DYNAMODB_TABLE.name,
                    'FilterExpression': Attr('cloud').eq(provider.upper())
                }
        else:
            scan_params = {'TableName': DYNAMODB_TABLE.name}

        items = scan_db_records(scan_params, [])
        return build_response(200, items)

    except ClientError as e:
        print(f"ClientError: {e}")
        return build_response(403, e.response['Error']['Message'])
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return build_response(500, str(e))



router = {
    '/status': {
        'GET': lambda event: build_response(200, {'status': 'OK. API is up and running'})
    },
    '/templates': {
        'GET': lambda event: get_templates(event)
    },
    '/templates/latest': {
        'GET': lambda event: get_latest_templates(event)
    },
    '/templates/category': {
        'GET': lambda event: get_template_category(event)
    }
}

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    print('Request event:', event)
    print('Request context:', context)
    response = None

    try:
        http_method = event.get('httpMethod')
        path = event.get('path')

        if path in router and http_method in router[path]:
            print(f'{http_method} {path}')
            response = router[path][http_method](event)
        else:
            response = build_response(405, 'Method Not Allowed')
        
    except Exception as e:
        print('Error', e)
        response = build_response(401, 'Error processing request')

    return response 
