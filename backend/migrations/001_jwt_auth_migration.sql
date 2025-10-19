-- Migration: Add JWT authentication support to users table
-- Date: 2024
-- Description: Add password_hash, full_name, provider_user_id fields
--              Make firebase_uid nullable for new auth system

-- Add new columns for JWT authentication
ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR;
ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR;
ALTER TABLE users ADD COLUMN IF NOT EXISTS provider_user_id VARCHAR;

-- Make firebase_uid nullable (for users not migrated from Firebase)
ALTER TABLE users ALTER COLUMN firebase_uid DROP NOT NULL;

-- Add index on provider_user_id for OAuth lookups
CREATE INDEX IF NOT EXISTS idx_users_provider_user_id ON users(provider_user_id);

-- Add composite index for provider + provider_user_id lookups
CREATE INDEX IF NOT EXISTS idx_users_provider_lookup ON users(provider, provider_user_id);

-- Set default provider to 'email' for existing users without a provider
UPDATE users SET provider = 'email' WHERE provider IS NULL;

-- Update display_name to full_name for existing users
UPDATE users SET full_name = display_name WHERE full_name IS NULL AND display_name IS NOT NULL;

-- Add comments for documentation
COMMENT ON COLUMN users.password_hash IS 'Bcrypt hashed password for email/password authentication';
COMMENT ON COLUMN users.full_name IS 'User full name (replaces display_name)';
COMMENT ON COLUMN users.provider_user_id IS 'OAuth provider unique user ID (e.g., Google sub, Facebook id)';
COMMENT ON COLUMN users.provider IS 'Authentication provider: email, google, facebook, twitter, instagram';
