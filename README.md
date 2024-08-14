# JupiterOne CLI Client

A command-line interface (CLI) client for interacting with the JupiterOne API. This tool allows you to execute J1QL queries against your JupiterOne account and output the results in JSON or CSV format.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Command-Line Arguments](#command-line-arguments)
- [Examples](#examples)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.6 or later
- A JupiterOne account with an API token

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/jmountifield/jupiterone-cli-client.git
   cd jupiterone-cli-client
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install the CLI tool:

   ```bash
   pip install .
   ```

## Usage

Once installed, you can use the CLI client by running the `jupiterone-cli` command followed by the necessary arguments.

### Command-Line Arguments

- **`--account-id`** (Required): The ID of your JupiterOne account.
- **`--token`** (Required): Your API token for authentication.
- **`--api-url`** (Optional): The URL of the JupiterOne API. Defaults to `https://api.us.jupiterone.io`.
- **`--output`** (Optional): Output format, either `csv` or `json`. Defaults to `csv`.
- **`--include-deleted`** (Optional): Include deleted entities in the query results.
- **`query`** (Positional, Required): The J1QL query to execute.

### Examples

- **Basic Query with JSON Output**:

  ```bash
  jupiterone-cli --account-id your_account_id --token your_api_token "FIND * LIMIT 1" --output json
  ```

- **Query with CSV Output**:

  ```bash
  jupiterone-cli --account-id your_account_id --token your_api_token "FIND * LIMIT 1" --output csv > output.csv
  ```

- **Include Deleted Entities**:

  ```bash
  jupiterone-cli --account-id your_account_id --token your_api_token --include-deleted "FIND * LIMIT 1" --output json
  ```

### Output

- **JSON**: The results will be printed to stdout in JSON format.
- **CSV**: The results will be printed to stdout in CSV format. You can redirect the output to a file using `> output.csv`.

## Testing

Unit tests are provided to ensure the CLI client works as expected.

### Running Tests

1. Install the test dependencies:

   ```bash
   pip install coverage
   ```

2. Run the tests with coverage:

   ```bash
   coverage run -m unittest discover -s tests
   ```

3. Generate a coverage report:

   ```bash
   coverage report
   ```

4. Optionally, generate an HTML coverage report:

   ```bash
   coverage html
   ```

   Open `htmlcov/index.html` in your web browser to view the coverage details.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure your code is well-documented and covered by tests.

### Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/jmountifield/jupiterone-cli-client.git
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Make your changes and add tests as necessary.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

### Overview of the README Structure:

1. **Installation**: Instructions on how to install the CLI tool, including prerequisites.

2. **Usage**: Detailed information on how to use the CLI, including command-line arguments and examples.

3. **Testing**: Information on how to run the tests and check test coverage.

4. **Contributing**: Guidelines for contributing to the project, including how to set up a development environment.

5. **License**: Information about the licensing of the project.

This `README.md` should provide users and developers with a comprehensive understanding of the CLI client, how to use it, and how to contribute to its development.