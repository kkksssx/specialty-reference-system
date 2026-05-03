from aiogram import Dispatcher

from .start import router as start_router
from .help import router as help_router
from .applicant import router as applicant_router
from .student import router as student_router
from .teacher import router as teacher_router
from .discipline import router as discipline_router
from .common import router as common_router


def register_all_routers(dp: Dispatcher) -> None:
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(applicant_router)
    dp.include_router(student_router)
    dp.include_router(teacher_router)
    dp.include_router(discipline_router)
    dp.include_router(common_router)