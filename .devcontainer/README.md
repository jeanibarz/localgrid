# Debugging in the Devcontainer

This devcontainer includes two services: `main-app` and `tests`.

- Use the `main-app` service when debugging the application's core functionality, business logic, or any code related to the main application itself. This is the default service VS Code connects to and is configured to run the main application code.

- Use the `tests` service when debugging the tests themselves, investigating test failures, or developing new tests. This service is specifically designed for running tests and might have different dependencies or configurations optimized for testing.

In essence, the choice depends on whether you are debugging the application code or the tests.
