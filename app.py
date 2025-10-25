import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import time
import asyncio # Make sure asyncio is imported

# --- Setup Guide Content ---
# This text is from the README.md file to be displayed in the app.
SETUP_GUIDE_MARKDOWN = """
# Industry Analyzer Streamlit App

This Streamlit app analyzes a company's website or manual description to identify its core products/services and classifies them into Primary, Secondary, or Tertiary industry sectors based on a custom database.

## How It Works

1.  **Input:** A user provides a website URL or manually enters a description of products/services.
2.  **API Key:** The user must enter a valid Gemini API key into the input field.
3.  **Scraping:** If a URL is provided, the app uses `requests` and `BeautifulSoup` to scrape the visible text content from the page.
4.  **Analysis:** The scraped text (or manual input) is sent to the Gemini API (`gemini-2.5-pro-preview-09-2025`).
5.  **AI Processing:** A detailed system prompt instructs the model to:
    * Identify products/services.
    * Match them to the provided industry database.
    * Classify each as Primary, Secondary, or Tertiary.
    * Return a structured JSON response.
6.  **Output:** The app parses the JSON and displays the results in a table and a summary bar chart.

## Setup and Deployment on Streamlit Community Cloud

### 1. Create a GitHub Repository

1.  Create a new public repository on GitHub (e.g., `industry-analyzer`).
2.  Add the following three files to the repository:
    * `app.py` (the main Streamlit app code)
    * `requirements.txt` (the list of dependencies)
    * `README.md` (this file)

### 2. Get a Gemini API Key

1.  Go to the [Google AI Studio](https://aistudio.google.com/).
2.  Create a new API key.
3.  Copy this key. It will be pasted into the app's UI after deployment.

### 3. Deploy on Streamlit Community Cloud

1.  Sign up for or log in to [Streamlit Community Cloud](https://share.streamlit.io/).
2.  Click the "**New app**" button.
3.  **Deploy from an existing repo:**
    * **Repository:** Select the GitHub repository created in Step 1.
    * **Branch:** Select the main branch (e.g., `main` or `master`).
    * **Main file path:** Enter `app.py`.
4.  Click the "**Deploy!**" button.
5.  Once the app is deployed, it will ask for the Gemini API key directly in the user interface. Paste the key obtained in Step 2 into this field to use the app.
"""

# --- Database from Prompt ---
INDUSTRY_DATABASE = """
- Adult Products: Products related to adult entertainment and intimacy (Adult toys, lingerie, sexual wellness products)
- Agriculture & Environment: Farming, natural resource management, sustainability (Crop production, livestock, forestry, fisheries, conservation, renewable energy (solar, wind, hydro), environmental protection)
- Performing Artis & Cultural Experiences: Creative expression, entertainment, cultural experiences (Theater, dance, and a wide of activities, including concerts, festivals, museums, and other cultural attractions.)
- Visual Arts & Entertainment: Creative expression, entertainment, cultural experiences (Visual arts, film, television, gaming)
- Autos & Vehicles: Design, manufacturing, and sales of automobiles and other vehicles (Cars, trucks, motorcycles, buses, recreational vehicles (RVs))
- Beauty & Fitness: Personal care, appearance enhancement, physical well-being (Cosmetics, skincare, hair care, salons, spas, gyms, fitness studios, personal training)
- Business & Industrial: Commercial activities, manufacturing, production, and professional services (Manufacturing, construction, energy (fossil fuels, utilities), logistics, wholesale, retail, consulting, legal services, accounting, B2B services)
- Computers & Electronics: Technology, computing, and electronic devices (Hardware (computers, smartphones, peripherals), software, IT services, consumer electronics (TVs, audio equipment))
- Fashion: Clothing, footwear, accessories, and style (Apparel design, manufacturing, retail, fashion shows, modeling)
- Finance: Money management, investments, banking, and financial services (Banking, investment banking, insurance, financial planning, accounting, wealth management)
- Firearms & Weapons: Firearms, ammunition, and related equipment (Guns, rifles, pistols, ammunition, hunting gear, self-defense equipment)
- Food & Beverage: Production, distribution, and sale of food and drinks (Restaurants, cafes, food manufacturing, grocery stores, beverage production (alcoholic and non-alcoholic))
- Gifts & Shopping: Retail, e-commerce, and consumer goods (Gift shops, department stores, online retailers, specialty stores)
- Health & Wellness: Healthcare, personal well-being, alternative medicine (Hospitals, clinics, pharmacies, mental health services, alternative therapies (acupuncture, massage), nutritional supplements, alternative health products (Kratom, where legal))
- Hobbies & Leisure: Recreational activities, interests, and pastimes (Arts and crafts, collecting, gaming, sports, travel, reading, gardening)
- Home & Garden: Home improvement, décor, gardening, and outdoor living (Furniture, appliances, home décor, gardening supplies, landscaping)
- Hospitality & Travel: Accommodation, tourism, and travel services (Hotels, resorts, airlines, travel agencies, restaurants, entertainment venues)
- Internet & Telecommunications: Digital communication, online services, and network infrastructure (Internet service providers (ISPs), telecommunications companies, social media platforms, online content providers)
- Jobs & Education: Employment, training, and education (Recruitment, staffing, training, schools, universities, online learning platforms)
- Kids & Family: Products and services for children and families (Toys, children's clothing, childcare, family entertainment, parenting resources)
- Law & Government: Legal services, public administration, and policy (Law firms, government agencies, courts, legal aid organizations)
- Lifestyle: Personal interests, values, and way of living (Fashion, beauty, travel, food, home décor, hobbies)
- Logistics & Transportation: Movement of goods and people (Shipping, trucking, warehousing, airlines, railways, public transportation)
- Marketing: Promoting products, services, or ideas (Market research, advertising, branding, public relations, content marketing, digital marketing, sales)
- Media & Communications: Information dissemination, journalism, public relations (Journalism, publishing, broadcasting, telecommunications, public relations, content creation)
- Medical Cannabis: Cannabis for medical use (Dispensaries, cultivation, medical marijuana products)
- News: Current events and information (Newspapers, magazines, television news, online news portals, radio)
- Not For Profit: Charitable organizations and social causes (Charities, foundations, NGOs, social advocacy groups)
- People & Society: Social issues, community, and culture (Social services, community organizations, advocacy groups, cultural institutions)
- Pets & Animals: Pet care, animal welfare, and related products and services (Pet food, pet supplies, veterinary services, animal shelters, zoos)
- Real Estate: Property, land, and buildings (Residential, commercial, and industrial real estate, property development, real estate brokerage, property management)
- Recreational Cannabis: Cannabis for recreational use (where legal) (Dispensaries, cannabis products, consumption lounges (where permitted))
- Science: Research, discovery, and innovation (Scientific research institutions, laboratories, technology companies, academic departments)
- Specialty Products: Unique, niche, or regulated goods (Antiques, collectibles, art, luxury goods, specialized equipment)
- Vices & Adult Entertainment: Activities and products considered taboo or morally questionable (Gambling, adult entertainment venues, pornography, tobacco, alcohol)
- Other: Any industry not explicitly categorized above
"""

# --- System Prompt for Gemini ---
SYSTEM_PROMPT = f"""
You are an expert business analyst. The task is to analyze a company's description (from their website text or a manual description) and categorize their products/services.

Follow these steps:
1.  Identify the core products or services described in the user's text.
2.  For each identified product/service, match it to the *most relevant* category from the 'Industry Database' provided below.
3.  For each matched category, classify it as 'Primary', 'Secondary', or 'Tertiary' based on these economic definitions:
    * **Primary:** Involves the extraction and harvesting of raw materials (e.g., farming, mining, fishing, forestry).
    * **Secondary:** Involves manufacturing, processing, and construction (e.g., car manufacturing, food production, building).
    * **Tertiary:** Involves providing services (e.g., retail, finance, healthcare, software, entertainment, consulting).
4.  Return the analysis in a structured JSON format. The JSON should be an object with a single key "services", which is a list of objects. Each object in the list should have three keys: "name" (the identified product/service), "category" (the category from the database), and "sector" (Primary, Secondary, or Tertiary).

Example of a valid JSON output:
{{"services": [
    {{"name": "Smartphone Sales", "category": "Computers & Electronics", "sector": "Tertiary"}},
    {{"name": "Software Development", "category": "Computers & Electronics", "sector": "Tertiary"}},
    {{"name": "Crop Production", "category": "Agriculture & Environment", "sector": "Primary"}}
]}}

Here is the Industry Database:
{INDUSTRY_DATABASE}
"""

# --- Helper Functions ---

def scrape_website_text(url):
    """
    Scrapes the visible text from a given URL.
    Returns the text content or an error message.
    """
    try:
        # Add a simple header to pretend to be a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style tags
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        cleaned_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Limit the text to avoid sending too much to the API
        return cleaned_text[:4000]
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        st.error(f"Error parsing website: {e}")
        return None

async def call_gemini_api(user_text, api_key):
    """
    Calls the Gemini API with the scraped text and returns the JSON analysis.
    Implements exponential backoff for retries.
    """
    if not api_key:
        st.error("API Key is not set. Please add it to the Streamlit Secrets.")
        return None

    # --- MODEL UPDATED TO 2.5 PRO ---
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-preview-09-2025:generateContent?key={api_key}"
    
    user_query = f"Please analyze the following company information: {user_text}"

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "generationConfig": {
            "responseMimeType": "application/json",
        }
    }

    max_retries = 5
    delay = 1  # Start with 1 second delay

    for attempt in range(max_retries):
        try:
            # Use a session for requests, which can be more efficient
            with requests.Session() as session:
                response = session.post(api_url, json=payload, headers={'Content-Type': 'application/json'})
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            
            result = response.json()
            
            candidate = result.get("candidates", [])[0]
            if candidate:
                text_content = candidate.get("content", {}).get("parts", [])[0].get("text", "")
                if text_content:
                    # The response is expected to be a JSON string
                    return json.loads(text_content)
            
            st.error("Failed to get a valid response from the API. The response might be empty or malformed.")
            return None

        except requests.exceptions.HTTPError as e:
            if e.response.status_code in [429, 500, 503]:
                # Rate limit or server error, wait and retry
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                st.error(f"HTTP Error: {e}")
                st.json(e.response.json()) # Show error details
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Request Error: {e}. Retrying...")
            time.sleep(delay)
            delay *= 2
        except json.JSONDecodeError:
            st.error("API did not return valid JSON. The output may be malformed.")
            # Log the raw response for debugging if possible
            try:
                st.text_area("Raw API Response:", value=response.text, height=150)
            except NameError:
                pass # response object might not be available
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            return None
            
    st.error("Failed to get a response from the API after several retries.")
    return None

# --- Streamlit App UI ---

st.set_page_config(layout="wide", page_title="Industry Sector Analyzer")

st.title("Industry Sector Analyzer")
st.markdown("Enter a website URL to automatically scan its content, or manually describe the company's products/services. The app will categorize them into Primary, Secondary, or Tertiary industries.")

# --- Added Collapsible Setup Guide ---
with st.expander("Show Setup Guide and Instructions"):
    st.markdown(SETUP_GUIDE_MARKDOWN)

# API Key Input
# This section is modified to remove Streamlit Secrets and use a direct text input.
GEMINI_API_KEY = st.text_input("Enter the Gemini API Key:", type="password")

if not GEMINI_API_KEY:
    st.warning("Please enter a Gemini API Key to proceed.")
    st.stop()


col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input Method 1: Scan Website")
    website_url = st.text_input("Enter website URL (e.g., https://www.apple.com):")
    scan_button = st.button("Scan and Analyze Website")

with col2:
    st.subheader("Input Method 2: Manual Input")
    manual_services = st.text_area("Core products/services (one per line):", height=120)
    manual_button = st.button("Analyze Manual Input")

# --- Logic to handle button clicks ---

analysis_input = None
if scan_button and website_url:
    with st.spinner(f"Scanning {website_url}... This may take a moment."):
        scraped_text = scrape_website_text(website_url)
        if scraped_text:
            analysis_input = scraped_text
            st.session_state['analysis_input'] = scraped_text
            st.session_state['analysis_complete'] = False

elif manual_button and manual_services:
    analysis_input = manual_services
    st.session_state['analysis_input'] = manual_services
    st.session_state['analysis_complete'] = False

# --- Perform Analysis and Display Results ---

if 'analysis_input' in st.session_state and not st.session_state.get('analysis_complete', False):
    st.divider()
    st.subheader("Analysis Results")
    
    with st.spinner("Analyzing content and classifying industries..."):
        # Run the async function using asyncio.run()
        analysis_result = asyncio.run(call_gemini_api(st.session_state['analysis_input'], GEMINI_API_KEY))
        
        if analysis_result and "services" in analysis_result:
            st.session_state['analysis_result'] = analysis_result["services"]
            st.session_state['analysis_complete'] = True
        else:
            st.error("Analysis failed. The API did not return the expected data format.")
            st.session_state['analysis_complete'] = True # Stop retrying

# Display the results if they exist in the session state
if st.session_state.get('analysis_complete', False) and 'analysis_result' in st.session_state:
    results = st.session_state['analysis_result']
    
    if results:
        st.dataframe(results, use_container_width=True)
        
        st.divider()
        st.subheader("Summary by Sector")
        
        # Pie chart data
        primary_count = sum(1 for item in results if item['sector'] == 'Primary')
        secondary_count = sum(1 for item in results if item['sector'] == 'Secondary')
        tertiary_count = sum(1 for item in results if item['sector'] == 'Tertiary')
        
        sector_data = {
            'Sector': ['Primary', 'Secondary', 'Tertiary'],
            'Count': [primary_count, secondary_count, tertiary_count]
        }
        
        if sum(sector_data['Count']) > 0:
            st.bar_chart(sector_data, x='Sector', y='Count')
        else:
            st.info("No sectors were identified.")
            
    else:
        st.info("No products or services were identified from the provided content.")

# Show the text that was analyzed
if 'analysis_input' in st.session_state:
    with st.expander("Show Analyzed Text"):
        st.text(st.session_state['analysis_input'])

