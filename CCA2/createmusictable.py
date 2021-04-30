import boto3


def createMusicTable(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName='music',
        KeySchema=[
            {
                'AttributeName': 'title',
                'KeyType': 'HASH',
            },
            {
                'AttributeName': 'artist',
                'KeyType': 'RANGE'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'artist',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        })


if __name__ == '__main__':
    createMusicTable()
