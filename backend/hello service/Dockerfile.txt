# --- deps ---
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# --- runner ---
FROM node:18-alpine
ENV NODE_ENV=production
WORKDIR /helloService
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV PORT=7201
EXPOSE 7201
# Optional healthcheck (expects /health route)
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD wget -qO- http://localhost:7201/health || exit 1
# If your app starts via npm start, use the npm CMD instead
CMD ["node", "server.js"]
