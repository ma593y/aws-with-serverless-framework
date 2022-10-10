import json, boto3


def publish_trigger_data(data):
    mqtt_client = boto3.client('iot-data')

    response = mqtt_client.publish(
        topic='tempAdnanTopic',
        payload="the trigger worked... yayyyy\n" + (json.dumps(data, indent=5))
    )


def lambda_handler(event, context):
    publish_trigger_data(event)
    
    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                'Message': 'Hello from Lambda!',
            }
        )
    }
