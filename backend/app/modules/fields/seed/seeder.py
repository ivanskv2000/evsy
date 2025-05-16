import random

from faker import Faker
from sqlalchemy.orm import Session

from app.modules.fields.models import Field, FieldType

fake = Faker()

BASES = [
    "user",
    "session",
    "device",
    "page",
    "event",
    "campaign",
    "platform",
    "country",
    "language",
    "subscription",
    "experiment",
    "click",
    "ref",
]

SUFFIXES = ["id", "type", "name", "source", "status", "variant", "group", "version"]

PREFIXES = ["is", "has", "from", "to", "ref"]


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
        source=random.choice(SOURCES),
    )


def generate_field_example(field_type: FieldType):
    if field_type == FieldType.string:
        return fake.word()
    elif field_type == FieldType.integer:
        return random.randint(0, 1000000)
    elif field_type == FieldType.number:
        return random.uniform(0, 1000000)
    elif field_type == FieldType.boolean:
        return random.choice([True, False])
    elif field_type == FieldType.array:
        return [fake.word() for _ in range(random.randint(1, 10))]
    elif field_type == FieldType.object:
        return {
            fake.word(part_of_speech="noun"): fake.word(part_of_speech="adjective")
            for _ in range(random.randint(1, 5))
        }
    else:
        return None


def seed(db: Session, count: int = 20):
    existing_names = set()

    for _ in range(count):
        name = generate_field_slug(existing_names)
        existing_names.add(name)

        field_type = random.choice(list(FieldType))
        example = generate_field_example(field_type)

        db_field = Field(
            name=name,
            description=generate_field_description(),
            field_type=field_type,
            example=example,
        )
        db.add(db_field)

    db.commit()
    print(f"✅ Seeded {count} fields.")
