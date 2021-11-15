from flask import Flask

# 1. Create a flask app object that derives settings from a python class / config file /
# or environment variables

# 2. Initialize plugins accessible to any part of our app such as Database, Cache, Authentication

# 3. Import logic that makes the app (subcomponents) such as routes.

# 4. Register blueprints

def create_app():
    """The application factory"""

    app = Flask(__name__)
    app.config.from_object('config.Config')

    with app.app_context():
        from . import routes

        import feature
        app.register_blueprint(feature.feature_blueprint)
        return app
