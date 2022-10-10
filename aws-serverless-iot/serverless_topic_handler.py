import json, boto3


def publish_serverless_topic_data(data):
    mqtt_client = boto3.client('iot-data')

    response = mqtt_client.publish(
        topic='tempAdnanTopic',
        payload="it worked... yayyyy\n" + (json.dumps(data, indent=5))
    )


def lambda_handler(event, context):
    publish_serverless_topic_data(event)
    
    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                'Message': 'Hello from Lambda!',
            }
        )
    }
