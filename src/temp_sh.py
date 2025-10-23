import os
import requests
import loguru

class TempSh():
    def upload(self):
        for filename in os.listdir('out/'):
            loguru.logger.info(f'Uploading {filename} to temp.sh ...')

            files = {
                'file': open(f'out/{filename}', 'rb'),
            }

            response = requests.post('https://temp.sh/upload', files=files)
            final_url = response.text

            loguru.logger.info(f'\n\nUploaded: {filename} to {final_url}')
