from typing import Tuple


def should_escalate(context, confidence_score: float, sentiment_score: float, intent: str) -> Tuple[bool, str]:

    # Rule 1: confidence below 0.65
    if confidence_score < 0.65:
        return True, "low_confidence"

    # Rule 2: angry customer sentiment
    if sentiment_score < -0.6:
        return True, "angry_customer"

    # Rule 3: repeat complaint (same intent 3 or more times)
    if context.ticket_history and "complaints" in context.ticket_history:
        complaints = context.ticket_history["complaints"]
        if complaints.count(intent) >= 3:
            return True, "repeat_complaint"

    # Rule 4: service cancellation always escalate
    if intent == "service_cancellation":
        return True, "service_cancellation"

    # Rule 5: VIP customer with overdue billing
    if context.crm_data and context.billing_data:
        if context.crm_data.get("vip") and context.billing_data.get("overdue"):
            return True, "vip_billing_issue"

    # Rule 6: incomplete data and low confidence
    if not context.data_complete and confidence_score < 0.80:
        return True, "incomplete_data"

    return False, "no_escalation"
