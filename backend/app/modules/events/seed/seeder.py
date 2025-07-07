import random
import uuid

from faker import Faker
from sqlalchemy.orm import Session

from app.modules.events.models import Event, EventField, EventTag
from app.modules.events.schemas import LinkType
from app.modules.fields.models import Field
from app.modules.tags.models import Tag

faker = Faker()

SHORT_ACTIONS = [
    "click",
    "view",
    "submit",
    "open",
    "close",
    "scroll",
    "hover",
    "load",
    "hide",
    "show",
    "change",
    "remove",
    "add",
    "edit",
    "delete",
]
TARGETS = [
    "button",
    "page",
    "form",
    "modal",
    "tab",
    "section",
    "tooltip",
    "link",
    "dialog",
    "dropdown",
    "table",
    "chart",
    "image",
    "text",
]


def generate_event_slug(existing: set) -> str:
    attempts = 0
    while attempts < 100:
        adjective = faker.word(part_of_speech="adjective")
        action = random.choice(SHORT_ACTIONS)
        target = random.choice(TARGETS)

        name = f"{adjective}_{target}_{action}"

        if name not in existing:
            return name
        attempts += 1

    return f"event_{uuid.uuid4()}"


ACTIONS = [
    "clicks a button",
    "views a page",
    "completes a form",
    "logs in",
    "signs up",
    "adds an item to cart",
    "removes a product",
    "starts checkout",
]

SCENARIOS = [
    "successful login",
    "signup failure",
    "purchase",
    "password reset",
    "newsletter subscription",
    "referral flow",
    "onboarding step",
]

CONTEXTS = [
    "purchase",
    "checkout process",
    "user flow",
    "conversion funnel",
]

STATES = [
    "verified their email",
    "enabled two-factor auth",
    "accepted terms",
]

INTERACTIONS = [
    "click",
    "hover",
    "submit",
    "scroll",
    "drag-and-drop",
]

EVENT_DESCRIPTION_TEMPLATES = [
    "Triggered when the user {action}.",
    "Fired after a {scenario}.",
    "Captures when a user {action}.",
    "Sent when a {context} is completed.",
    "Indicates that the user has {state}.",
    "Used to log {interaction} actions.",
]


def generate_event_description():
    template = random.choice(EVENT_DESCRIPTION_TEMPLATES)
    return template.format(
        action=random.choice(ACTIONS),
        scenario=random.choice(SCENARIOS),
        context=random.choice(CONTEXTS),
        state=random.choice(STATES),
        interaction=random.choice(INTERACTIONS),
    )


def generate_event_link():
    link_type = random.choice(list(LinkType))
    return {
        "type": link_type,
        "url": faker.url(),
        "label": None if link_type != LinkType.other else faker.company(),
    }


def seed(db: Session, count: int = 10):
    tags = db.query(Tag).all()
    fields = db.query(Field).all()

    if not tags or not fields:
        print("⚠️ No tags or fields available. Please seed them first.")
        return

    existing_names = set()

    for _ in range(count):
        name = generate_event_slug(existing_names)
        existing_names.add(name)

        links = [generate_event_link() for _ in range(random.randint(0, 4))]

        event = Event(
            name=name,
            description=generate_event_description(),
            links=links,
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        # Attach 0–2 random tags
        for tag in random.sample(tags, k=random.randint(0, min(2, len(tags)))):
            db.add(EventTag(event_id=event.id, tag_id=tag.id))

        # Attach 1–6 random fields
        for field in random.sample(fields, k=random.randint(1, min(6, len(fields)))):
            db.add(EventField(event_id=event.id, field_id=field.id))

        db.commit()

    print(f"✅ Seeded {count} events with random tags and fields.")
