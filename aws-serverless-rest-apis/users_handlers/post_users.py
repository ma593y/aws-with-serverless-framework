import json, boto3, os


def create_user(data):
    try:
        table = boto3.resource('dynamodb').Table(os.getenv('users_table'))
        response = table.put_item(
            Item = {
                'id': data['id'],
                'email': data['email'],
                'name': data['name'],
                'phone': data['phone']
            }
        )
        return [True, response]
        
    except Exception as e:
        return [False, e]


def lambda_handler(event, context):
    if event['body'] is not None:
        body = json.loads(event['body'])
        
    else:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    'Message': 'Request body is missing.',
                }
            )
        }
    
    if 'id' not in body or 'email' not in body or 'name' not in body or 'phone' not in body:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    'Message': 'Id, email, name or phone is missing.',
                }
            )
        }
        
    if 'Item' not in boto3.resource('dynamodb').Table(os.getenv('users_table')).get_item(Key={'id': body['id']}):
        result = create_user(body)
        if result[0]:
            return {
                "statusCode": 201,
                "body": json.dumps(
                    {
                        'Message': 'User created successfully.',
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
            "statusCode": 400,
            "body": json.dumps(
                {
                    'Message': 'User already exists.',
                }
            )
        }
