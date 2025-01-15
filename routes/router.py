from flask import Flask


def router(app: Flask):
    from routes.admin import admin_blueprints
    from routes.private import private_blueprints
    from routes.public import public_blueprints

    app.register_blueprint(admin_blueprints)
    app.register_blueprint(private_blueprints)
    app.register_blueprint(public_blueprints)
