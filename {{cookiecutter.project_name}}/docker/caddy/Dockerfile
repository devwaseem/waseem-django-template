FROM caddy:2.7-builder-alpine AS builder
# Install tls plugin
# RUN xcaddy build --with github.com/caddy-dns/google-domains
FROM caddy:2.7-alpine
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
