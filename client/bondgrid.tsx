# NodeJS base image
FROM nexus-amazon-dev-docker-registry.barclays.intranet/barclays-int-ibdsp/ubi8-nodejs_18:latest

# Replace the following with your team's email address
# MAINTAINER your-email@barclays.com
LABEL maintainer="your-email@barclays.com"
LABEL prisma_email_alert="your-email@barclays.com"

# Set working directory
WORKDIR /usr/app

# Copy package files first (for better caching)
COPY ["package.json", "package-lock.json", "./"]

# Install app dependencies
RUN echo "Application install: start." && npm install && npm ci

# Add the source files
COPY . .

# NOTE: We do NOT run `npm run build` here because React needs REACT_APP_THEME injected at runtime

# Optional: Prepare for server logic (safe check for future)
WORKDIR /usr/app/build/server
RUN echo "Server install: start." && \
  if [ -f package.json ]; then \
    npm ci --production; \
  else \
    echo "No server package.json found, skipping install."; \
  fi

# Expose app port
EXPOSE 3002

# Switch to non-root user
USER 5000

# Build React app at runtime (after env vars like REACT_APP_THEME are injected)
ENTRYPOINT [ "sh", "-c", "echo \"Building React app with theme=$REACT_APP_THEME\" && cd /usr/app && npm run build && node server" ]
