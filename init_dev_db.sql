CREATE USER websiteuser WITH PASSWORD 'password';
CREATE DATABASE websitedb WITH OWNER websiteuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO websiteuser;