/* CREATE DB mlops */
CREATE DATABASE mlops;

/* SWITCH TO mlops DB */
\connect mlops

/* CREATE TABLE avatar_characters*/
CREATE TABLE IF NOT EXISTS avatar_characters (
    id SERIAL PRIMARY KEY,
    name TEXT,
    image TEXT,
    gender VARCHAR(20),
    eye_color VARCHAR(50),
    hair_color VARCHAR(100),
    skin_color VARCHAR(50)
);
