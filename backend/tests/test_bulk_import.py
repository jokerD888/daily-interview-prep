"""Tests for bulk-import bridge endpoint."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.schemas.bridge import BulkImportRequest, BulkImportResponse, BridgeCardItem
from app.api.cards import bulk_import
from app.models.card import Card
from app.models.card_progress import CardProgress, CardState
from app.models.user import User


def test_bulk_import_request_validation():
    """Request validates card list length constraints."""
    with pytest.raises(ValueError):
        BulkImportRequest(cards=[])  # min_length=1

    with pytest.raises(ValueError):
        BulkImportRequest(cards=[BridgeCardItem(question=f"q{i}", answer=f"a{i}") for i in range(51)])  # max_length=50


def test_bulk_import_request_missing_question():
    """Question field is required."""
    with pytest.raises(ValueError):
        BridgeCardItem(question="", answer="some answer")


@pytest.mark.asyncio
async def test_bulk_import_inserts_new_cards():
    """New cards are inserted with progress rows."""
    db = AsyncMock()
    # No existing questions
    db.execute.return_value.scalars.return_value.all.return_value = []
    db.flush = AsyncMock()

    user = User(id=1, username="test", hashed_password="x")

    req = BulkImportRequest(cards=[
        BridgeCardItem(question="什么是 GIL？", answer="Python 全局解释器锁", importance_score=4),
        BridgeCardItem(question="TCP 三次握手", answer="SYN ...", importance_score=3, source_url="https://example.com"),
    ])

    resp = await bulk_import(req, db, user)
    assert resp.imported == 2
    assert resp.skipped == 0
    # flush called once per card (to get card.id)
    assert db.flush.call_count == 2
    # commit called once
    db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_bulk_import_skips_duplicates():
    """Duplicates by (user_id, question) are skipped."""
    db = AsyncMock()
    db.execute.return_value.scalars.return_value.all.return_value = ["什么是 GIL？"]
    db.flush = AsyncMock()

    user = User(id=1, username="test", hashed_password="x")
    req = BulkImportRequest(cards=[
        BridgeCardItem(question="什么是 GIL？", answer="重复的"),  # duplicate
        BridgeCardItem(question="TCP 三次握手", answer="新的"),
    ])

    resp = await bulk_import(req, db, user)
    assert resp.imported == 1
    assert resp.skipped == 1
    assert len(resp.skipped_reasons) == 1
    assert "什么是 GIL？" in resp.skipped_reasons[0]
