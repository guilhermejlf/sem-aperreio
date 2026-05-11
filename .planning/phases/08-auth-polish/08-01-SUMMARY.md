# Phase 8 - Backend Summary: Auth Polish

**Phase:** 08-auth-polish
**Plan:** 08-01 (backend)
**Status:** Completed
**Date:** 2026-05-11

## What Was Built

### UserProfile Model
- OneToOneField with User
- Fields: email_verified, verification_token, verification_token_expires, reset_token, reset_token_expires
- Migration 0007_userprofile created and applied

### RegisterSerializer Updates
- Password strength validation: min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
- password2 field for confirmation
- Creates UserProfile with unverified email on registration
- Sends verification email via SendGrid

### Custom LoginView
- Accepts "identifier" field (username or email)
- Auto-detects email by "@" symbol
- Blocks login if email_verified is False
- Returns friendly error message for unverified accounts

### Email Verification Endpoint
- GET /api/auth/verify-email/?token=xxx
- Validates token and expiration (48h)
- Activates account on success

### Password Reset Flow
- POST /api/auth/password-reset/ — sends email with token (24h expiration)
- POST /api/auth/password-reset/confirm/ — validates token and updates password
- Password strength validation on reset
- Generic response to prevent email enumeration

### Email Templates
- email_verification.html — dark theme, CTA button, expiration notice
- password_reset.html — dark theme, CTA button, expiration notice

### Files Modified
- api/models.py
- api/serializers_auth.py
- api/views_auth.py
- api/tasks.py
- api/urls.py
- api/migrations/0007_userprofile.py
- api/templates/emails/email_verification.html
- api/templates/emails/password_reset.html

## Verification
- [x] UserProfile model created and migrated
- [x] Register validates password strength and confirmation
- [x] Register creates unverified UserProfile and sends email
- [x] Login accepts username or email
- [x] Login blocks unverified accounts
- [x] Email verification endpoint works
- [x] Password reset request sends email
- [x] Password reset confirm updates password
- [x] All endpoints return appropriate status codes
