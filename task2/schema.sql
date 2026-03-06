CREATE TABLE call_records (
    id SERIAL PRIMARY KEY,
    customer_phone VARCHAR(20) NOT NULL,
    channel VARCHAR(20) NOT NULL,
    transcript TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    outcome VARCHAR(20),
    confidence_score FLOAT CHECK (confidence_score BETWEEN 0 AND 1),
    csat_score INT CHECK (csat_score BETWEEN 1 AND 5),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration INT
);

-- Index for fast search by phone number
CREATE INDEX idx_phone ON call_records(customer_phone);

-- Index for time based queries (recent calls)
CREATE INDEX idx_timestamp ON call_records(timestamp);

-- Index for filtering by outcome
CREATE INDEX idx_outcome ON call_records(outcome);
