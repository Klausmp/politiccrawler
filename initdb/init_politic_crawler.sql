-- Create the database:
CREATE DATABASE "politicCrawler";

-- Create the user with a password:
CREATE USER "politicCrawler" WITH PASSWORD 'politicCrawler';

-- Allow the user to create additional databases (needed for Prisma's shadow DB):
ALTER USER "politicCrawler" CREATEDB;

-- Finally, grant all privileges on the new database to that user:
GRANT ALL PRIVILEGES ON DATABASE "politicCrawler" TO "politicCrawler";
