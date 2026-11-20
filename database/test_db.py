import psycopg2

conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_YPutR6wViH3L@ep-square-star-be6fg2ub-pooler.c-9.us-east-2.aws.neon.tech/neondb?sslmode=require"
)

print("Connected to Neon!")