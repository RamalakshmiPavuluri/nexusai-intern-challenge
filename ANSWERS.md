# Q1: Handling Partial Transcripts from STT

When the speech-to-text (STT) system sends partial transcripts every 200ms, querying the database on every partial result would be inefficient and could overload the backend systems. Instead, I would implement a hybrid approach. The system would analyze partial transcripts locally to detect potential intents, but only trigger database queries when a stable or meaningful phrase is detected. For example, if the transcript contains keywords like "internet down", "billing issue", or "cancel service", the system could begin fetching relevant customer data in the background.

This approach reduces latency because the system can prefetch necessary data before the user finishes speaking. However, it also avoids excessive database queries for incomplete sentences. Another safeguard would be debouncing requests so the database is queried only once within a short interval unless the detected intent changes significantly.

The trade-off is balancing responsiveness with system load. Starting queries early can improve response time for the AI assistant, but doing it too frequently can increase infrastructure costs and degrade performance. Therefore, intelligent intent detection combined with rate-limiting database calls provides the best compromise.

---

# Q2: Risks of Auto-Adding Resolutions to the Knowledge Base

Automatically adding resolutions with CSAT ≥ 4 to the knowledge base may seem efficient, but it introduces several risks over time.

First, incorrect or context-specific solutions could enter the knowledge base. A resolution that works for one customer's issue might not apply broadly. Over six months, this could create a large collection of inaccurate or misleading solutions, reducing the reliability of the knowledge base. To prevent this, a validation step should be introduced where new entries are reviewed or automatically clustered with similar solutions before becoming official knowledge base articles.

Second, CSAT scores may not accurately reflect the technical quality of the solution. Customers sometimes give high satisfaction ratings simply because the agent was polite, even if the underlying issue was not fully resolved. Over time, this could allow ineffective solutions into the system. To mitigate this, additional metrics such as issue recurrence rate or resolution confirmation should be included before adding solutions automatically.

By combining CSAT with technical validation and monitoring repeat issues, the knowledge base can remain accurate and useful.

---

# Q3: Handling an Angry Customer Wanting Cancellation

When a customer says, "I've been without internet for 4 days, I called 3 times already, your company is useless and I want to cancel right now," the system should immediately detect multiple escalation signals.

First, sentiment analysis would detect strong negative sentiment, triggering the "angry_customer" escalation rule. Second, the intent "service_cancellation" would also activate a rule that always escalates the conversation to a human agent.

The AI should respond calmly and empathetically before transferring the call. For example: "I'm really sorry you've experienced this issue for so long. I understand how frustrating that must be. Let me connect you to a specialist who can resolve this immediately."

While escalating, the AI should pass important context to the human agent. This includes the customer’s phone number, account details, billing status, previous complaints, and the transcript of the conversation. It should also highlight that the customer reported multiple prior calls and prolonged service downtime.

Providing this context ensures the human agent can continue the conversation without asking the customer to repeat information, improving the customer experience.

---

# Q4: One Improvement to the System

One major improvement I would add is a real-time context memory system for customer interactions. Currently, the system retrieves customer data from multiple services during each call, but it does not maintain long-term conversational context across sessions.

The improvement would involve storing structured summaries of past interactions, including detected intents, resolutions attempted, and escalation outcomes. When a customer contacts support again, the AI could instantly understand the history of previous issues and responses.

For example, if the same internet outage problem occurred three times in a week, the system could automatically prioritize escalation or suggest a technician visit. This would prevent repetitive troubleshooting steps and significantly improve customer satisfaction.

To implement this, a lightweight context storage layer could be built on top of the existing database, storing summarized conversation metadata. Machine learning models could also analyze patterns in customer complaints to predict recurring problems.

Success of this feature could be measured using metrics such as reduced average handling time, fewer repeat complaints, and higher customer satisfaction scores.
