
import os
import sys

import requests
from jinja2 import Environment, FileSystemLoader


def main():
    # Capture the second argv
    id_product = sys.argv[1]

    # Declare where the template
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('SendZoho.html.j2')

    # Declared API  to used
    req_url = "https://api.kieroapi.net/variations/product_funnel/" + id_product
    headersList = {}
    payload = {}

    # Get values from the API to build the template
    response = requests.get(req_url, data=payload, headers=headersList)

    # Convert response to JSON
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
        # Crear el breadcrumb
        breadcrumb = ""
        for bread in data['data']['breadcum']:
            breadcrumb = breadcrumb + bread['name'] + "/"
        data_render['breadcrumb'] = breadcrumb.strip("/")
        # Mandar los datos y construir los datos
        output = template.render(data=data_render)
        # Declara donde generar el HTML
        filename = f"build/SendZoho-{id_product}.html"
        if not os.path.exists("build"):
            os.makedirs("build")
        with open(filename, 'w') as f:
            f.write(output)
            f.close()
    else:
        print(data)


if __name__ == '__main__':
    main()
