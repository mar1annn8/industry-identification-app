import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import time
import asyncio # Make sure asyncio is imported

# --- Page Configuration ---
st.set_page_config(
    page_title="Industry Sector Analyzer",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
    <style>
        /* Reduce top padding */
        .block-container {
            padding-top: 1rem;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1rem;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        .status-tag {
            display: inline-block;
            padding: 0.3em 0.8em;
            margin: 0.2em;
            font-size: 0.9em;
            font-weight: bold;
            line-height: 1;
            text-align: center;
            white-space: nowrap;
            vertical-align: middle;
            border-radius: 0.25rem;
            color: white;
        }
        .tag-red {
            background-color: #D32F2F; /* Red */
        }
        .tag-green {
            background-color: #388E3C; /* Green */
        }
        
        /* CSS for the green button when ready */
        div.stButton > button {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)


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
- Medical Cannabis: Cannabis for medical use (Disparies, cultivation, medical marijuana products)
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

    # --- MODEL UPDATED TO gemini-2.5-pro AND URL TYPO FIXED ---
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"
    
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
            
            # Use .get() for safer dictionary access
            candidate = result.get("candidates", [{}])[0]
            if candidate:
                text_content = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
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
                # Log the error response from the API
                try:
                    st.json(e.response.json()) 
                except json.JSONDecodeError:
                    st.text(e.response.text) # Fallback if error response isn't JSON
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

# --- Sidebar for Inputs ---
with st.sidebar:
    st.markdown("<h2 style='font-weight: bold;'>Inputs</h2>", unsafe_allow_html=True)
    
    # API Key Input
    GEMINI_API_KEY = st.text_input("Enter the Gemini API Key:", type="password")
    
    st.subheader("Input Method 1: Scan Website")
    website_url = st.text_input("Enter website URL (e.g., https://www.apple.com):")
    scan_button = st.button("Scan and Analyze Website", type="primary")

    st.subheader("Input Method 2: Manual Input")
    manual_services = st.text_area("Core products/services (one per line):", height=120)
    manual_button = st.button("Analyze Manual Input", type="primary")

# --- Main Page Display ---
st.markdown("<p style='font-size: 1px;'>&nbsp;</p>", unsafe_allow_html=True) # Spacer
st.markdown("<h1 style='background-color: #FFF9C4; padding: 10px; border-radius: 10px;'>Industry Sector Analyzer</h1>", unsafe_allow_html=True)
st.markdown("""
This tool helps brands accurately identify their industry category by analyzing website content or manual input. 
It uses Gemini’s AI to compare messaging against a trusted reference database, ensuring precise classification for outreach, compliance, and positioning.
""")

# --- Updated Instructions Section ---
with st.expander("Instructions"):

    with st.expander("How to Use This Tool"):
        st.markdown("""
        This tool analyzes a company's website or a manual description to identify its core products/services. It classifies them into Primary, Secondary, or Tertiary industry sectors.

        1.  **Provide API Key:** Enter a valid Google Gemini API key in the sidebar.
        2.  **Choose Input Method:**
            * **Method 1 (Scan Website):** Enter a full website URL (e.g., `https://www.company.com`) and click "Scan and Analyze Website".
            * **Method 2 (Manual Input):** Manually type or paste a description of the company's products/services and click "Analyze Manual Input".
        3.  **Review Results:** The tool will display a table of the identified services, their industry category, and their economic sector. A bar chart will summarize the findings.
        """)

    with st.expander("How to Start"):
        st.markdown("""
        1.  **Get Your API Key:** Follow the instructions in the "How to Get a Google AI API Key" section below.
        2.  **Enter Key:** Paste your API key into the "Enter the Gemini API Key" field in the sidebar. A green "API Key Ready" tag will appear.
        3.  **Provide Input:** Use either "Input Method 1" (website) or "Input Method 2" (manual text) in the sidebar.
        4.  **Analyze:** Click the "Scan and Analyze Website" or "Analyze Manual Input" button.
        """)

    with st.expander("How to Get a Google AI API Key"):
        st.markdown("""
        1.  **Visit Google AI Studio:** Go to [aistudio.google.com](https://aistudio.google.com).
        2.  **Sign In:** Log in with a Google account.
        3.  **Get API Key:** Click on **"Get API key"** on the left-hand menu.
        4.  **Create API Key:** Click **"Create API key in new project"**.
        5.  **Copy and Use:** Copy the new key and paste it into the "Enter the Gemini API Key" field in this app's sidebar.
        """)

# Check for API key after setting up the main page
api_key_ready = bool(GEMINI_API_KEY)
if not api_key_ready:
    st.warning("Please enter a Gemini API Key in the sidebar to proceed.")
    st.stop()
else:
    # Show green "Ready" tag in sidebar if key is present
    st.sidebar.markdown(
        '<div style="display: flex; align-items: center; justify-content: center; margin-top: 10px;">'
        '<span class="status-tag tag-green">API Key Ready</span>'
        '</div>',
        unsafe_allow_html=True
    )

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
    st.header("Analysis Results", divider="rainbow")
    
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

