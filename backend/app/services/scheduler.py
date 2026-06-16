from datetime import datetime, timedelta
from app.models.card_progress import CardState

INTERVALS = {
    CardState.new: 0,
    CardState.level_0: 1,
    CardState.level_1: 2,
    CardState.level_2: 4,
    CardState.level_3: 7,
    CardState.level_4: 15,
    CardState.level_5: 30,
}

STATE_ORDER = [CardState.new, CardState.level_0, CardState.level_1,
               CardState.level_2, CardState.level_3, CardState.level_4, CardState.level_5]


def advance_state(current: CardState) -> tuple[CardState, datetime]:
    """Return (next_state, next_review_at). mastered stays mastered."""
    if current == CardState.mastered:
        return CardState.mastered, datetime.utcnow() + timedelta(days=365)

    idx = STATE_ORDER.index(current)
    if idx + 1 < len(STATE_ORDER):
        next_state = STATE_ORDER[idx + 1]
    else:
        next_state = CardState.mastered

    interval = INTERVALS.get(next_state, 365)
    return next_state, datetime.utcnow() + timedelta(days=interval)


def reset_state() -> tuple[CardState, datetime]:
    """Forget: reset to level_0, review tomorrow."""
    return CardState.level_0, datetime.utcnow() + timedelta(days=1)
