CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(16) NOT NULL,
    password VARCHAR(50) NOT NULL
);

INSERT INTO "user" (username, password) VALUES
('admin', 'admin'),
('reader', 'reader');