# flake8: noqa

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

import simple
from .base import *


# sentry_sdk.init(
#     dsn=config("SENTRY_DSN", default=""),
#     environment=SIMPLE_ENVIRONMENT,
#     release="simple@%s" % simple.__version__,
#     integrations=[DjangoIntegration()],
# )