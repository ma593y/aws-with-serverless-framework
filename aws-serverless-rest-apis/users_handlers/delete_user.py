import json, boto3, os


def delete_user(user_id):
    try:
        table = boto3.resource('dynamodb').Table(os.getenv('users_table'))
        response = table.delete_item(Key = {'id': user_id})
        return [True, response]
        
    except Exception as e:
        return [False, e]


def lambda_handler(event, context):
    user_id = event['pathParameters']['id']
    if user_id.isnumeric():
        if 'Item' in boto3.resource('dynamodb').Table(os.getenv('users_table')).get_item(Key={'id': user_id}):
            result = delete_user(user_id)
            if result[0]:
                return {
                    "statusCode": 200,
                    "body": json.dumps(
                        {
                            'Message': 'User deleted successfully.',
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
