CREATE DATABASE netflix_db;

USE netflix_db;

CREATE TABLE netflix_titles (
    show_id VARCHAR(20),
    type VARCHAR(20),
    title VARCHAR(300),
    director TEXT,
    cast TEXT,
    country VARCHAR(200),
    date_added VARCHAR(50),
    release_year INT,
    rating VARCHAR(20),
    duration VARCHAR(50),
    listed_in TEXT,
    description TEXT
);
