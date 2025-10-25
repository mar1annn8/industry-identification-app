{\rtf1\ansi\ansicpg1252\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red111\green14\blue195;\red236\green241\blue247;\red0\green0\blue0;
\red77\green80\blue85;\red24\green112\blue43;\red164\green69\blue11;}
{\*\expandedcolortbl;;\cssrgb\c51765\c18824\c80784;\cssrgb\c94118\c95686\c97647;\cssrgb\c0\c0\c0;
\cssrgb\c37255\c38824\c40784;\cssrgb\c9412\c50196\c21961;\cssrgb\c70980\c34902\c3137;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs28 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import\cf0 \strokec4  streamlit \cf2 \strokec2 as\cf0 \strokec4  st\cb1 \
\cf2 \cb3 \strokec2 import\cf0 \strokec4  requests\cb1 \
\cf2 \cb3 \strokec2 from\cf0 \strokec4  bs4 \cf2 \strokec2 import\cf0 \strokec4  BeautifulSoup\cb1 \
\cf2 \cb3 \strokec2 import\cf0 \strokec4  json\cb1 \
\cf2 \cb3 \strokec2 import\cf0 \strokec4  time\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- Database from Prompt ---\cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # This is used in the system prompt for the AI\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 INDUSTRY_DATABASE = \cf6 \strokec6 """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf6 \cb3 \strokec6 - Adult Products: Products related to adult entertainment and intimacy (Adult toys, lingerie, sexual wellness products)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Agriculture & Environment: Farming, natural resource management, sustainability (Crop production, livestock, forestry, fisheries, conservation, renewable energy (solar, wind, hydro), environmental protection)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Performing Artis & Cultural Experiences: Creative expression, entertainment, cultural experiences (Theater, dance, and a wide range of activities, including concerts, festivals, museums, and other cultural attractions.)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Visual Arts & Entertainment: Creative expression, entertainment, cultural experiences (Visual arts, film, television, gaming)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Autos & Vehicles: Design, manufacturing, and sales of automobiles and other vehicles (Cars, trucks, motorcycles, buses, recreational vehicles (RVs))\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Beauty & Fitness: Personal care, appearance enhancement, physical well-being (Cosmetics, skincare, hair care, salons, spas, gyms, fitness studios, personal training)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Business & Industrial: Commercial activities, manufacturing, production, and professional services (Manufacturing, construction, energy (fossil fuels, utilities), logistics, wholesale, retail, consulting, legal services, accounting, B2B services)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Computers & Electronics: Technology, computing, and electronic devices (Hardware (computers, smartphones, peripherals), software, IT services, consumer electronics (TVs, audio equipment))\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Fashion: Clothing, footwear, accessories, and style (Apparel design, manufacturing, retail, fashion shows, modeling)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Finance: Money management, investments, banking, and financial services (Banking, investment banking, insurance, financial planning, accounting, wealth management)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Firearms & Weapons: Firearms, ammunition, and related equipment (Guns, rifles, pistols, ammunition, hunting gear, self-defense equipment)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Food & Beverage: Production, distribution, and sale of food and drinks (Restaurants, cafes, food manufacturing, grocery stores, beverage production (alcoholic and non-alcoholic))\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Gifts & Shopping: Retail, e-commerce, and consumer goods (Gift shops, department stores, online retailers, specialty stores)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Health & Wellness: Healthcare, personal well-being, alternative medicine (Hospitals, clinics, pharmacies, mental health services, alternative therapies (acupuncture, massage), nutritional supplements, alternative health products (Kratom, where legal))\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Hobbies & Leisure: Recreational activities, interests, and pastimes (Arts and crafts, collecting, gaming, sports, travel, reading, gardening)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Home & Garden: Home improvement, d\'e9cor, gardening, and outdoor living (Furniture, appliances, home d\'e9cor, gardening supplies, landscaping)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Hospitality & Travel: Accommodation, tourism, and travel services (Hotels, resorts, airlines, travel agencies, restaurants, entertainment venues)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Internet & Telecommunications: Digital communication, online services, and network infrastructure (Internet service providers (ISPs), telecommunications companies, social media platforms, online content providers)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Jobs & Education: Employment, training, and education (Recruitment, staffing, training, schools, universities, online learning platforms)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Kids & Family: Products and services for children and families (Toys, children's clothing, childcare, family entertainment, parenting resources)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Law & Government: Legal services, public administration, and policy (Law firms, government agencies, courts, legal aid organizations)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Lifestyle: Personal interests, values, and way of living (Fashion, beauty, travel, food, home d\'e9cor, hobbies)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Logistics & Transportation: Movement of goods and people (Shipping, trucking, warehousing, airlines, railways, public transportation)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Marketing: Promoting products, services, or ideas (Market research, advertising, branding, public relations, content marketing, digital marketing, sales)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Media & Communications: Information dissemination, journalism, public relations (Journalism, publishing, broadcasting, telecommunications, public relations, content creation)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Medical Cannabis: Cannabis for medical use (Dispensaries, cultivation, medical marijuana products)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - News: Current events and information (Newspapers, magazines, television news, online news portals, radio)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Not For Profit: Charitable organizations and social causes (Charities, foundations, NGOs, social advocacy groups)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - People & Society: Social issues, community, and culture (Social services, community organizations, advocacy groups, cultural institutions)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Pets & Animals: Pet care, animal welfare, and related products and services (Pet food, pet supplies, veterinary services, animal shelters, zoos)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Real Estate: Property, land, and buildings (Residential, commercial, and industrial real estate, property development, real estate brokerage, property management)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Recreational Cannabis: Cannabis for recreational use (where legal) (Dispensaries, cannabis products, consumption lounges (where permitted))\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Science: Research, discovery, and innovation (Scientific research institutions, laboratories, technology companies, academic departments)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Specialty Products: Unique, niche, or regulated goods (Antiques, collectibles, art, luxury goods, specialized equipment)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Vices & Adult Entertainment: Activities and products considered taboo or morally questionable (Gambling, adult entertainment venues, pornography, tobacco, alcohol)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 - Other: Any industry not explicitly categorized above\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 """\cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- System Prompt for Gemini ---\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 SYSTEM_PROMPT = \cf6 \strokec6 f"""\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf6 \cb3 \strokec6 You are an expert business analyst. The task is to analyze a company's description (from their website text or a manual description) and categorize their products/services.\cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 Follow these steps:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf7 \cb3 \strokec7 1\cf0 \strokec4 .  Identify the core products \cf2 \strokec2 or\cf0 \strokec4  services described \cf2 \strokec2 in\cf0 \strokec4  the user\cf6 \strokec6 's text.\cf0 \cb1 \strokec4 \
\cf7 \cb3 \strokec7 2\cf0 \strokec4 .  For each identified product/service, \cf2 \strokec2 match\cf0 \strokec4  it to the *most relevant* category \cf2 \strokec2 from\cf0 \strokec4  the \cf6 \strokec6 'Industry Database'\cf0 \strokec4  provided below.\cb1 \
\cf7 \cb3 \strokec7 3\cf0 \strokec4 .  For each matched category, classify it \cf2 \strokec2 as\cf0 \strokec4  \cf6 \strokec6 'Primary'\cf0 \strokec4 , \cf6 \strokec6 'Secondary'\cf0 \strokec4 , \cf2 \strokec2 or\cf0 \strokec4  \cf6 \strokec6 'Tertiary'\cf0 \strokec4  based on these economic definitions:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     * **Primary:** Involves the extraction \cf2 \strokec2 and\cf0 \strokec4  harvesting of raw materials (e.g., farming, mining, fishing, forestry).\cb1 \
\cb3     * **Secondary:** Involves manufacturing, processing, \cf2 \strokec2 and\cf0 \strokec4  construction (e.g., car manufacturing, food production, building).\cb1 \
\cb3     * **Tertiary:** Involves providing services (e.g., retail, finance, healthcare, software, entertainment, consulting).\cb1 \
\pard\pardeftab720\partightenfactor0
\cf7 \cb3 \strokec7 4\cf0 \strokec4 .  Return the analysis \cf2 \strokec2 in\cf0 \strokec4  a structured JSON \cf2 \strokec2 format\cf0 \strokec4 . The JSON should be an \cf2 \strokec2 object\cf0 \strokec4  \cf2 \strokec2 with\cf0 \strokec4  a single key \cf6 \strokec6 "services"\cf0 \strokec4 , which \cf2 \strokec2 is\cf0 \strokec4  a \cf2 \strokec2 list\cf0 \strokec4  of objects. Each \cf2 \strokec2 object\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  the \cf2 \strokec2 list\cf0 \strokec4  should have three keys: \cf6 \strokec6 "name"\cf0 \strokec4  (the identified product/service), \cf6 \strokec6 "category"\cf0 \strokec4  (the category \cf2 \strokec2 from\cf0 \strokec4  the database), \cf2 \strokec2 and\cf0 \strokec4  \cf6 \strokec6 "sector"\cf0 \strokec4  (Primary, Secondary, \cf2 \strokec2 or\cf0 \strokec4  Tertiary).\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 Example of a valid JSON output:\cb1 \
\cb3 \{\{\cf6 \strokec6 "services"\cf0 \strokec4 : [\cb1 \
\cb3     \{\{\cf6 \strokec6 "name"\cf0 \strokec4 : \cf6 \strokec6 "Smartphone Sales"\cf0 \strokec4 , \cf6 \strokec6 "category"\cf0 \strokec4 : \cf6 \strokec6 "Computers & Electronics"\cf0 \strokec4 , \cf6 \strokec6 "sector"\cf0 \strokec4 : \cf6 \strokec6 "Tertiary"\cf0 \strokec4 \}\},\cb1 \
\cb3     \{\{\cf6 \strokec6 "name"\cf0 \strokec4 : \cf6 \strokec6 "Software Development"\cf0 \strokec4 , \cf6 \strokec6 "category"\cf0 \strokec4 : \cf6 \strokec6 "Computers & Electronics"\cf0 \strokec4 , \cf6 \strokec6 "sector"\cf0 \strokec4 : \cf6 \strokec6 "Tertiary"\cf0 \strokec4 \}\},\cb1 \
\cb3     \{\{\cf6 \strokec6 "name"\cf0 \strokec4 : \cf6 \strokec6 "Crop Production"\cf0 \strokec4 , \cf6 \strokec6 "category"\cf0 \strokec4 : \cf6 \strokec6 "Agriculture & Environment"\cf0 \strokec4 , \cf6 \strokec6 "sector"\cf0 \strokec4 : \cf6 \strokec6 "Primary"\cf0 \strokec4 \}\}\cb1 \
\cb3 ]\}\}\cb1 \
\
\cb3 Here \cf2 \strokec2 is\cf0 \strokec4  the Industry Database:\cb1 \
\cb3 \{INDUSTRY_DATABASE\}\cb1 \
\pard\pardeftab720\partightenfactor0
\cf6 \cb3 \strokec6 """\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 # --- Helper Functions ---\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 def scrape_website_text(url):\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     Scrapes the visible text \cf2 \strokec2 from\cf0 \strokec4  a given URL.\cb1 \
\cb3     Returns the text content \cf2 \strokec2 or\cf0 \strokec4  an error message.\cb1 \
\cb3     \cf6 \strokec6 """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf6 \cb3 \strokec6     try:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         # Add a simple header to pretend to be a browser\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         headers = \{\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         \}\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         response = requests.get(url, headers=headers, timeout=10)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6         # Parse the HTML\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         soup = BeautifulSoup(response.text, 'html.parser')\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6         # Remove script and style tags\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         for script_or_style in soup(["script", "style"]):\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             script_or_style.decompose()\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6         # Get text and clean it up\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         text = soup.get_text()\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         lines = (line.strip() for line in text.splitlines())\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         chunks = (phrase.strip() for line in lines for phrase in line.split("  "))\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         cleaned_text = '\\n'.join(chunk for chunk in chunks if chunk)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         # Limit the text to avoid sending too much to the API\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         return cleaned_text[:4000]\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     except requests.exceptions.RequestException as e:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         st.error(f"Error fetching URL: \{e\}")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         return None\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     except Exception as e:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         st.error(f"Error parsing website: \{e\}")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         return None\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 async def call_gemini_api(user_text, api_key):\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     Calls the Gemini API \cf2 \strokec2 with\cf0 \strokec4  the scraped text \cf2 \strokec2 and\cf0 \strokec4  returns the JSON analysis.\cb1 \
\cb3     Implements exponential backoff \cf2 \strokec2 for\cf0 \strokec4  retries.\cb1 \
\cb3     \cf6 \strokec6 """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf6 \cb3 \strokec6     if not api_key:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         st.error("API Key is not set. Please add it to the Streamlit Secrets.")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         return None\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6     api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=\{api_key\}"\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     user_query = f"Please analyze the following company information: \{user_text\}"\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6     payload = \{\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         "contents": [\{"parts": [\{"text": user_query\}]\}],\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         "systemInstruction": \{\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             "parts": [\{"text": SYSTEM_PROMPT\}]\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         \},\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         "generationConfig": \{\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             "responseMimeType": "application/json",\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         \}\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     \}\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6     max_retries = 5\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     delay = 1  # Start with 1 second delay\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6     for attempt in range(max_retries):\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         try:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             response = requests.post(api_url, json=payload, headers=\{'Content-Type': 'application/json'\})\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             result = response.json()\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             candidate = result.get("candidates", [])[0]\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             if candidate:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6                 text_content = candidate.get("content", \{\}).get("parts", [])[0].get("text", "")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6                 if text_content:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6                     # The response is expected to be a JSON string\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6                     return json.loads(text_content)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             st.error("Failed to get a valid response from the API. The response might be empty or malformed.")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             return None\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6         except requests.exceptions.HTTPError as e:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             if e.response.status_code in [429, 500, 503]:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6                 # Rate limit or server error, wait and retry\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6                 time.sleep(delay)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6                 delay *= 2  # Exponential backoff\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             else:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6                 st.error(f"HTTP Error: \{e\}")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6                 st.json(e.response.json()) # Show error details\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6                 return None\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         except requests.exceptions.RequestException as e:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             st.error(f"Request Error: \{e\}. Retrying...")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             time.sleep(delay)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             delay *= 2\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         except json.JSONDecodeError:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             st.error("API did not return valid JSON. The output may be malformed.")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             # Log the raw response for debugging if possible\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             try:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6                 st.text_area("Raw API Response:", value=response.text, height=150)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             except NameError:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6                 pass # response object might not be available\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             return None\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         except Exception as e:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             st.error(f"An unexpected error occurred: \{e\}")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             return None\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     st.error("Failed to get a response from the API after several retries.")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     return None\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 # --- Streamlit App UI ---\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 st.set_page_config(layout="wide", page_title="Industry Sector Analyzer")\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 st.title("Industry Sector Analyzer")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 st.markdown("Enter a website URL to automatically scan its content, or manually describe the company's products/services. The app will categorize them into Primary, Secondary, or Tertiary industries.")\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 # API Key Input\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 # Load API key from secrets\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 try:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 except FileNotFoundError:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     st.error("`secrets.toml` file not found. Please create one.")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     GEMINI_API_KEY = ""\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 except KeyError:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     st.warning("`GEMINI_API_KEY` not found in `secrets.toml`. Please add it.")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     GEMINI_API_KEY = st.text_input("Enter Gemini API Key (or add to secrets):", type="password")\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 if not GEMINI_API_KEY:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     st.stop()\cf0 \cb1 \strokec4 \
\
\
\cf6 \cb3 \strokec6 col1, col2 = st.columns([1, 1])\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 with col1:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     st.subheader("Input Method 1: Scan Website")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     website_url = st.text_input("Enter website URL (e.g., https://www.apple.com):")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     scan_button = st.button("Scan and Analyze Website")\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 with col2:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     st.subheader("Input Method 2: Manual Input")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     manual_services = st.text_area("Core products/services (one per line):", height=120)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     manual_button = st.button("Analyze Manual Input")\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 # --- Logic to handle button clicks ---\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 analysis_input = None\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 if scan_button and website_url:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     with st.spinner(f"Scanning \{website_url\}... This may take a moment."):\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         scraped_text = scrape_website_text(website_url)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         if scraped_text:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             analysis_input = scraped_text\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             st.session_state['analysis_input'] = scraped_text\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             st.session_state['analysis_complete'] = False\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 elif manual_button and manual_services:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     analysis_input = manual_services\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     st.session_state['analysis_input'] = manual_services\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     st.session_state['analysis_complete'] = False\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 # --- Perform Analysis and Display Results ---\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 if 'analysis_input' in st.session_state and not st.session_state.get('analysis_complete', False):\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     st.divider()\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     st.subheader("Analysis Results")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     with st.spinner("Analyzing content and classifying industries..."):\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         analysis_result = asyncio.run(call_gemini_api(st.session_state['analysis_input'], GEMINI_API_KEY))\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         if analysis_result and "services" in analysis_result:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             st.session_state['analysis_result'] = analysis_result["services"]\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             st.session_state['analysis_complete'] = True\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         else:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             st.error("Analysis failed. The API did not return the expected data format.")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             st.session_state['analysis_complete'] = True # Stop retrying\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 # Display the results if they exist in the session state\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 if st.session_state.get('analysis_complete', False) and 'analysis_result' in st.session_state:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     results = st.session_state['analysis_result']\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     if results:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         st.dataframe(results, use_container_width=True)\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         st.divider()\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         st.subheader("Summary by Sector")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         # Pie chart data\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         primary_count = sum(1 for item in results if item['sector'] == 'Primary')\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         secondary_count = sum(1 for item in results if item['sector'] == 'Secondary')\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         tertiary_count = sum(1 for item in results if item['sector'] == 'Tertiary')\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         sector_data = \{\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             'Sector': ['Primary', 'Secondary', 'Tertiary'],\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             'Count': [primary_count, secondary_count, tertiary_count]\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         \}\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         if sum(sector_data['Count']) > 0:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             st.bar_chart(sector_data, x='Sector', y='Count')\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         else:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             st.info("No sectors were identified.")\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     else:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         st.info("No products or services were identified from the provided content.")\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 # Show the text that was analyzed\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 if 'analysis_input' in st.session_state:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     with st.expander("Show Analyzed Text"):\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6         st.text(st.session_state['analysis_input'])\cf0 \cb1 \strokec4 \
\
}