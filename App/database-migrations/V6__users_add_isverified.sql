ALTER TABLE users
ADD COLUMN is_verified BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE users
ADD COLUMN verification_code VARCHAR(7);

-- Set is_verified to TRUE and verification_code to 'ABC-123' for existing users
UPDATE users
SET is_verified = TRUE,
    verification_code = 'ABC-123'
WHERE is_verified = FALSE OR verification_code IS NULL;

-- Enforce that verification_code is always exactly 7 characters
ALTER TABLE users
ADD CONSTRAINT verification_code_length CHECK (char_length(verification_code) = 7);
