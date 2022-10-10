import json, boto3, os


def seed_data(count, data):
    try:
        table = boto3.resource('dynamodb').Table(os.getenv('users_table'))
        with table.batch_writer() as batch:
            for x in range(int(count)):
                response = batch.put_item(
                    Item = {
                        'id': str(x),
                        'email': data['email'],
                        'name': data['name'],
                        'phone': data['phone']
                    }
                )
        return [True]
        
    except Exception as e:
        return [False, e]


def clear_data():
    try:
        table = boto3.resource('dynamodb').Table(os.getenv('users_table'))
        scan = table.scan()
        with table.batch_writer() as batch:
            for each in scan['Items']:
                batch.delete_item(
                    Key={
                        'id': each['id']
                    }
                )
        return [True]
        
    except Exception as e:
        return [False, e]


def lambda_handler(event, context):
    
    if event['body'] is not None:
        body = json.loads(event['body'])
        
        if 'action' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps(
                    {
                        "Message": "Action is missing in request body."
                    }
                )
            }
            
        elif body['action'] == 'seed':
            if 'count' not in body or not body['count'].isnumeric():
                return {
                    'statusCode': 400,
                    'body': json.dumps(
                        {
                            "Message": "Count is missing or invalid."
                        }
                    )
                }
                
            result = seed_data(body['count'], body['data'][0])
            if result[0]:
                return {
                    'statusCode': 200,
                    'body': json.dumps(
                        {
                            "Message": "Data seeded successfully."
                        }
                    )
                }
                
            else:
                return {
                    "statusCode": 400,
                    "body": json.dumps(
                        {
                            'Message': 'Something went wrong.',
                            'Exception': str(result[1]),
                        }
                    )
                }
                
        elif body['action'] == 'clear':
            result = clear_data()
            if result[0]:
                return {
                    'statusCode': 200,
                    'body': json.dumps(
                        {
                            "Message": "Data cleared successfully."
                        }
                    )
                }
                
            else:
                return {
                    "statusCode": 400,
                    "body": json.dumps(
                        {
                            'Message': 'Something went wrong.',
                            'Exception': str(result[1]),
                        }
                    )
                }
            
        else:
            return {
                'statusCode': 400,
                'body': json.dumps(
                    {
                        "Message": "Action is not supported."
                    }
                )
            }
        
    else:
        return {
            'statusCode': 400,
            'body': json.dumps(
                {
                    "Message": "Request body is missing."
                }
            )
        }
