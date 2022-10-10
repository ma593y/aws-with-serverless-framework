import json, boto3, os


def get_all_users():
    try:
        table = boto3.resource('dynamodb').Table(os.getenv('users_table'))
        response = table.scan()
        return [True, response]
        
    except Exception as e:
        return [False, e]


def lambda_handler(event, context):
    
    result = get_all_users()
    if result[0]:
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    'Message': 'Users fetched successfully.',
                    'Users': sorted(result[1]['Items'], key = lambda item: item['id']),
                    'Count': result[1]['Count'],
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
