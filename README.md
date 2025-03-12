# [Paykassma](https://paykassma.com/) gateway module for [Fleio](https://fleio.com)

## Introduce

This module was developed by the [Fotbo](https://fotbo.com) team and is designed for integrating the Paykassma payment method into Fleio.

- Paykassma - Payment Gateway.
- The Fleio OpenStack Edition - billing system and self-service portal software - enables service providers to sell public cloud services.

## Getting started

First, it is necessary to clone the project and integrate the module into Fleio. For the integration, we will be using a custom Dockerfile.

1. Clone project.
```sh
git clone git@github.com:fotbo/paykassma-gateway-module.git
```

2. Now you need to add custom code into Docker. For example, you can achieve this as follows:

```dockerfile
# define the build arguments that are used below to reference the base Docker backend image
ARG FLEIO_DOCKER_HUB
ARG FLEIO_RELEASE_SUFFIX

FROM ${FLEIO_DOCKER_HUB}/fleio_backend${FLEIO_RELEASE_SUFFIX}

ENV INSTALLED_PATH="/var/webapps/fleio/project/fleio"

COPY --chown=fleio:fleio paykassma-gateway-module $INSTALLED_PATH/billing/gateways/paykassma
```

More information at the [link](https://fleio.com/docs/2024.01/developer/add-change-docker-files.html)

3. After this, you need to add configurations in the `settings.py` file.
```sh
fleio edit settings.py
```

4. And put settings.
```python
# >>> Paykassma 

INSTALLED_APPS += ('fleio.billing.gateways.paykassma', )

PAYKASSMA_SETTINGS = {
    'api_key': '{api_key}',
    'return_url': '{callback_url}',
    'api_url': '{api_url}',
    'webhook_id': {webhook_id},
    'webhook_private_key': '{webhook_private_key}'
}

# >>> FASTFOREX for exchange rates
FASTFOREX_API_KEY = '{fastforex_api_key}'
FASTFOREX_API_URL = '{fastforex_api_url}'
```

Save and restart Fleio.
After restarting, you will have the option to enable the module for users in the graphical interface.
