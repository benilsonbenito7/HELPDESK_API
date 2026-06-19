from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from .controllers.user_controller import router

api = NinjaExtraAPI()

api.register_controllers(NinjaJWTDefaultController)
api.add_router("v1/", router)