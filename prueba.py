import requests

# declara el API a consumir
req_url = "https://api.kieroapi.net/variations/product_global/4559254"
headersList = {}
payload = {}

# Obtener valores del api para construir la plantilla
response = requests.get(req_url, data=payload, headers=headersList)
data = response.json()
if response.status_code == 200 and 'data' in data:
    data_render = data['data']
    breadcum = ""
    for bread in data_render['breadcum']:
        breadcum = breadcum + bread['name'] + "/"
    print(breadcum.strip("/"))
