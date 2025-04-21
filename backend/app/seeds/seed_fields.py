from faker import Faker
from sqlalchemy.orm import Session
from app import models
import random

fake = Faker()

BASES = [
    "user", "session", "device", "page", "event", "campaign", "platform",
    "country", "language", "subscription", "experiment", "click", "ref"
]

SUFFIXES = [
    "id", "type", "name", "source", "status", "variant", "group", "version"
]

PREFIXES = [
    "is", "has", "from", "to", "ref"
]

def generate_field_slug(existing: set) -> str:
    attempts = 0
    while attempts < 50:
        # Randomly pick naming pattern
        if random.random() < 0.3:
            prefix = random.choice(PREFIXES)
            base = random.choice(BASES)
            name = f"{prefix}_{base}"
        else:
            base = random.choice(BASES)
            suffix = random.choice(SUFFIXES)
            name = f"{base}_{suffix}"

        if name not in existing:
            return name
        attempts += 1

    return f"field_{random.randint(1000, 9999)}"


DESCRIPTION_TEMPLATES = [
    "The {noun} of the current {entity}.",
    "Indicates whether the user has a {feature}.",
    "Tracks the {action} during a session.",
    "Represents the {noun} associated with the event.",
    "Shows whether the user is {status}.",
    "Used to identify the {entity} uniquely.",
    "Defines the {property} used for segmentation.",
    "Stores the {source} from which the user arrived.",
]

NOUNS = ["ID", "type", "variant", "source", "device", "campaign", "country", "referrer"]
ENTITIES = ["user", "session", "event", "page", "campaign"]
ACTIONS = ["click", "signup", "conversion", "view"]
STATUSES = ["logged in", "subscribed", "anonymous"]
PROPERTIES = ["platform", "language", "subscription tier"]
SOURCES = ["referrer", "ad", "UTM tag", "entry point"]


def generate_field_description():
    template = random.choice(DESCRIPTION_TEMPLATES)

    return template.format(
        noun=random.choice(NOUNS),
        entity=random.choice(ENTITIES),
        action=random.choice(ACTIONS),
        status=random.choice(STATUSES),
        feature=random.choice(PROPERTIES),
        property=random.choice(PROPERTIES),
        source=random.choice(SOURCES)
    )


def seed_fields(db: Session, count: int = 20):
    existing_names = set()
    
    for _ in range(count):
        name = generate_field_slug(existing_names)
        existing_names.add(name)

        db_field = models.Field(
            name=name,
            description=generate_field_description(),
            field_type=random.choice(list(models.FieldType))
        )
        db.add(db_field)

    db.commit()
    print(f"✅ Seeded {count} fields.")
