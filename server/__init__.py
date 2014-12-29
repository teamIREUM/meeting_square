def setup(app):
    import models
    models.setup(app)

    import views.user
    views.user.setup(app)
