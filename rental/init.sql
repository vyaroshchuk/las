CREATE TYPE rental_status AS ENUM ('borrowed', 'retrieved');

CREATE TABLE "rental_records" (
    id SERIAL PRIMARY KEY,
    book_id VARCHAR(24) NOT NULL,
    user_id INTEGER NOT NULL,
    borrowed_date TIMESTAMPTZ,
    retrieved_date TIMESTAMPTZ,
    status rental_status NOT NULL
);

CREATE SEQUENCE rental_records_id_seq;