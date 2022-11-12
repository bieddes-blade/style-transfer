import requests

response = {"url":"https://storage.yandexcloud.net/upload-bucket-hw7","fields":{"key":"6563.jpg","AWSAccessKeyId":"nKRSTJ2RtVi5adaSim-_","policy":"eyJleHBpcmF0aW9uIjogIjIwMjEtMDMtMjlUMDA6MzE6MzZaIiwgImNvbmRpdGlvbnMiOiBbeyJidWNrZXQiOiAidXBsb2FkLWJ1Y2tldC1odzcifSwgeyJrZXkiOiAiNjU2My5qcGcifV19","signature":"DmfXJVxuKTBerRTdUB+LPREQFbU="}}

name = response['fields']['key']

with open('/Users/clarence/Desktop/' + name, 'rb') as f:
    files = {'file': (name, f)}
    http_response = requests.post(response['url'], data=response['fields'], files=files)