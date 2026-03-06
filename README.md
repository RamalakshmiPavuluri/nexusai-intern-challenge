# nexusai-intern-challenge
NexusAI Intern Challenge – Async AI message handler, database schema, parallel data fetcher, and escalation decision engine.
# NexusAI Intern Challenge

## Project Overview

This project implements an AI-powered telecom customer support system that can analyze customer messages, fetch customer context data, and decide whether the AI can resolve the issue or escalate it to a human agent.

The project demonstrates async programming, database design, AI message handling, and automated testing.

---

## Project Structure

task1 → AI Message Handler
task2 → PostgreSQL database schema and repository
task3 → Parallel data fetching system
task4 → Escalation decision engine and pytest tests

---

## Installation

Install dependencies:

pip install -r requirements.txt

---

## Running Tasks

### Task 3 (Parallel Fetch Test)

python task3/fetcher.py

Example output:

Sequential time: ~650 ms
Parallel time: ~330 ms

This shows parallel execution improves performance significantly.

---

### Task 4 (Run Tests)

pytest task4/ -v

Expected output:

8 passed

---

## Rule Conflict Handling

When two escalation rules conflict, safety-critical rules take priority. For example, if the AI confidence is high but the intent is "service_cancellation", escalation still occurs. This is because cancellation requests are sensitive and require human confirmation.

Therefore, rule priority is determined by business risk. Customer retention issues or strong negative sentiment override confidence-based decisions.
