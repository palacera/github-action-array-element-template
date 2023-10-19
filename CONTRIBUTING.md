# Contributing

## Setup

### Select Python SDK (for IntelliJ IDEA on Mac)

If not already set, select the SDK to use for the project.
1. Click `File` > `Project Structure...`
2. Under the  `Project Settings` menu, select `Project` 
3. For `SDK`, select `Python 3.11` or greater version
4. Click `OK`

## Code Check

### Install Ruff

This example shows how to install Ruff on macOS using Homebrew. If you use a different operating system, you will need to install Ruff using the appropriate package manager.

```
brew install ruff
```

See [Ruff installation](https://docs.astral.sh/ruff/installation/) for more information.

### Run Checks
```
ruff check .
```

Or, if using IntelliJ IDEA, you can run `lint-check-all` from the `Run / Debug Configurations` dropdown menu.

### Run Checks and Fix
```
ruff check --fix .
```

Or, if using IntelliJ IDEA, you can run `lint-fix-all` from the `Run / Debug Configurations` dropdown menu.

### Lint Check Configuration

The lint check configuration for this project can be found in the `ruff.toml` file located in the root directory.

See the [Ruff website](https://docs.astral.sh/ruff/) for full documentation.


## Testing

### Install pytest

```
pip install -U pytest
```

Note: pytest requires Python 3.7+ or PyPy3

### Run tests

```
pytest test
```

Or, if using IntelliJ IDEA, you can run `test-all` from the `Run / Debug Configurations` dropdown menu.

See the [pytest website](https://docs.pytest.org/) for full documentation.
