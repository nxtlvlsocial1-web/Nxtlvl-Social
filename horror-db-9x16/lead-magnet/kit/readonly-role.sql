-- Run once on production, as the owner. Day-to-day, connect as dev_readonly.
CREATE ROLE dev_readonly LOGIN PASSWORD 'change-me';
GRANT CONNECT ON DATABASE app TO dev_readonly;
GRANT USAGE ON SCHEMA public TO dev_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO dev_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO dev_readonly;
