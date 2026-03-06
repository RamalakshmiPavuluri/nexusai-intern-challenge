import asyncio
from models import MessageResponse

async def mock_ai_call(message: str):
    await asyncio.sleep(1)  # simulate API delay

    return {
        "response": "Please restart your router. If the issue continues, contact support.",
        "confidence": 0.85,
        "action": "restart_router"
    }

async def handle_message(customer_message: str, customer_id: str, channel: str):

    # Error case 1: empty input
    if not customer_message.strip():
        return MessageResponse(
            response_text="",
            confidence=0,
            suggested_action="none",
            channel_formatted_response="",
            error="empty_input"
        )

    try:
        result = await asyncio.wait_for(mock_ai_call(customer_message), timeout=10)

    except asyncio.TimeoutError:
        return MessageResponse(
            response_text="",
            confidence=0,
            suggested_action="none",
            channel_formatted_response="",
            error="api_timeout"
        )

    response_text = result["response"]
    confidence = result["confidence"]
    action = result["action"]

    # Format response based on channel
    if channel == "voice":
        formatted = response_text.split(".")[0] + "."
    else:
        formatted = response_text

    return MessageResponse(
        response_text=response_text,
        confidence=confidence,
        suggested_action=action,
        channel_formatted_response=formatted,
        error=None
    )
