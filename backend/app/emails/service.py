from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.config import settings
from app.utils.logger import app_logger


class EmailService:
    def __init__(self) -> None:
        self.template_dir = settings.EMAIL_TEMPLATES_DIR
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )

    async def send_email(
        self,
        to_email: str,
        subject: str,
        template_name: str,
        context: dict[str, Any] | None = None,
    ) -> bool:
        if not settings.SMTP_HOST:
            app_logger.warning("SMTP not configured, skipping email send")
            return False

        try:
            template = self.env.get_template(template_name)
            html_content = template.render(**(context or {}))

            msg = MIMEMultipart("alternative")
            msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_USE_TLS:
                    server.starttls()
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            app_logger.info("Email sent successfully", to=to_email, subject=subject, template=template_name)
            return True

        except Exception:
            app_logger.exception("Failed to send email", to=to_email, subject=subject, template=template_name)
            return False

    async def send_contact_notification(
        self,
        name: str,
        email: str,
        company: str,
        phone: str,
        message: str,
    ) -> bool:
        return await self.send_email(
            to_email=settings.SMTP_FROM_EMAIL,
            subject=f"New Contact Request from {name}",
            template_name="contact.html",
            context={
                "name": name,
                "email": email,
                "company": company,
                "phone": phone,
                "message": message,
                "company_name": settings.APP_NAME,
            },
        )

    async def send_newsletter_confirmation(self, email: str, name: str) -> bool:
        return await self.send_email(
            to_email=email,
            subject="Welcome to VALP SYSTEMS Newsletter",
            template_name="newsletter.html",
            context={
                "name": name,
                "email": email,
                "company_name": settings.APP_NAME,
            },
        )

    async def send_career_application(
        self,
        name: str,
        email: str,
        position: str,
        phone: str,
        experience_years: int | None,
        cover_letter: str,
        linkedin_url: str,
        portfolio_url: str,
    ) -> bool:
        return await self.send_email(
            to_email=settings.SMTP_FROM_EMAIL,
            subject=f"New Job Application for {position} from {name}",
            template_name="career.html",
            context={
                "name": name,
                "email": email,
                "position": position,
                "phone": phone,
                "experience_years": experience_years,
                "cover_letter": cover_letter,
                "linkedin_url": linkedin_url,
                "portfolio_url": portfolio_url,
                "company_name": settings.APP_NAME,
            },
        )

    async def send_quote_notification(
        self,
        name: str,
        email: str,
        company: str,
        phone: str,
        service: str,
        project_description: str,
        budget_range: str,
        timeline: str,
    ) -> bool:
        return await self.send_email(
            to_email=settings.SMTP_FROM_EMAIL,
            subject=f"New Quote Request from {name} for {service}",
            template_name="quote.html",
            context={
                "name": name,
                "email": email,
                "company": company,
                "phone": phone,
                "service": service,
                "project_description": project_description,
                "budget_range": budget_range,
                "timeline": timeline,
                "company_name": settings.APP_NAME,
            },
        )

    async def send_verification_email(
        self,
        to_email: str,
        user_name: str,
        token: str,
    ) -> bool:
        return await self.send_email(
            to_email=to_email,
            subject=f"Verify your {settings.APP_NAME} account",
            template_name="verify_email.html",
            context={
                "user_name": user_name,
                "email": to_email,
                "token": token,
                "verify_url": f"{settings.APP_URL}/verify-email?token={token}",
                "company_name": settings.APP_NAME,
                "expires_hours": settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS,
            },
        )

    async def send_password_reset_email(
        self,
        to_email: str,
        user_name: str,
        token: str,
        expires_hours: int = 1,
    ) -> bool:
        return await self.send_email(
            to_email=to_email,
            subject=f"Reset your {settings.APP_NAME} password",
            template_name="password_reset.html",
            context={
                "user_name": user_name,
                "email": to_email,
                "token": token,
                "reset_url": f"{settings.APP_URL}/reset-password?token={token}",
                "company_name": settings.APP_NAME,
                "expires_hours": expires_hours,
            },
        )

    async def send_password_changed_email(
        self,
        to_email: str,
        user_name: str,
    ) -> bool:
        return await self.send_email(
            to_email=to_email,
            subject=f"Your {settings.APP_NAME} password has been changed",
            template_name="password_changed.html",
            context={
                "user_name": user_name,
                "email": to_email,
                "company_name": settings.APP_NAME,
            },
        )

    async def send_password_reset_confirmation(
        self,
        to_email: str,
        user_name: str,
    ) -> bool:
        return await self.send_email(
            to_email=to_email,
            subject=f"Your {settings.APP_NAME} password has been reset",
            template_name="password_changed.html",
            context={
                "user_name": user_name,
                "email": to_email,
                "company_name": settings.APP_NAME,
            },
        )

    async def send_welcome_email(
        self,
        to_email: str,
        user_name: str,
    ) -> bool:
        return await self.send_email(
            to_email=to_email,
            subject=f"Welcome to {settings.APP_NAME}",
            template_name="welcome.html",
            context={
                "user_name": user_name,
                "email": to_email,
                "company_name": settings.APP_NAME,
            },
        )

    async def send_feedback_notification(
        self,
        name: str,
        email: str,
        rating: int,
        category: str,
        message: str,
    ) -> bool:
        return await self.send_email(
            to_email=settings.SMTP_FROM_EMAIL,
            subject=f"New Feedback from {name} - {category} ({rating}/5)",
            template_name="feedback.html",
            context={
                "name": name,
                "email": email,
                "rating": rating,
                "category": category,
                "message": message,
                "company_name": settings.APP_NAME,
            },
        )
