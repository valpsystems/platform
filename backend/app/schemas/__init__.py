from .career import CareerRequest, CareerResponse
from .common import ErrorResponse, ValidationErrorResponse
from .contact import ContactRequest, ContactResponse
from .feedback import FeedbackRequest, FeedbackResponse
from .health import HealthResponse
from .newsletter import NewsletterRequest, NewsletterResponse
from .quote import QuoteRequest, QuoteResponse
from .resource import ResourceRequest, ResourceResponse
from .service import ServiceRequest, ServiceResponse
from .solution import SolutionRequest, SolutionResponse
from .technology import TechnologyRequest, TechnologyResponse

from .auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
    ProfileResponse,
    UserResponse,
)

__all__ = [
    "HealthResponse",
    "ContactRequest",
    "ContactResponse",
    "NewsletterRequest",
    "NewsletterResponse",
    "CareerRequest",
    "CareerResponse",
    "QuoteRequest",
    "QuoteResponse",
    "FeedbackRequest",
    "FeedbackResponse",
    "TechnologyRequest",
    "TechnologyResponse",
    "ServiceRequest",
    "ServiceResponse",
    "SolutionRequest",
    "SolutionResponse",
    "ResourceRequest",
    "ResourceResponse",
    "ErrorResponse",
    "ValidationErrorResponse",
    "LoginRequest",
    "LoginResponse",
    "RegisterRequest",
    "RegisterResponse",
    "ChangePasswordRequest",
    "ForgotPasswordRequest",
    "ResetPasswordRequest",
    "VerifyEmailRequest",
    "ProfileResponse",
    "UserResponse",
]
