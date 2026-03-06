import asyncpg

class CallRecordRepository:

    def __init__(self, db_url):
        self.db_url = db_url

    async def save(self, call_data: dict):
        conn = await asyncpg.connect(self.db_url)

        query = """
        INSERT INTO call_records(
            customer_phone, channel, transcript, ai_response,
            outcome, confidence_score, csat_score, duration
        )
        VALUES($1,$2,$3,$4,$5,$6,$7,$8)
        """

        await conn.execute(
            query,
            call_data["customer_phone"],
            call_data["channel"],
            call_data["transcript"],
            call_data["ai_response"],
            call_data["outcome"],
            call_data["confidence_score"],
            call_data.get("csat_score"),
            call_data["duration"]
        )

        await conn.close()

    async def get_recent(self, phone: str, limit: int = 5):

        conn = await asyncpg.connect(self.db_url)

        query = """
        SELECT * FROM call_records
        WHERE customer_phone=$1
        ORDER BY timestamp DESC
        LIMIT $2
        """

        rows = await conn.fetch(query, phone, limit)

        await conn.close()

        return [dict(row) for row in rows]
    async def get_low_resolution_intents(conn):

    query = """
    SELECT transcript AS intent,
           COUNT(*) FILTER (WHERE outcome='resolved')::float /
           COUNT(*) AS resolution_rate,
           AVG(csat_score) AS avg_csat
    FROM call_records
    WHERE timestamp >= NOW() - INTERVAL '7 days'
    GROUP BY transcript
    ORDER BY resolution_rate ASC
    LIMIT 5;
    """

    rows = await conn.fetch(query)

    return [dict(row) for row in rows]
