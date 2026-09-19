# ─────────────────────────────────────────────────────────────
# Eduvia Frontend — Multi-stage Dockerfile
# ─────────────────────────────────────────────────────────────

# ── Stage 1: Development ───────────────────────────────────────
FROM node:20-alpine AS development

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source
COPY . .

EXPOSE 5173

# Development: Vite dev server with hot reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# ── Stage 2: Build ─────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production=false

COPY . .
RUN npm run build

# ── Stage 3: Production (nginx) ────────────────────────────────
FROM nginx:alpine AS production

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx config for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 8080

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD wget -qO- http://localhost:80/ || wget -qO- http://localhost:8080/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
