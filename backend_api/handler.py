from mangum import Mangum
from backend_api.main import app

handler = Mangum(app)
