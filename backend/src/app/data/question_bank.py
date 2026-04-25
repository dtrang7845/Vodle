from __future__ import annotations

from app.schemas.question import GeneratedQuestionDraft, QuestionOptionCreate


CONTEXTS = [
    {
        "title": "Morning Routine",
        "description": "How people like to begin the day.",
        "label": "morning routine",
        "article": "a",
        "tags": ["morning", "routine", "daily"],
    },
    {
        "title": "Weekend Outing",
        "description": "Free-time plans and preferences.",
        "label": "weekend outing",
        "article": "a",
        "tags": ["weekend", "social", "outdoor"],
    },
    {
        "title": "Movie Night",
        "description": "How people like to spend a movie night.",
        "label": "movie night",
        "article": "a",
        "tags": ["movies", "entertainment", "night"],
    },
    {
        "title": "Road Trip",
        "description": "Travel styles and preferences.",
        "label": "road trip",
        "article": "a",
        "tags": ["travel", "cars", "weekend"],
    },
    {
        "title": "Workout Session",
        "description": "Exercise preferences and routines.",
        "label": "workout session",
        "article": "a",
        "tags": ["fitness", "exercise", "health"],
    },
    {
        "title": "Study Session",
        "description": "How people like to learn and focus.",
        "label": "study session",
        "article": "a",
        "tags": ["study", "school", "focus"],
    },
    {
        "title": "Dinner Out",
        "description": "Dining preferences for a night out.",
        "label": "dinner out",
        "article": "a",
        "tags": ["food", "restaurants", "evening"],
    },
    {
        "title": "Lunch Break",
        "description": "How people like to spend their midday pause.",
        "label": "lunch break",
        "article": "a",
        "tags": ["food", "work", "midday"],
    },
    {
        "title": "Shopping Trip",
        "description": "How people approach a shopping run.",
        "label": "shopping trip",
        "article": "a",
        "tags": ["shopping", "errands", "lifestyle"],
    },
    {
        "title": "Beach Day",
        "description": "Summer-day preferences and plans.",
        "label": "beach day",
        "article": "a",
        "tags": ["summer", "beach", "outdoor"],
    },
    {
        "title": "Board Game Night",
        "description": "How people like to set up game night.",
        "label": "board game night",
        "article": "a",
        "tags": ["games", "friends", "night"],
    },
    {
        "title": "Coffee Shop Visit",
        "description": "How people like to spend cafe time.",
        "label": "coffee shop visit",
        "article": "a",
        "tags": ["coffee", "cafe", "daily"],
    },
    {
        "title": "Museum Visit",
        "description": "How people like to explore a museum.",
        "label": "museum visit",
        "article": "a",
        "tags": ["art", "culture", "indoor"],
    },
    {
        "title": "Park Visit",
        "description": "How people enjoy time in the park.",
        "label": "park visit",
        "article": "a",
        "tags": ["park", "outdoor", "relaxing"],
    },
    {
        "title": "Birthday Celebration",
        "description": "How people like to celebrate a birthday.",
        "label": "birthday celebration",
        "article": "a",
        "tags": ["birthday", "celebration", "social"],
    },
    {
        "title": "Day Off",
        "description": "How people like to spend free days.",
        "label": "day off",
        "article": "a",
        "tags": ["rest", "weekend", "lifestyle"],
    },
    {
        "title": "Date Night",
        "description": "Evening plans and vibe preferences.",
        "label": "date night",
        "article": "a",
        "tags": ["date", "evening", "social"],
    },
    {
        "title": "Creative Project",
        "description": "How people like to work on something creative.",
        "label": "creative project",
        "article": "a",
        "tags": ["creative", "art", "hobby"],
    },
    {
        "title": "Cooking Session",
        "description": "Kitchen habits and cooking preferences.",
        "label": "cooking session",
        "article": "a",
        "tags": ["cooking", "food", "home"],
    },
    {
        "title": "Hiking Trip",
        "description": "How people like to approach a hike.",
        "label": "hiking trip",
        "article": "a",
        "tags": ["hiking", "nature", "outdoor"],
    },
    {
        "title": "Holiday Gathering",
        "description": "How people like to spend a holiday get-together.",
        "label": "holiday gathering",
        "article": "a",
        "tags": ["holiday", "family", "celebration"],
    },
    {
        "title": "Commute",
        "description": "How people like to structure their travel time.",
        "label": "commute",
        "article": "a",
        "tags": ["commute", "work", "travel"],
    },
    {
        "title": "Rainy Day Plan",
        "description": "How people like to spend a rainy day.",
        "label": "rainy day plan",
        "article": "a",
        "tags": ["weather", "indoor", "cozy"],
    },
    {
        "title": "Sunday Reset",
        "description": "How people like to reset for the week ahead.",
        "label": "Sunday reset",
        "article": "a",
        "tags": ["sunday", "routine", "home"],
    },
    {
        "title": "Brunch Outing",
        "description": "How people like to do brunch.",
        "label": "brunch outing",
        "article": "a",
        "tags": ["brunch", "food", "weekend"],
    },
    {
        "title": "Camping Trip",
        "description": "Outdoor trip preferences.",
        "label": "camping trip",
        "article": "a",
        "tags": ["camping", "nature", "travel"],
    },
    {
        "title": "Concert Night",
        "description": "How people like to experience a concert.",
        "label": "concert night",
        "article": "a",
        "tags": ["music", "nightlife", "events"],
    },
    {
        "title": "Library Visit",
        "description": "How people like to use library time.",
        "label": "library visit",
        "article": "a",
        "tags": ["books", "study", "quiet"],
    },
    {
        "title": "DIY Project",
        "description": "Hands-on project styles and preferences.",
        "label": "DIY project",
        "article": "a",
        "tags": ["DIY", "home", "creative"],
    },
    {
        "title": "Apartment Refresh",
        "description": "How people approach improving their space.",
        "label": "apartment refresh",
        "article": "an",
        "tags": ["home", "decor", "lifestyle"],
    },
    {
        "title": "Game Session",
        "description": "How people like to spend gaming time.",
        "label": "game session",
        "article": "a",
        "tags": ["games", "indoor", "fun"],
    },
    {
        "title": "Sightseeing Day",
        "description": "Travel-day preferences while exploring.",
        "label": "sightseeing day",
        "article": "a",
        "tags": ["travel", "city", "explore"],
    },
    {
        "title": "Farmers Market Visit",
        "description": "How people like to shop local.",
        "label": "farmers market visit",
        "article": "a",
        "tags": ["food", "shopping", "weekend"],
    },
    {
        "title": "School Project",
        "description": "How people like to approach a shared assignment.",
        "label": "school project",
        "article": "a",
        "tags": ["school", "study", "teamwork"],
    },
    {
        "title": "Reunion",
        "description": "How people like to spend a reunion.",
        "label": "reunion",
        "article": "a",
        "tags": ["friends", "family", "social"],
    },
    {
        "title": "Watch Party",
        "description": "How people like to set up a sports or show watch party.",
        "label": "watch party",
        "article": "a",
        "tags": ["sports", "tv", "friends"],
    },
    {
        "title": "Self-Care Evening",
        "description": "How people like to unwind at night.",
        "label": "self-care evening",
        "article": "a",
        "tags": ["wellness", "night", "relaxing"],
    },
    {
        "title": "Pet Walk",
        "description": "How people like to approach a walk with their pet.",
        "label": "pet walk",
        "article": "a",
        "tags": ["pets", "walking", "outdoor"],
    },
    {
        "title": "Photography Outing",
        "description": "How people like to spend a photo-focused outing.",
        "label": "photography outing",
        "article": "a",
        "tags": ["photography", "creative", "outdoor"],
    },
    {
        "title": "Picnic",
        "description": "How people like to set up a picnic.",
        "label": "picnic",
        "article": "a",
        "tags": ["outdoor", "food", "weekend"],
    },
    {
        "title": "Networking Event",
        "description": "How people like to approach professional events.",
        "label": "networking event",
        "article": "a",
        "tags": ["career", "events", "social"],
    },
    {
        "title": "Festival Visit",
        "description": "How people like to explore a festival.",
        "label": "festival visit",
        "article": "a",
        "tags": ["festival", "events", "music"],
    },
    {
        "title": "Volunteering Day",
        "description": "How people like to contribute their time.",
        "label": "volunteering day",
        "article": "a",
        "tags": ["community", "service", "weekend"],
    },
    {
        "title": "Remote Workday",
        "description": "How people like to structure working from home.",
        "label": "remote workday",
        "article": "a",
        "tags": ["work", "home", "productivity"],
    },
    {
        "title": "Desk Refresh",
        "description": "How people like to improve their workspace.",
        "label": "desk refresh",
        "article": "a",
        "tags": ["workspace", "productivity", "home"],
    },
    {
        "title": "Morning Walk",
        "description": "How people like to ease into a walk outdoors.",
        "label": "morning walk",
        "article": "a",
        "tags": ["morning", "walking", "wellness"],
    },
    {
        "title": "Podcast Session",
        "description": "How people like to listen to a podcast.",
        "label": "podcast session",
        "article": "a",
        "tags": ["podcast", "audio", "daily"],
    },
    {
        "title": "Reading Session",
        "description": "How people like to settle in with a book.",
        "label": "reading session",
        "article": "a",
        "tags": ["books", "reading", "quiet"],
    },
    {
        "title": "Dinner Party",
        "description": "How people like to host or attend dinner with others.",
        "label": "dinner party",
        "article": "a",
        "tags": ["food", "hosting", "social"],
    },
    {
        "title": "City Day",
        "description": "How people like to spend a day exploring a city.",
        "label": "city day",
        "article": "a",
        "tags": ["city", "travel", "weekend"],
    },
    {
        "title": "Home Cleanup",
        "description": "How people like to approach getting the house in order.",
        "label": "home cleanup",
        "article": "a",
        "tags": ["home", "routine", "chores"],
    },
    {
        "title": "Airport Day",
        "description": "How people like to handle travel-day logistics.",
        "label": "airport day",
        "article": "an",
        "tags": ["airport", "travel", "planning"],
    },
]


QUESTION_TYPES = [
    {
        "suffix": "Style",
        "description": "A question about preferred style and structure.",
        "question_template": "What kind of {label} feels best to you?",
        "options": [
            "Carefully planned",
            "Relaxed but structured",
            "Flexible and open",
            "Totally spontaneous",
        ],
    },
    {
        "suffix": "Timing",
        "description": "A question about when people prefer it most.",
        "question_template": "When would you most want {article} {label}?",
        "options": [
            "Early morning",
            "Late morning",
            "Afternoon",
            "Evening",
        ],
    },
    {
        "suffix": "Energy",
        "description": "A question about the desired energy level.",
        "question_template": "What energy do you want from {article} {label}?",
        "options": [
            "Calm and quiet",
            "Steady and balanced",
            "Lively and social",
            "High-energy and packed",
        ],
    },
    {
        "suffix": "Company",
        "description": "A question about who people want around.",
        "question_template": "Who would you most want for {article} {label}?",
        "options": [
            "Just me",
            "One other person",
            "A small group",
            "A bigger crowd",
        ],
    },
    {
        "suffix": "Setting",
        "description": "A question about the best setting or environment.",
        "question_template": "What setting suits {article} {label} best?",
        "options": [
            "At home",
            "Out in the city",
            "Outdoors",
            "A mix of settings",
        ],
    },
    {
        "suffix": "Priority",
        "description": "A question about what matters most in the experience.",
        "question_template": "What matters most in a great {label}?",
        "options": [
            "Comfort",
            "Efficiency",
            "Fun",
            "Trying something new",
        ],
    },
]


def build_question_bank() -> list[dict[str, object]]:
    bank: list[dict[str, object]] = []

    for context in CONTEXTS:
        for question_type in QUESTION_TYPES:
            title = f"{context['title']} {question_type['suffix']}"
            description = f"{context['description']} {question_type['description']}"
            question_text = question_type["question_template"].format(
                label=context["label"],
                article=context["article"],
            )
            bank.append(
                {
                    "title": title,
                    "description": description,
                    "question_text": question_text,
                    "options": question_type["options"],
                    "tags": context["tags"],
                }
            )

    return bank[:300]


QUESTION_BANK = build_question_bank()


def question_bank_size() -> int:
    return len(QUESTION_BANK)


def question_bank_drafts() -> list[GeneratedQuestionDraft]:
    return [
        GeneratedQuestionDraft(
            title=entry["title"],
            description=entry["description"],
            question_text=entry["question_text"],
            options=[
                QuestionOptionCreate(option_text=option_text)
                for option_text in entry["options"]
            ],
        )
        for entry in QUESTION_BANK
    ]
