import asyncio
import random
import time
from dataclasses import dataclass

@dataclass
class CustomerContext:
    crm_data: dict
    billing_data: dict
    ticket_history: dict
    data_complete: bool
    fetch_time_ms: float


# Mock CRM fetch
async def fetch_crm(phone):
    await asyncio.sleep(random.uniform(0.2, 0.4))
    return {
        "phone": phone,
        "name": "John Doe",
        "vip": random.choice([True, False])
    }


# Mock Billing fetch
async def fetch_billing(phone):
    await asyncio.sleep(random.uniform(0.15, 0.35))

    # 10% chance of timeout error
    if random.random() < 0.1:
        raise TimeoutError("Billing system timeout")

    return {
        "status": "paid",
        "last_payment": "2026-02-25",
        "overdue": False
    }


# Mock Ticket history fetch
async def fetch_tickets(phone):
    await asyncio.sleep(random.uniform(0.1, 0.3))

    return {
        "complaints": [
            "slow internet",
            "router restart issue",
            "billing confusion"
        ]
    }


# Sequential fetch
async def fetch_sequential(phone):

    start = time.perf_counter()

    crm = await fetch_crm(phone)
    billing = await fetch_billing(phone)
    tickets = await fetch_tickets(phone)

    end = time.perf_counter()

    return CustomerContext(
        crm,
        billing,
        tickets,
        True,
        (end - start) * 1000
    )


# Parallel fetch
async def fetch_parallel(phone):

    start = time.perf_counter()

    results = await asyncio.gather(
        fetch_crm(phone),
        fetch_billing(phone),
        fetch_tickets(phone),
        return_exceptions=True
    )

    crm, billing, tickets = results

    data_complete = True

    if isinstance(crm, Exception):
        print("CRM fetch failed")
        crm = None
        data_complete = False

    if isinstance(billing, Exception):
        print("Billing fetch failed")
        billing = None
        data_complete = False

    if isinstance(tickets, Exception):
        print("Ticket fetch failed")
        tickets = None
        data_complete = False

    end = time.perf_counter()

    return CustomerContext(
        crm,
        billing,
        tickets,
        data_complete,
        (end - start) * 1000
    )


# Run test
async def main():

    phone = "9876543210"

    seq = await fetch_sequential(phone)
    print("Sequential time:", seq.fetch_time_ms, "ms")

    par = await fetch_parallel(phone)
    print("Parallel time:", par.fetch_time_ms, "ms")


if __name__ == "__main__":
    asyncio.run(main())
