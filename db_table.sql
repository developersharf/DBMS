--lost_lostitem Table

CREATE TABLE lost_lostitem (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(254) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    date_lost DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    submitted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

--found_founditem Table

CREATE TABLE found_founditem (
    id SERIAL PRIMARY KEY,
    finder_email VARCHAR(254) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    date_found DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    submitted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
