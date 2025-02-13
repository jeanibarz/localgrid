# Minimal End-to-End Testing Project

This project provides a minimal setup for end-to-end testing of a multi-component application. It demonstrates how to integrate and test several essential resources in a local Docker environment using Docker Compose. The primary goal is to ensure that all components can interact correctly through a unified main application.

## Deployed and Tested Resources

During the end-to-end tests, the following resources are deployed and validated:

1. **PostgreSQL**  
   - **Test:** Create a table, insert a record, and retrieve it.
2. **Redis**  
   - **Test:** Set and retrieve a key-value pair.
3. **gRPC Server**  
   - **Test:** Invoke the `SayHello` RPC method which returns a greeting message.
4. **S3 (via LocalStack)**  
   - **Test:** Create a bucket, upload an object, and retrieve the object's content.
5. **Main Application**  
   - **Test:** Exposes an HTTP endpoint (`/run`) that orchestrates calls to all the above resources.

## Project Structure

```plaintext
my-project/
├── docker-compose.yml          # Defines all services (PostgreSQL, Redis, gRPC, LocalStack, Main App, Tests)
├── run_tests.sh              # Script for CI pipelines to run tests and tear down the stack
├── main-app/                   # Main application integrating all resources
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py                  # Flask application handling the integration logic
│   ├── service.proto           # Protocol definition for gRPC communication
│   └── grpc_client.py          # gRPC client to communicate with the gRPC server
├── grpc-server/                # gRPC service implementation
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── server.py               # gRPC server code
│   └── service.proto           # Protocol definition (same as in main-app)
└── tests/                      # End-to-end test suite using pytest
    ├── Dockerfile
    ├── requirements.txt
    └── test_e2e.py             # Pytest script to validate the full integration
```

## How to Run

### Locally

1. **Build and Start the Services**

   Navigate to the root directory (`my-project/`) and run:

   ```bash
   docker-compose up --build
   ```

   This command builds all the Docker images and starts the services defined in the `docker-compose.yml` file.

2. **Run End-to-End Tests**

   The `tests` container is configured to automatically run the pytest suite when started. If you need to run the tests separately, you can use:

   ```bash
   docker-compose run tests
   ```

   The tests will perform the following:
   - Call the `/run` endpoint of the main application.
   - Verify that PostgreSQL, Redis, gRPC, and S3 (LocalStack) operations complete successfully.
   - Validate that each service returns the expected output.

### Using Jenkins Pipelines

A `run_tests.sh` script is included to facilitate CI/CD integration with Jenkins. This script:

- Uses Docker Compose to build and start all services.
- Runs the tests container and aborts if any container exits.
- Captures the exit code from the tests container.
- Tears down the Docker Compose stack and removes volumes to ensure a clean state.
- Exits with the test's exit code, allowing Jenkins to determine if the build passed or failed.

Below is the content of `run_tests.sh`:

```bash
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
```

**To use in Jenkins:**

- Add a build step to execute `./run_tests.sh`.
- The script will run the entire end-to-end test suite and return the appropriate exit code for your pipeline.

## Devcontainer Configuration

This project includes a `.devcontainer` directory with configurations for developing inside a Docker container using VS Code.

### Using the Devcontainer

1.  **Install the Remote - Containers extension:** In VS Code, install the "Remote - Containers" extension.
2.  **Open the project in a container:** Open the project folder in VS Code. If you have the Remote - Containers extension installed, VS Code will detect the `.devcontainer` folder and prompt you to open the project in a container. Alternatively, you can use the "Remote-Containers: Reopen in Container" command from the VS Code command palette.

The devcontainer includes two services defined in `docker-compose.yml`: `main-app` and `tests`.

-   Use the `main-app` service when debugging the application's core functionality.
-   Use the `tests` service when debugging the tests themselves.

See the `.devcontainer/README.md` file for more details.

## Conclusion

This minimal project setup serves as a template for building and testing multi-component applications locally. It leverages Docker Compose to provide an isolated environment where services interact as they would in production, enabling robust end-to-end testing. With the added `run_tests.sh` script, integration into Jenkins pipelines is straightforward, ensuring that your CI/CD process can reliably test your infrastructure. Feel free to extend this project to include additional services or more complex interactions as needed.
