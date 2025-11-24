import os
import csv
import io
from celery import Celery
from .config import settings
import psycopg2
import redis
import json

celery_app = Celery('app', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

r = redis.Redis.from_url(settings.REDIS_URL)

@celery_app.task(bind=True)
def import_csv_task(self, local_path, job_id=None):
    conn = psycopg2.connect(dsn=settings.DATABASE_URL.replace('+psycopg2',''))
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products_staging (
      sku text,
      name text,
      description text,
      price numeric,
      active boolean
    );
    """)
    conn.commit()

    total = 0
    with open(local_path, 'r', encoding='utf-8') as f:
        total = sum(1 for _ in f) - 1

    processed = 0
    batch_size = 5000
    buffer = io.StringIO()

    with open(local_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            buffer.write('\t'.join([
                row.get('sku','') or '\\N',
                row.get('name','') or '\\N',
                row.get('description','') or '\\N',
                row.get('price','') or '\\N',
                row.get('active','true') or '\\N'
            ]) + '\n')

            if i % batch_size == 0:
                buffer.seek(0)
                cur.copy_from(buffer, 'products_staging', sep='\t',
                              columns=('sku','name','description','price','active'))
                conn.commit()
                buffer = io.StringIO()
                processed = i
                if job_id:
                    r.publish(f"job:{job_id}:progress",
                              json.dumps({"processed": processed, "total": total}))

        if buffer.tell() > 0:
            buffer.seek(0)
            cur.copy_from(buffer, 'products_staging', sep='\t',
                          columns=('sku','name','description','price','active'))
            conn.commit()
            processed = i
            if job_id:
                r.publish(f"job:{job_id}:progress",
                          json.dumps({"processed": processed, "total": total}))

    upsert_sql = """
    INSERT INTO products (sku, name, description, price, active)
    SELECT sku, name, description, price, COALESCE(active, true)
    FROM products_staging
    ON CONFLICT ((lower(sku)))
    DO UPDATE SET
      name = EXCLUDED.name,
      description = EXCLUDED.description,
      price = EXCLUDED.price,
      active = EXCLUDED.active;
    """
    cur.execute(upsert_sql)
    conn.commit()

    if job_id:
        r.publish(f"job:{job_id}:progress",
                  json.dumps({"processed": processed, "total": total, "status": "done"}))

    cur.execute("TRUNCATE products_staging;")
    conn.commit()
    cur.close()
    conn.close()
