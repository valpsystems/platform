from fastapi import APIRouter

from .auth.router import router as auth_router
from .careers.router import router as careers_router
from .contact.router import router as contact_router
from .feedback.router import router as feedback_router
from .health.router import router as health_router
from .newsletter.router import router as newsletter_router
from .quote.router import router as quote_router

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(auth_router)
v1_router.include_router(health_router)
v1_router.include_router(contact_router)
v1_router.include_router(newsletter_router)
v1_router.include_router(careers_router)
v1_router.include_router(quote_router)
v1_router.include_router(feedback_router)

__all__ = ["v1_router"]
