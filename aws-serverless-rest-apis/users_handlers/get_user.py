import json, boto3, os


def get_user(user_id):
    try:
        table = boto3.resource('dynamodb').Table(os.getenv('users_table'))
        response = table.get_item(Key={'id': user_id})
        return [True, response]
        
    except Exception as e:
        return [False, e]


def lambda_handler(event, context):
    user_id = event['pathParameters']['id']
    if user_id.isnumeric():
        result = get_user(user_id)
        if result[0] and 'Item' in result[1]:
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        'Message': 'User fetched successfully.',
                        'User': result[1]['Item'],
                    }
                )
            }
            
        elif result[0] and 'Item' not in result[1]:
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        'Message': 'User does not exists.'
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
                    'Message': 'Invalid user id.',
                }
            )
        }
