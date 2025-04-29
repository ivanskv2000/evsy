from faker import Faker
from sqlalchemy.orm import Session
from app import models
import random

fake = Faker()

feature_tags = [
    "onboarding", "referral", "checkout", "recommendations", "auth_flow",
    "notifications", "search_improvements", "profile_redesign"
]

context_tags = [
    "beta_users", "internal", "release_v1_2", "early_access", "tracking", "debug"
]

TAG_NAMES = feature_tags + context_tags

def generate_tag_name(existing: set) -> str:
    attempts = 0
    while attempts < 50:
        name = random.choice(TAG_NAMES)
        if name not in existing:
            return name
        attempts += 1
    
    return f"tag_{random.randint(1000, 9999)}"


FEATURES = [
    "onboarding", "checkout", "referral", "recommendations", "auth", "search", "profile", "notifications"
]

FUNNELS = [
    "signup", "purchase", "retention", "activation", "churn", "conversion"
]

JOURNEYS = [
    "user onboarding", "checkout", "referral program", "premium upgrade"
]

VERSIONS = [
    "v1.0.0", "v1.2.3", "v2.0-beta", "v3.4.1", "release-2024-11"
]

EXPERIMENTS = [
    "button-color-test", "new-flow-variation", "pricing-toggle", "copy-change-experiment"
]

TAG_DESCRIPTION_TEMPLATES = [
    "Used for A/B test of the {feature}.",
    "Marks events in experiment '{experiment}'.",
    "Part of the {funnel} funnel.",
    "Used in {journey} flow tracking.",
    "Tracks interactions in the {feature} module.",
    "Related to the {feature} rollout.",
    "Introduced in release {version}.",
    "Enabled after {version} deployment.",
    "Used for debugging {feature}.",
    "Added for internal monitoring of {feature}.",
]

def generate_tag_description():
    template = random.choice(TAG_DESCRIPTION_TEMPLATES)
    return template.format(
        feature=random.choice(FEATURES),
        funnel=random.choice(FUNNELS),
        journey=random.choice(JOURNEYS),
        version=random.choice(VERSIONS),
        experiment=random.choice(EXPERIMENTS),
    )

def seed_tags(db: Session, count: int = 10):
    existing_names = set()

    for _ in range(count):
        name = generate_tag_name(existing_names)
        existing_names.add(name)

        db_tag = models.Tag(
            id=name,
            description=generate_tag_description(),
        )
        db.add(db_tag)

    db.commit()
    print(f"✅ Seeded {count} tags.")
