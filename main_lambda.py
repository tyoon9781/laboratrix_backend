from app import app
from mangum import Mangum

hanlder = Mangum(app)
