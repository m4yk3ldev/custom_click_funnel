import os
import sys

import requests
from jinja2 import Environment, FileSystemLoader


def main():
    # Capturar el ID del product_global
    id_product = sys.argv[1]

    # declarar donde está la plantilla
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('SendZoho.html')

    # declara el API a consumir
    req_url = "https://api.kieroapi.net/variations/product_funnel/" + id_product
    headersList = {}
    payload = {}

    # Obtener valores del api para construir la plantilla
    response = requests.get(req_url, data=payload, headers=headersList)

    # Convertir respuesta del API a JSON
    data = response.json()
    # Hacer la operación siempre que este presente data
    if response.status_code == 200 and 'data' in data:
        data_render = data['data']
        # Truncar la description a solo 254
        data_render['product_description'] = data['data']['product_description'][:254]
        if data['data']['product_description']:
            data_render['active'] = "true"
        else:
            data_render['active'] = "false"
        # Mandar los datos y construir los datos
        output = template.render(data=data_render)
        # declara donde generar el HTML
        filename = f"generada/SendZoho-{id_product}.html"
        if not os.path.exists("generada"):
            os.makedirs("generada")
        with open(filename, 'w') as f:
            f.write(output)
            f.close()
    else:
        print(data)


if __name__ == '__main__':
    main()
