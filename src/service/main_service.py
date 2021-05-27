# ####main_service.py
from service.metadata_service import app
from service.view_service import app_view
from httpserver import httpserver

app1 = httpserver.getApp()

app1.register_blueprint(app)
app1.register_blueprint(app_view)

# @app1.route("/")
# def hello():
#     return "Hello World!"

if __name__ == "__main__":
    httpserver.startWebServer()
