import psycopg2

DB_CONFIG = {
    "dbname": "pdf",
    "user": "postgres",
    "password": 'student123',   
    "host": "localhost",
    "port": 5432
}

def save_to_db(original_name: str, processed_content: bytes) -> int:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO pdf_results (original_name, processed_data) VALUES (%s, %s) RETURNING id",
        (original_name, psycopg2.Binary(processed_content))
    )
    record_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return record_id