import datetime
import configparser
from base64 import b64decode
import webbrowser
import openai
from openai.error import InvalidRequestError

def generate_image(prompt, num_image=1, size='512x512', output_format='url'):
    """
    params:
        prompt (str):
        num_image (int):
        size (str):
        output_format (str):
    """
    try:
        images = []
        response = openai.Image.create(
            prompt=prompt,
            n=num_image,
            size=size,
            response_format=output_format
        )
        if output_format == 'url':
            for image in response['data']:
                images.append(image.url)
        elif output_format == 'b64_json':
            for image in response['data']:
                images.append(image.b64_json)
        return {'created': datetime.datetime.fromtimestamp(response['created']), 'images': images}
    except InvalidRequestError as e:
        print(e)

config = configparser.ConfigParser() 
config.read('creation.ini')
API_KEY = config['openai']['APIKEY']

openai.api_key = API_KEY

SIZES = ('1024x1024', '512x512', '256x256')

# generate images (url outputs)
response = generate_image('The National Emblem of Saudi Arabia Crest', num_image=10, size=SIZES[0])
response['created']
images = response['images']
for image in images:
    webbrowser.open(image)

## generate images (byte output)
response = generate_image('The National Emblem of Saudi Arabia Crest', num_image=20, size=SIZES[1], output_format='b64_json')
prefix = 'demo'
for indx, image in enumerate(response['images']):
    with open(f'{prefix}_{indx}.jpg', 'wb') as f:
        f.write(b64decode(image))