import json, boto3, os


def update_user(user_id, data):
    try:
        table = boto3.resource('dynamodb').Table(os.getenv('users_table'))
        response = table.update_item(
            Key={
                'id': user_id
            },
            ExpressionAttributeNames={
                '#email': 'email',
                '#name': 'name',
                '#phone': 'phone'
            },
            ExpressionAttributeValues={
                ':val1': data['email'],
                ':val2': data['name'],
                ':val3': data['phone']
            },
            UpdateExpression='SET #email = :val1, #name = :val2, #phone = :val3'
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
    
    if 'email' not in body or 'name' not in body or 'phone' not in body:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    'Message': 'Email, name or phone is missing.',
                }
            )
        }
        
    
    user_id = event['pathParameters']['id']
    if user_id.isnumeric():
        if 'Item' in boto3.resource('dynamodb').Table(os.getenv('users_table')).get_item(Key={'id': user_id}):
            result = update_user(user_id, body)
            if result[0]:
                return {
                    "statusCode": 200,
                    "body": json.dumps(
                        {
                            'Message': 'User updated successfully.',
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
                        'Message': 'User does not exists.',
                    }
                )
            }    
    else:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    'Message': 'Invalid user id.',
                }
            )
        }
