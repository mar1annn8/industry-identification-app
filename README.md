## industry-identification-app
Industry identification app that scrapes websites and uses the Gemini API to analyze content against a reference database for accurate classification.

# **Industry Analyzer Streamlit App**

This Streamlit app analyzes a company's website or manual description to identify its core products/services and classifies them into Primary, Secondary, or Tertiary industry sectors based on a custom database.

### _**How It Works**_

1. Input: A user provides a website URL or manually enters a description of products/services.

2. API Key: The user must enter a valid Gemini API key into the input field.

3. Scraping: If a URL is provided, the app uses requests and BeautifulSoup to scrape the visible text content from the page.

4. Analysis: The scraped text (or manual input) is sent to the Gemini API (gemini-2.5-pro-preview-09-2025).

5. AI Processing: A detailed system prompt instructs the model to:

- *Identify products/services.* 

- *Match them to the provided industry database.*

- *Classify each as Primary, Secondary, or Tertiary.*

- *Return a structured JSON response.*

6. Output: The app parses the JSON and displays the results in a table and a summary bar chart.
