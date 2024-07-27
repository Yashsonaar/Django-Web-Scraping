# 🖥️ Gaming Laptop Recommendation System

## Overview

This project is a Django-based web application that scrapes data about gaming laptops from Flipkart, displays the laptops with their details, and provides recommendations based on cosine similarity. Users can search for laptops by name or price and set price alerts.

## Features

- 🕸️ Web scraping of gaming laptop data from Flipkart.
- 📋 Displaying laptops with their details (name, price, description).
- 🔍 Search functionality for filtering laptops by name or price.
- 🤖 Recommendations based on cosine similarity of laptop descriptions.
- 📄 Pagination for navigating through the list of laptops.
- 📧 Buttons to send email notifications and set price alerts.
- 📂 Mailing the scraped data as a CSV or PDF file with a single click.
- 📬 Sending an email alert when a set price is reached.

## Technologies Used

- 🐍 Django: Backend framework
- 🍲 BeautifulSoup: Web scraping library
- 🌐 Requests: HTTP library for making requests
- 🐼 Pandas: Data manipulation and analysis
- 📊 Scikit-learn: Machine learning library for cosine similarity
- 🎨 Bootstrap: Frontend framework for styling

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Yashsonaar/Django-Web-Scraping.git
    cd gaming-laptop-recommendation
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

6. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:8000`.

## Usage

1. **Scrape Data:**

    The application automatically scrapes data from Flipkart when accessed. Make sure you have an active internet connection.

2. **Search for Laptops:**

    Use the search bar to filter laptops by name or price.

3. **View Recommendations:**

    After performing a search, the application provides recommendations based on cosine similarity of laptop descriptions.

4. **Pagination:**

    Navigate through the list of laptops using the pagination controls at the bottom of the page.

5. **Send Email and Set Price Alerts:**

    Use the provided buttons to send email notifications or set price alerts.

6. **Mail Scraped Data:**

    Click the button to send the scraped data as a CSV or PDF file.

7. **Price Alert Emails:**

    Once a price alert is set, an email will be sent when the target price is reached.

## Project Structure

- `scrape_data` view: Scrapes data from Flipkart and handles search functionality.
- `index.html` template: Displays the list of laptops, search form, and recommendations.
- `models.py`: Defines the `Gaminglaptop` model to store laptop details.

## Contributing

1. 🍴 Fork the repository.
2. 🌿 Create a new branch: `git checkout -b feature-branch`
3. 💻 Make your changes and commit them: `git commit -m 'Add some feature'`
4. 🚀 Push to the branch: `git push origin feature-branch`
5. 🔄 Open a pull request.

## Acknowledgments

- 🙏 Thanks to Flipkart for providing the data used in this project.
- 🙌 Thanks to the open-source community for the libraries and tools used.
