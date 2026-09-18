# Eduvia — Security

## Principles

1. All secrets via environment variables — never hardcoded
2. JWT authentication for teacher/admin interfaces
3. Learner interface is teacher-managed (no learner credentials in MVP)
4. Input validation on all API endpoints via Pydantic
5. SQL injection prevention via SQLAlchemy ORM
6. CORS restricted to known origins

## Authentication

- JWT Bearer tokens for teacher/admin
- Access token: 60 min expiry (configurable)
- Refresh token: 7 days expiry (configurable)
- Passwords hashed with bcrypt

## Secrets Management

| Secret | Storage |
|--------|---------|
| Database password | Environment variable |
| JWT secret | Environment variable |
| Gemini API key | Environment variable |
| Qdrant API key | Environment variable |

## Data Privacy

- Learner profiles use display names (no real names required)
- No medical or sensitive health data stored
- No learner login credentials required in MVP
- Activity data retained for learning analytics only

## API Security

- Rate limiting (Phase 1+)
- Request validation via Pydantic
- Structured error responses (no stack traces in production)
- Centralized error handling

## Production Checklist

- [ ] APP_DEBUG=false
- [ ] Strong JWT_SECRET (min 32 random chars)
- [ ] Strong POSTGRES_PASSWORD
- [ ] CORS_ORIGINS restricted to production domain
- [ ] HTTPS enforced
- [ ] Gemini API key restricted to Eduvia project
