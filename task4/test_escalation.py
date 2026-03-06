import pytest
from engine import should_escalate


class MockContext:
    def __init__(self, crm_data=None, billing_data=None, ticket_history=None, data_complete=True):
        self.crm_data = crm_data or {}
        self.billing_data = billing_data or {}
        self.ticket_history = ticket_history or {}
        self.data_complete = data_complete


def test_low_confidence():
    """Test escalation when confidence is below threshold."""
    ctx = MockContext()
    result = should_escalate(ctx, 0.5, 0.0, "internet_issue")
    assert result == (True, "low_confidence")


def test_angry_customer():
    """Test escalation when sentiment is very negative."""
    ctx = MockContext()
    result = should_escalate(ctx, 0.9, -0.8, "internet_issue")
    assert result == (True, "angry_customer")


def test_repeat_complaint():
    """Test escalation when same complaint appears 3+ times."""
    ctx = MockContext(ticket_history={"complaints": ["slow_internet","slow_internet","slow_internet"]})
    result = should_escalate(ctx, 0.9, 0.0, "slow_internet")
    assert result == (True, "repeat_complaint")


def test_service_cancellation():
    """Test escalation when intent is service cancellation."""
    ctx = MockContext()
    result = should_escalate(ctx, 0.95, 0.0, "service_cancellation")
    assert result == (True, "service_cancellation")


def test_vip_overdue():
    """Test escalation for VIP customer with overdue bill."""
    ctx = MockContext(
        crm_data={"vip": True},
        billing_data={"overdue": True}
    )
    result = should_escalate(ctx, 0.9, 0.0, "billing_issue")
    assert result == (True, "vip_billing_issue")


def test_incomplete_data():
    """Test escalation when system data is incomplete and confidence < 0.80."""
    ctx = MockContext(data_complete=False)
    result = should_escalate(ctx, 0.7, 0.0, "internet_issue")
    assert result == (True, "incomplete_data")


def test_no_escalation():
    """Edge case: everything normal so AI should handle."""
    ctx = MockContext()
    result = should_escalate(ctx, 0.9, 0.2, "internet_issue")
    assert result == (False, "no_escalation")


def test_repeat_but_low_confidence_priority():
    """Edge case: low confidence should trigger escalation first."""
    ctx = MockContext(ticket_history={"complaints": ["a","a","a"]})
    result = should_escalate(ctx, 0.5, 0.0, "a")
    assert result == (True, "low_confidence")
