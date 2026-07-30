from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.enums import ContentStatus
from app.repositories.resource import ResourceRepository
from app.repositories.service import ServiceRepository
from app.repositories.solution import SolutionRepository
from app.repositories.technology import TechnologyRepository
from app.utils.logger import app_logger

SERVICES = [
    {
        "title": "Cloud Engineering",
        "slug": "cloud-engineering",
        "description": (
            "Design, implement, and manage scalable cloud infrastructure across "
            "AWS, Azure, and GCP. Services include cloud migration, architecture "
            "design, cost optimization, and managed operations."
        ),
        "icon": "Cloud",
        "display_order": 1,
        "is_featured": True,
        "status": ContentStatus.PUBLISHED,
    },
    {
        "title": "Platform Engineering",
        "slug": "platform-engineering",
        "description": (
            "Build internal developer platforms (IDP) that accelerate software "
            "delivery. Services include CI/CD pipeline automation, infrastructure "
            "as code, container orchestration, and developer tooling."
        ),
        "icon": "Layers",
        "display_order": 2,
        "is_featured": True,
        "status": ContentStatus.PUBLISHED,
    },
    {
        "title": "DevSecOps",
        "slug": "devsecops",
        "description": (
            "Integrate security into every phase of the software development "
            "lifecycle. Services include security automation, compliance auditing, "
            "vulnerability management, and security training."
        ),
        "icon": "Shield",
        "display_order": 3,
        "is_featured": True,
        "status": ContentStatus.PUBLISHED,
    },
    {
        "title": "AI Engineering",
        "slug": "ai-engineering",
        "description": (
            "Leverage artificial intelligence and machine learning to solve complex "
            "business problems. Services include ML pipeline development, LLM "
            "integration, computer vision, and predictive analytics."
        ),
        "icon": "Brain",
        "display_order": 4,
        "is_featured": True,
        "status": ContentStatus.PUBLISHED,
    },
    {
        "title": "Managed Services",
        "slug": "managed-services",
        "description": (
            "24/7 monitoring, maintenance, and support for your cloud "
            "infrastructure. Services include incident response, patch management, "
            "performance optimization, and disaster recovery."
        ),
        "icon": "Settings",
        "display_order": 5,
        "is_featured": True,
        "status": ContentStatus.PUBLISHED,
    },
]

TECHNOLOGIES = [
    {"name": "AWS", "slug": "aws", "category": "cloud", "icon": "aws",
     "display_order": 1, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "Azure", "slug": "azure", "category": "cloud", "icon": "azure",
     "display_order": 2, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "Google Cloud", "slug": "gcp", "category": "cloud", "icon": "gcp",
     "display_order": 3, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "Kubernetes", "slug": "kubernetes", "category": "containers", "icon": "kubernetes",
     "display_order": 4, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "Docker", "slug": "docker", "category": "containers", "icon": "docker",
     "display_order": 5, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "Terraform", "slug": "terraform", "category": "iac", "icon": "terraform",
     "display_order": 6, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "Ansible", "slug": "ansible", "category": "iac", "icon": "ansible",
     "display_order": 7, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "GitHub Actions", "slug": "github-actions", "category": "cicd", "icon": "github",
     "display_order": 8, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "Jenkins", "slug": "jenkins", "category": "cicd", "icon": "jenkins",
     "display_order": 9, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "Python", "slug": "python", "category": "languages", "icon": "python",
     "display_order": 10, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "TypeScript", "slug": "typescript", "category": "languages", "icon": "typescript",
     "display_order": 11, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "React", "slug": "react", "category": "frontend", "icon": "react",
     "display_order": 12, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "PostgreSQL", "slug": "postgresql", "category": "databases", "icon": "postgresql",
     "display_order": 13, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "Redis", "slug": "redis", "category": "databases", "icon": "redis",
     "display_order": 14, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "FastAPI", "slug": "fastapi", "category": "backend", "icon": "fastapi",
     "display_order": 15, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "Node.js", "slug": "nodejs", "category": "backend", "icon": "nodejs",
     "display_order": 16, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "Prometheus", "slug": "prometheus", "category": "monitoring", "icon": "prometheus",
     "display_order": 17, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "Grafana", "slug": "grafana", "category": "monitoring", "icon": "grafana",
     "display_order": 18, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {"name": "Datadog", "slug": "datadog", "category": "monitoring", "icon": "datadog",
     "display_order": 19, "is_featured": True, "status": ContentStatus.PUBLISHED},
    {
        "name": "Elasticsearch", "slug": "elasticsearch",
        "category": "monitoring", "icon": "elasticsearch",
        "display_order": 20, "is_featured": True, "status": ContentStatus.PUBLISHED},
]

SOLUTIONS = [
    {
        "title": "Cloud Migration & Modernization",
        "slug": "cloud-migration-modernization",
        "description": (
            "Seamlessly migrate on-premises workloads to the cloud and modernize "
            "legacy applications for improved performance, scalability, and cost efficiency."
        ),
        "category": "infrastructure", "icon": "Cloud",
        "display_order": 1, "is_featured": True, "status": ContentStatus.PUBLISHED,
    },
    {
        "title": "CI/CD Pipeline Automation",
        "slug": "cicd-pipeline-automation",
        "description": (
            "Automate build, test, and deployment pipelines to accelerate software "
            "delivery while maintaining quality and security standards."
        ),
        "category": "devops", "icon": "GitBranch",
        "display_order": 2, "is_featured": True, "status": ContentStatus.PUBLISHED,
    },
    {
        "title": "Kubernetes & Containerization",
        "slug": "kubernetes-containerization",
        "description": (
            "Design and manage containerized applications with Kubernetes "
            "orchestration for consistent, scalable deployments across any environment."
        ),
        "category": "containers", "icon": "Container",
        "display_order": 3, "is_featured": True, "status": ContentStatus.PUBLISHED,
    },
    {
        "title": "Security & Compliance Automation",
        "slug": "security-compliance-automation",
        "description": (
            "Automate security controls, compliance checks, and vulnerability "
            "management to maintain robust security posture across your infrastructure."
        ),
        "category": "security", "icon": "Shield",
        "display_order": 4, "is_featured": True, "status": ContentStatus.PUBLISHED,
    },
    {
        "title": "AI/ML Platform Engineering",
        "slug": "aiml-platform-engineering",
        "description": (
            "Build and manage AI/ML platforms that enable data scientists and "
            "developers to train, deploy, and monitor machine learning models at scale."
        ),
        "category": "ai", "icon": "Brain",
        "display_order": 5, "is_featured": True, "status": ContentStatus.PUBLISHED,
    },
    {
        "title": "Observability & Monitoring",
        "slug": "observability-monitoring",
        "description": (
            "Implement comprehensive observability with metrics, logs, and traces "
            "to gain deep visibility into system performance and user experience."
        ),
        "category": "monitoring", "icon": "Activity",
        "display_order": 6, "is_featured": True, "status": ContentStatus.PUBLISHED,
    },
]

RESOURCES = [
    {
        "title": "The Ultimate Guide to Cloud Migration Strategy",
        "slug": "ultimate-guide-cloud-migration",
        "category": "guide",
        "summary": (
            "A comprehensive guide to planning and executing a successful cloud "
            "migration strategy for enterprise organizations."
        ),
        "author": "VALP SYSTEMS Engineering Team",
        "published_date": datetime(2025, 11, 15, tzinfo=timezone.utc),
        "status": ContentStatus.PUBLISHED,
        "tags": "cloud,migration,strategy,enterprise",
    },
    {
        "title": "Kubernetes Best Practices for Production",
        "slug": "kubernetes-best-practices-production",
        "category": "blog",
        "summary": (
            "Learn the essential best practices for running Kubernetes workloads "
            "in production environments, from security to monitoring."
        ),
        "author": "VALP SYSTEMS Engineering Team",
        "published_date": datetime(2025, 10, 20, tzinfo=timezone.utc),
        "status": ContentStatus.PUBLISHED,
        "tags": "kubernetes,containers,production,devops",
    },
    {
        "title": "DevSecOps: Integrating Security into Your Pipeline",
        "slug": "devsecops-integrating-security-pipeline",
        "category": "whitepaper",
        "summary": (
            "A deep dive into DevSecOps practices and how to integrate security "
            "seamlessly into your CI/CD pipeline without slowing down development."
        ),
        "author": "VALP SYSTEMS Security Team",
        "published_date": datetime(2025, 9, 5, tzinfo=timezone.utc),
        "status": ContentStatus.PUBLISHED,
        "tags": "devsecops,security,cicd,automation",
    },
    {
        "title": "Building Internal Developer Platforms with Platform Engineering",
        "slug": "building-internal-developer-platforms",
        "category": "blog",
        "summary": (
            "Discover how platform engineering can accelerate your development "
            "teams by providing self-service capabilities and standardized workflows."
        ),
        "author": "VALP SYSTEMS Engineering Team",
        "published_date": datetime(2025, 8, 12, tzinfo=timezone.utc),
        "status": ContentStatus.PUBLISHED,
        "tags": "platform-engineering,developer-experience,idp",
    },
    {
        "title": "AI Engineering: From Experiment to Production",
        "slug": "ai-engineering-experiment-to-production",
        "category": "case_study",
        "summary": (
            "How we helped an enterprise client take their AI initiatives from "
            "experimental prototypes to production-ready systems."
        ),
        "author": "VALP SYSTEMS AI Team",
        "published_date": datetime(2025, 7, 22, tzinfo=timezone.utc),
        "status": ContentStatus.PUBLISHED,
        "tags": "ai,ml,machine-learning,production,case-study",
    },
]


async def seed_database(session: AsyncSession) -> None:
    app_logger.info("Starting database seeding...")

    service_repo = ServiceRepository(session)
    technology_repo = TechnologyRepository(session)
    solution_repo = SolutionRepository(session)
    resource_repo = ResourceRepository(session)

    existing_services = await service_repo.count()
    if existing_services == 0:
        await service_repo.bulk_create(SERVICES)
        app_logger.info(f"Seeded {len(SERVICES)} services")
    else:
        app_logger.info(f"Skipping services seed: {existing_services} already exist")

    existing_technologies = await technology_repo.count()
    if existing_technologies == 0:
        await technology_repo.bulk_create(TECHNOLOGIES)
        app_logger.info(f"Seeded {len(TECHNOLOGIES)} technologies")
    else:
        app_logger.info(f"Skipping technologies seed: {existing_technologies} already exist")

    existing_solutions = await solution_repo.count()
    if existing_solutions == 0:
        await solution_repo.bulk_create(SOLUTIONS)
        app_logger.info(f"Seeded {len(SOLUTIONS)} solutions")
    else:
        app_logger.info(f"Skipping solutions seed: {existing_solutions} already exist")

    existing_resources = await resource_repo.count()
    if existing_resources == 0:
        await resource_repo.bulk_create(RESOURCES)
        app_logger.info(f"Seeded {len(RESOURCES)} resources")
    else:
        app_logger.info(f"Skipping resources seed: {existing_resources} already exist")

    app_logger.info("Database seeding completed")


async def clear_database(session: AsyncSession) -> None:
    app_logger.info("Clearing database...")
    tables = [
        "resources", "solutions", "services", "technologies",
        "feedbacks", "quote_requests", "career_applications",
        "newsletters", "contacts",
    ]
    for table in tables:
        await session.execute(text(f"DELETE FROM {table}"))
    await session.commit()
    app_logger.info("Database cleared")
