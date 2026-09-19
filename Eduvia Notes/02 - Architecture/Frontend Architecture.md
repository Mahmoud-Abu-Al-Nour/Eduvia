# Frontend Architecture

The Eduvia frontend (`frontend/src/`) is organized by feature domains rather than technical types:

```text
frontend/src/
├── app/            # App entry, router configuration, global providers
├── features/       # Feature modules:
│   ├── auth/       # AuthContext, LoginPage, ProtectedRoute
│   ├── curriculum/ # CurriculumBrowser, hierarchy components
│   ├── dashboard/  # Teacher dashboard layout & tabs
│   └── home/       # Marketing & landing page
├── services/       # Centralized api.ts client (Axios with interceptors)
├── hooks/          # Shared custom hooks (useHealth, useAuth)
└── types/          # Shared TypeScript interfaces
```

---

## Token & Authentication Interceptor

Authentication tokens are managed strictly through `frontend/src/services/api.ts`:
- Token Key: `eduvia_access_token` (with backward-compatible storage alias).
- Request Interceptor: Automatically injects `Authorization: Bearer <token>`.
- Response Interceptor: Catches `401 Unauthorized`, clears tokens, and redirects safely to `/login`.
- Standardized Promise unwrapping: `api.get<T>` and `api.post<T>` return unwrapped typed payload `T`.
