# Flight Search Web Application

A Flask-based flight search web application that allows users to search for the cheapest flight deals using the Amadeus API
& set trip alerts that will notify users when a flight is available at a set price. 

## Features

- Search for flights by destination and origin cities.
- Set a trip alert that notifies users when flights are available (To be completed...).
- Specify flight details i.e. number of passengers, travel class, travel dates etc.
- View flight results with pricing and details.
- Communication with Amadeus Flight Offers API.
- Built with Flask, Bootstrap 5, Jinja2 templates, Flask-WTF, WTForms, Flask sessions, CSRF protection.
- Integrated with AWS services.
- AWS Cognito for authentication.
- AWS DynamoDB for saving flight details.
- AWS Lambda for executing flight search functions (To be completed...).
- AWS SNS for notifications by email (To be completed...).

## Requirements

- Python 3.8 or higher
- Amadeus API credentials

## Installation

1. Clone the git repository:
    ```bash
    git clone <git-url>
    cd flight-search-app
   ```

2. Install required packages:
    ```bash
    pip install -r requirements.txt
   ```
 
3. Open the .env file and add your Amadeus API credentials after getting your keys here: https://developers.amadeus.com/self-service/apis-docs/guides/developer-guides/quick-start/:
   - Getting Amadeus API Credentials:
     - Go to Amadeus for Developers
     - Create a free account
     - Create a new application to get your API key and secret
     - Use the test environment endpoints provided in the documentation

4. Execute the program and visit the IP Address shown on terminal:
    ```bash
    python main.py
    example: * Running on http://192.0.0.1:3002
   ```

## Troubleshooting

**Common Issues**
- API Authentication Errors:
  - Verify your Amadeus API credentials
  - Check that environment variables are properly set
  - Ensure you're using the API endpoints are correct

- Form Validation Errors:
  - Ensure all required fields are filled
  - Check dates and passenger counts 

- No Flight Results:
  - Verify city names are correct
  - Check that dates are in the future

**"Module not found" error?**
- Run `pip install -r requirements.txt` first

**Python not found?**
- Download Python from [python.org](https://python.org)
- Make sure to check "Add Python to PATH" during installation
- Alternative commands:
  ```bash
  python -m pip install -r requirements.txt
  or
  python3 -m pip install -r requirements.txt
  or
  py -m pip install -r requirements.txt
    ```
    ```bash
    py main.py
    ```

**Still having issues, try these:**
- Check Python version: `python --version`
- Ensure you're in the project directory
- Copy the error and paste on Google or a Gen A.I. tool.
- Open an issue on GitHub with your error message

## Disclaimer
***NB: This site is still under development and does not have a completion date***. 

***NB: Numerous improvements can made for it to become a production grade site***. 

***NB: This was constructed to merely display the developers capabilities in terms of software engineering knowledge and skills.***

***Site will be hosted on AWS in the near future to eliminate the need for others 
to create their own APIs and AWS configurations. A mini-production deployment of sorts***. 
