# Farsali

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## Installation

Se necesita tener instalado [Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-es)
Se necesita tener instalado [Docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-es)

Una vez instalado para ejecutar el proyecto se ejecuta el siguiente comando

```sh
sudo docker-compose build -> Esto instalara todas las dependencias
sudo docker-compose up -> Esto ejecutara el proyecto
```

Comandos Extra

```sh
sudo docker-compose run backend python manage.py makemigrations  -> Para generar migraciones
sudo docker-compose run backend python manage.py createsuperuser -> Para crear superuser
sudo docker-compose run backend python manage.py shell           -> Para hacer debug en consola
```

## Release

Una vez realizado los cambios con exito sehace push como normalmente se hace
Con la diferencia que una vez la branch este actualizada se ejecutaran los siguientes comandos.

```sh
heroku login
heroku container:login
heroku container:push web -a farsalicol -> para guardar la imagen nueva en heroku
heroku container:release web -a farsalicol -> para hacer el release a prod
```

Verificar que el proyecto una vez ejecutado ingrese exitosamente a la url

```sh
127.0.0.1:8000
```

## Notas

Como el proyecto se guarda en contenedores cada contenedor tiene su propia ip, así que hay que tener cuidado con la configuraciones extras, apuntando bien:

```sh
"""EXAMPLE"""

EC2_PRIVATE_IP = None
"""Fixes the IP issues on aws ECS"""
try:
    resp = requests.get('http://169.254.170.2/v2/metadata')
    data = resp.json()
    container_name = 'api'  # If stored in environment os.environ.get('DOCKER_CONTAINER_NAME', None)
    search_results = [x for x in data['Containers'] if x['Name'] == container_name]
    if len(search_results) > 0:
        container_meta = search_results[0]
    else:
        # Fall back to the pause container
        container_meta = data['Containers'][0]
    EC2_PRIVATE_IP = container_meta['Networks'][0]['IPv4Addresses'][0]
except Exception as e:
    # silently fail as we may not be in an ECS environment
    print('could not get EC2_PRIVATE_IP')
    print(str(e))
if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)
```