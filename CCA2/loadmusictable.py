from decimal import Decimal
import json
import boto3

def load_music(music, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('music')
    for song in music:
        title = song['title']
        artist = song['artist']
        year = song['year']
        web_url = song['web_url']
        image_url = song['img_url']
        print('Adding music:', title, artist, year, web_url, image_url)
        table.put_item(Item=song)

if __name__ == '__main__':
    with open('a2.json') as json_file:
        music_table = json.load(json_file, parse_float=Decimal)
    load_music(music_table['songs'])
