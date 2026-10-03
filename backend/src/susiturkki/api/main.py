from susiturkki.api.factory import create_app
from susiturkki.infrastructure.settings import load_settings

app = create_app(load_settings())
