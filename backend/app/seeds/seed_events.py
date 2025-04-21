from sqlalchemy.orm import Session
from app import models
from faker import Faker
import random

faker = Faker()

ACTIONS = ['click', 'view', 'submit', 'open', 'close', 'scroll', 'hover', 'load', 'hide', 'show', 'change', 'remove', 'add', 'edit', 'delete']
TARGETS = ['button', 'page', 'form', 'modal', 'tab', 'section', 'tooltip', 'link', 'dialog', 'dropdown', 'table', 'chart', 'image', 'text']

def generate_event_slug():
    adjective = faker.word(part_of_speech='adjective')
    action = random.choice(ACTIONS)
    target = random.choice(TARGETS)
    return f"{adjective}_{target}_{action}"


ACTIONS = [
    "clicks a button", "views a page", "completes a form", "logs in",
    "signs up", "adds an item to cart", "removes a product", "starts checkout",
]

SCENARIOS = [
    "successful login", "signup failure", "purchase", "password reset",
    "newsletter subscription", "referral flow", "onboarding step",
]

CONTEXTS = [
    "purchase", "checkout process", "user flow", "conversion funnel",
]

STATES = [
    "verified their email", "enabled two-factor auth", "accepted terms",
]

INTERACTIONS = [
    "click", "hover", "submit", "scroll", "drag-and-drop",
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

def seed_events(db: Session, count: int = 10):
    tags = db.query(models.Tag).all()
    fields = db.query(models.Field).all()

    if not tags or not fields:
        print("⚠️ No tags or fields available. Please seed them first.")
        return
    
    used_names = set()

    for _ in range(count):
        name = generate_event_slug()
        while name in used_names:
            name = generate_event_slug()
        used_names.add(name)

        event = models.Event(
            name=name,
            description=generate_event_description(),
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        # Attach 0–2 random tags
        for tag in random.sample(tags, k=random.randint(0, min(2, len(tags)))):
            db.add(models.EventTag(event_id=event.id, tag_id=tag.id))

        # Attach 1–6 random fields
        for field in random.sample(fields, k=random.randint(1, min(6, len(fields)))):
            db.add(models.EventField(event_id=event.id, field_id=field.id))

        db.commit()


    print(f"✅ Seeded {count} events with random tags and fields.")
