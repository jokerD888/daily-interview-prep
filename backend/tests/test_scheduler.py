import pytest
from app.services.scheduler import advance_state, reset_state, CardState


def test_advance_new_to_level_0():
    state, _ = advance_state(CardState.new)
    assert state == CardState.level_0


def test_advance_level_5_to_mastered():
    state, _ = advance_state(CardState.level_5)
    assert state == CardState.mastered


def test_advance_mastered_stays():
    state, _ = advance_state(CardState.mastered)
    assert state == CardState.mastered


def test_reset_to_level_0():
    state, _ = reset_state()
    assert state == CardState.level_0
