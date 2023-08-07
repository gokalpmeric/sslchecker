# SSL Certificate Expiry Checker

This project provides a web interface and API to check and monitor the expiration dates of SSL certificates for specified domains.

## Features

- Web interface to add, view, and delete monitored domains.
- Automatic daily checks of SSL certificate expiration dates.
- Alerting via color coding for certificates expiring in less than 40 days.
- Ability to query certificate expiration date via API.

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Flask
- certifi

### Setup

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-username/ssl-certificate-checker.git
    cd ssl-certificate-checker
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**

    ```bash
    python app.py
    ```

   Once running, the application will be accessible at [http://0.0.0.0:5000](http://0.0.0.0:5000).

## Usage

### Web Interface

- **Add a Domain**: Simply enter a domain name and click "Check" to add it to the monitored list.
- **View Domains**: See a list of monitored domains and their expiration dates.
- **Delete a Domain**: Use the "Delete" option next to a domain to remove it from the monitored list.

### API

You can also check the SSL certificate expiration date for a domain via the API.

#### Check Certificate Expiration Date

- **Endpoint**: `/api/check`
- **Method**: POST
- **Request Body**: A JSON object containing the domain name.

    ```json
    {
        "domain": "www.example.com"
    }
    ```

- **Response**: A JSON object containing the domain name and its expiration date.

    ```json
    {
        "domain": "www.example.com",
        "expiration_date": "2023-09-12 03:38:41"
    }
    ```

- **Example cURL Command**:

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"domain": "www.example.com"}' http://0.0.0.0:5000/api/check
    ```

## Contributing

For those interested in contributing, please fork the project, create a feature branch, and then submit a pull request once your changes are complete.

## License

This project is licensed under the MIT License.

## Acknowledgements

