# Electra-AI-E-Commerce-Shopping-Assistant 

A lightweight, web-based shopping assistant that helps customers find electronics through natural-language-style queries. Built with **Python, Flask, HTML, CSS, and JavaScript**, the application searches a fictional catalogue of 100 electronics products and displays matching items with prices, descriptions, and stock information.

## Overview

Electra provides a simple conversational interface for exploring an electronics catalogue without manually browsing through a spreadsheet. Customers can search by product name, category, features, or budget and receive relevant product suggestions.

The project demonstrates how a Python backend, a web frontend, and structured product data can work together to create an interactive shopping experience.

## Features

- **Interactive chat interface:** Ask product-related questions through a responsive web page.
- **Catalogue search:** Search 100 fictional electronics products across multiple categories.
- **Budget filtering:** Find products within a specified price limit.
- **Product recommendations:** Display matching products as cards with descriptions and prices.
- **Inventory information:** Show product IDs and available stock quantities.
- **REST API endpoint:** Process chat requests through a Flask JSON endpoint.
- **Health monitoring:** Check application status and the number of loaded products.
- **Responsive design:** Use the interface on desktop and mobile browsers.
- **Render deployment support:** Deploy the application as a public web service.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend logic and catalogue search |
| Flask | Web application and API endpoints |
| HTML5 | Frontend structure |
| CSS3 | Responsive styling and product cards |
| JavaScript | Chat interactions and asynchronous API requests |
| CSV | Product catalogue storage |
| Gunicorn | Production WSGI server |
| Render | Application hosting |

## Architecture

```text
Customer
   |
   v
Web Chat Interface
(HTML, CSS, JavaScript)
   |
   v
Flask Backend
   |
   v
Catalogue Search Engine
   |
   v
Fictional Electronics Catalogue
(100 Products, USD Pricing)
   |
   v
JSON Response
   |
   v
Product Recommendations
```

The frontend sends customer questions to the Flask backend. The backend searches the catalogue and returns matching products in JSON format, which the frontend renders as product cards.

**Current implementation:** Catalogue retrieval uses keyword matching, category synonyms, and basic budget detection. An LLM-based natural-language understanding layer is a planned extension rather than a feature of the current prototype.

## Product Catalogue

The application includes a fictional electronics catalogue with 100 products across 10 categories:

- Smartphones
- Laptops
- Tablets
- TVs and displays
- Audio equipment
- Gaming equipment
- Smart-home devices
- Cameras
- Networking equipment
- Accessories

Each product contains fields such as:

- Product ID
- Category
- Product name
- Brand
- Description
- Price in USD
- Stock quantity
- Supplier
- Reorder level
- Stock status

All product names, prices, suppliers, and inventory figures are fictional and intended for demonstration purposes.

## Example Queries

Customers can try questions such as:

- "Find laptops under $1,000."
- "Show me wireless headphones."
- "I'm looking for smart-home cameras."
- "What gaming accessories do you have?"
- "Find a router under $150."

The assistant returns matching catalogue entries when its search rules identify relevant products.

## Getting Started

### Prerequisites

- Python 3.10 or later
- pip
- Git (optional for local development)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/electra-shopping-assistant.git
cd electra-shopping-assistant
```

Replace `YOUR-USERNAME` and the repository name with your actual GitHub details.

### 2. Create a virtual environment

**Windows Command Prompt:**

```bat
py -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:10000
```

The application uses the `PORT` environment variable when available and defaults to port `10000`.

## API Endpoints

### `GET /`

Serves the shopping assistant's web interface.

### `POST /api/chat`

Accepts a customer question and returns a response with matching products.

**Example request:**

```json
{
  "message": "wireless headphones under $300"
}
```

**Example response structure:**

```json
{
  "message": "I found matching products in the catalogue.",
  "products": [
    {
      "Product_ID": "EL038",
      "Category": "Audio",
      "Product_Name": "SonicPods Pro",
      "Price_USD": "149",
      "Stock_Quantity": "24",
      "Description": "Wireless earbuds with active noise cancellation and charging case"
    }
  ]
}
```

The exact response depends on the catalogue search results and the query. The example above illustrates the response structure.

### `GET /health`

Returns the application's health status and the number of products loaded.

## Deployment on Render

The application can be deployed using Render's Web Service hosting.

1. Push the project files to a GitHub repository.
2. Create a new Web Service in Render.
3. Connect the GitHub repository.
4. Configure the build and start commands.

**Build command:**

```bash
pip install -r requirements.txt
```

**Start command:**

```bash
gunicorn app:app
```

5. Deploy the service and open the generated public URL.

For deployment guidance, consult the [Render Flask deployment documentation](https://render.com/docs/deploy-flask).

## Project Structure

```text
electra-shopping-assistant/
├── app.py
├── requirements.txt
├── README.md
├── fictional_electronics_catalogue_usd.csv
└── templates/
    └── index.html
```

- `app.py` — Flask application, catalogue loading, search logic, and API routes.
- `templates/index.html` — Chat interface and product-result rendering.
- `fictional_electronics_catalogue_usd.csv` — Fictional product dataset.
- `requirements.txt` — Python dependencies.

## Future Improvements

- Integrate an LLM API for more flexible natural-language understanding.
- Add structured filtering for product specifications, features, and price ranges.
- Implement retrieval-augmented generation (RAG) if catalogue complexity warrants it.
- Add conversational memory for follow-up questions.
- Introduce product comparison and personalized recommendations.
- Connect a live inventory database instead of relying on a static CSV.
- Add automated tests, input validation, and improved error handling.
- Add product images, shopping-cart functionality, and order-processing integrations.

## Limitations

This is a prototype intended to demonstrate catalogue search and conversational web interactions. It does not currently provide a fully integrated LLM, real-time inventory synchronization, purchasing, payment processing, or order fulfillment.

Search quality depends on the implemented matching rules, and results should not be treated as a substitute for a production e-commerce search system.

## License

Choose a license before distributing or reusing this project publicly. If you intend to make the repository open source, consider the [MIT License](https://choosealicense.com/licenses/mit/).

---

**Built with Python and Flask** to explore practical applications of conversational interfaces, product search, and lightweight web automation.
