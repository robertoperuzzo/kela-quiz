# Stage 1: build the Svelte app
FROM node:22-alpine AS builder

WORKDIR /build

# Copy app source
COPY app/package*.json ./
RUN npm ci

COPY app/ ./

# Copy extracted question data into public/ so it's bundled into dist/
COPY data/ ./public/data/

RUN npm run build

# Stage 2: serve with nginx
FROM nginx:alpine

# Remove default nginx content
RUN rm -rf /usr/share/nginx/html/*

# Copy built app
COPY --from=builder /build/dist /usr/share/nginx/html

# nginx config for SPA (serve index.html for all routes)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080
