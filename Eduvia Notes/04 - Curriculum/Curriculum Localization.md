# Curriculum Localization

Eduvia supports native multi-language delivery, built primarily for bilingual English/Arabic deployment.

---

## Native JSONB Architecture

Rather than maintaining fragile localized duplicate tables, title and description columns use PostgreSQL `JSONB`:

```json
{
  "en": "Number Recognition",
  "ar": "التعرف على الأرقام"
}
```

- **Frontend Handling**: The UI components inspect the text object, prioritizing user language preference and rendering Arabic text with appropriate `dir="rtl"` and Arabic typography.
- **Extensibility**: Additional languages (French, Spanish) can be appended without executing database migrations.
