from .base_command_handler import router as base_command_router
from .call_back_handler import router as call_back_router
from .command_handler import *

routers = [
    base_command_router,
    call_back_router,
    admin_router,
    engineer_router,
    professor_router,
]
