## ADDED Requirements

### Requirement: Multi-stage Docker build
The deployment SHALL use a multi-stage Dockerfile that builds the Svelte app and serves it with nginx.

#### Scenario: Docker build produces a working image
- **WHEN** `docker build` is run in the project root
- **THEN** the resulting image contains the built Svelte app and JSON data files, served by nginx on port 80

### Requirement: Docker Compose for easy deployment
The deployment SHALL include a `docker-compose.yaml` for single-command deployment.

#### Scenario: Start the app with docker compose
- **WHEN** a user runs `docker compose up -d` in the project root
- **THEN** the quiz webapp is accessible on the configured port (default: 8080)

### Requirement: JSON data files are included in the image
The deployment SHALL bundle the `data/*.json` files into the Docker image so the app is self-contained.

#### Scenario: App works without external file mounts
- **WHEN** the Docker container starts without any volume mounts
- **THEN** the webapp loads exams from the bundled JSON files and functions correctly
