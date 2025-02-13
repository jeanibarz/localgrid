#!/bin/bash
# Run tests using docker-compose and capture the exit code
docker-compose up --build --abort-on-container-exit --exit-code-from tests tests
RESULT=$?

# Tear down the stack and remove all volumes to ensure a clean state
docker-compose down -v

# Optionally, prune any dangling volumes (uncomment if needed)
# docker volume prune -f

# Exit with the test's exit code so Jenkins can use it
exit $RESULT
