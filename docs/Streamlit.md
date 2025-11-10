# Streamlit Documentation

Streamlit is an open-source Python framework designed for data scientists and AI/ML engineers to build and deploy dynamic data applications with minimal code. This documentation repository contains comprehensive guides, API references, tutorials, and deployment instructions for creating interactive web applications using Streamlit. The framework enables rapid prototyping and production deployment of data apps, eliminating the need for frontend development expertise while providing powerful features for data visualization, user interaction, and real-time updates.

The documentation covers the complete Streamlit ecosystem including the core library APIs, multipage application architecture, caching mechanisms, state management, chart integrations, custom components, database connections, and deployment options through Streamlit Community Cloud and enterprise solutions. It provides both conceptual guides for understanding Streamlit's execution model and practical tutorials for building everything from simple data explorers to complex LLM-powered chat applications. The framework's magic write capability, declarative widget system, and automatic rerun behavior make it uniquely suited for turning Python scripts into shareable web apps in minutes.

## Core Display Functions

### Write and Display Data

Stream any content to the app including text, dataframes, charts, and complex objects.

```python
import streamlit as st
import pandas as pd
import numpy as np

# Display text with markdown support
st.write("# My Data App")
st.write("Here's our first attempt at using data to create a table:")

# Display dataframe automatically formatted as interactive table
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
st.write(df)

# Write also handles multiple arguments
st.write("Temperature:", 72, "°F")

# Display raw data with st.dataframe for full interactivity
st.dataframe(df.style.highlight_max(axis=0))
```

### Stream LLM Responses

Display streaming text with typewriter effect for AI/chat applications.

```python
import streamlit as st
import time

def stream_data():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

    # Can also yield dataframes and other objects
    yield pd.DataFrame(np.random.randn(5, 3), columns=['a', 'b', 'c'])

if st.button("Stream response"):
    response = st.write_stream(stream_data)
    st.write("Full response:", response)

# Example with OpenAI streaming
# from openai import OpenAI
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# stream = client.chat.completions.create(
#     model="gpt-4",
#     messages=[{"role": "user", "content": "Tell me a joke"}],
#     stream=True,
# )
# st.write_stream(stream)
```

## Interactive Widgets

### Selectbox Widget

Display dropdown selection with optional new value creation.

```python
import streamlit as st

# Basic selectbox with default first option selected
option = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)
st.write("You selected:", option)

# Selectbox with no initial selection
contact = st.selectbox(
    "Preferred contact method",
    ("Email", "Phone", "Text"),
    index=None,
    placeholder="Select contact method..."
)

if contact:
    st.write(f"We'll contact you via {contact}")

# Allow users to add custom options
email = st.selectbox(
    "Default email",
    ["work@company.com", "personal@email.com"],
    index=None,
    placeholder="Select saved email or enter new one",
    accept_new_options=True,
    key="email_select"
)

if email:
    st.write(f"Using email: {email}")
```

### Slider Control

Create numeric sliders for value selection and filtering.

```python
import streamlit as st

# Simple integer slider
age = st.slider('Select your age', 0, 100, 25)
st.write(f"You are {age} years old")

# Range slider for min/max selection
temperature_range = st.slider(
    'Select temperature range',
    min_value=-20.0,
    max_value=50.0,
    value=(-10.0, 25.0),
    step=0.5
)
st.write(f"Range: {temperature_range[0]}°C to {temperature_range[1]}°C")

# Time-based filtering example
hour_to_filter = st.slider('hour', 0, 23, 17)  # 0-23h, default 17h
st.write(f"Filtering data for {hour_to_filter}:00")
```

### Checkbox Toggle

Show/hide content or enable/disable features with checkboxes.

```python
import streamlit as st

# Simple checkbox for showing raw data
show_data = st.checkbox('Show raw data')
if show_data:
    st.subheader('Raw data')
    st.write(pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]}))

# Checkbox with default state
agree = st.checkbox('I agree to terms and conditions', value=False)
if agree:
    st.success('Thank you for agreeing!')

# Using checkbox state to control widget behavior
if "disabled" not in st.session_state:
    st.session_state.disabled = False

st.checkbox("Disable other widgets", key="disabled")
st.text_input("Name", disabled=st.session_state.disabled)
```

## Data Visualization

### Bar Charts

Display bar charts from dataframes or arrays.

```python
import streamlit as st
import pandas as pd
import numpy as np

# Simple bar chart from array
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.bar_chart(chart_data)

# Bar chart with hour distribution
data = pd.read_csv('data.csv')
data['hour'] = pd.to_datetime(data['date/time']).dt.hour
hist_values = np.histogram(data['hour'], bins=24, range=(0,24))[0]
st.subheader('Number of pickups by hour')
st.bar_chart(hist_values)
```

### Vega-Lite Charts

Create interactive charts with Vega-Lite grammar with selection support.

```python
import streamlit as st
import pandas as pd
from numpy.random import default_rng as rng

df = pd.DataFrame(rng(0).standard_normal((60, 3)), columns=["a", "b", "c"])

# Basic scatter plot
st.vega_lite_chart(
    df,
    {
        "mark": {"type": "circle", "tooltip": True},
        "encoding": {
            "x": {"field": "a", "type": "quantitative"},
            "y": {"field": "b", "type": "quantitative"},
            "size": {"field": "c", "type": "quantitative"},
            "color": {"field": "c", "type": "quantitative"},
        },
    },
)

# Interactive chart with selection
event = st.vega_lite_chart(
    df,
    {
        "mark": "point",
        "params": [{
            "name": "point_selection",
            "select": {"type": "point"}
        }],
        "encoding": {
            "x": {"field": "a", "type": "quantitative"},
            "y": {"field": "b", "type": "quantitative"},
        },
    },
    on_select="rerun",
    key="chart"
)

if event.selection:
    st.write("Selected points:", event.selection)
```

### Map Visualization

Display geographic data on interactive maps.

```python
import streamlit as st
import pandas as pd

# Load data with lat/lon coordinates
data = pd.DataFrame({
    'lat': [37.76, 37.77, 37.78],
    'lon': [-122.4, -122.41, -122.42]
})

# Display all points
st.map(data)

# Filter and display subset
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data['hour'] == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)
```

## Caching and Performance

### Data Caching

Cache expensive data operations like database queries and dataframe transforms.

```python
import streamlit as st
import pandas as pd

@st.cache_data
def fetch_and_clean_data(url):
    # Fetch data from URL and clean it up
    data = pd.read_csv(url, nrows=10000)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data['date/time'] = pd.to_datetime(data['date/time'])
    return data

# First call executes function
d1 = fetch_and_clean_data("https://example.com/data1.csv")

# Second call with same URL returns cached value
d2 = fetch_and_clean_data("https://example.com/data1.csv")

# Different URL executes function again
d3 = fetch_and_clean_data("https://example.com/data2.csv")

# Cache with TTL (time to live)
@st.cache_data(ttl=3600)  # Cache expires after 1 hour
def fetch_live_data():
    return pd.read_csv("https://api.example.com/live-data")

# Persist cache to disk
@st.cache_data(persist="disk")
def load_large_dataset():
    return pd.read_parquet("large_file.parquet")

# Exclude unhashable parameters with underscore prefix
@st.cache_data
def query_database(_db_connection, num_rows):
    return pd.read_sql(f"SELECT * FROM table LIMIT {num_rows}", _db_connection)

# Clear specific cache entry
fetch_and_clean_data.clear("https://example.com/data1.csv")

# Clear all cached data
st.cache_data.clear()
```

## Layout and Containers

### Empty Placeholder

Create placeholder for dynamic content replacement.

```python
import streamlit as st
import time

# Progress countdown that replaces itself
with st.empty():
    for seconds in range(10):
        st.write(f"⏳ {seconds} seconds have passed")
        time.sleep(1)
    st.write("✅ 10 seconds over!")

st.button("Rerun")

# Replace multiple elements in sequence
placeholder = st.empty()
placeholder.markdown("Hello")
time.sleep(1)

placeholder.progress(0, "Wait for it...")
time.sleep(1)
placeholder.progress(50, "Wait for it...")
time.sleep(1)
placeholder.progress(100, "Wait for it...")
time.sleep(1)

# Display multiple elements temporarily
with placeholder.container():
    st.line_chart({"data": [1, 5, 2, 6]})
    time.sleep(1)
    st.markdown("3...")
    time.sleep(1)

placeholder.markdown("Poof!")
time.sleep(1)
placeholder.empty()  # Clear the placeholder
```

## Multipage Applications

### Page Definition and Navigation

Define multipage apps with custom navigation using st.Page and st.navigation.

```python
import streamlit as st

# Define pages
page1 = st.Page("pages/home.py", title="Home", icon="🏠")
page2 = st.Page("pages/dashboard.py", title="Dashboard", icon="📊")
page3 = st.Page("pages/settings.py", title="Settings", icon="⚙️")

# Create navigation
pg = st.navigation([page1, page2, page3])
pg.run()

# Conditional navigation based on authentication
if st.session_state.get("logged_in", False):
    pages = [
        st.Page("pages/home.py", title="Home"),
        st.Page("pages/profile.py", title="Profile"),
        st.Page("pages/admin.py", title="Admin")
    ]
else:
    pages = [st.Page("pages/login.py", title="Login")]

pg = st.navigation(pages)
pg.run()

# Programmatic page switching
if st.button("Go to Dashboard"):
    st.switch_page("pages/dashboard.py")

# Build custom navigation menu
st.page_link("pages/home.py", label="Home", icon="🏠")
st.page_link("pages/dashboard.py", label="Dashboard", icon="📊")
```

### Simple Pages Directory

Automatically create multipage apps using pages/ directory structure.

```
your_app/
├── streamlit_app.py        # Homepage
└── pages/
    ├── 1_📊_Dashboard.py
    ├── 2_🔍_Analysis.py
    └── 3_⚙️_Settings.py
```

```python
# streamlit_app.py (homepage)
import streamlit as st

st.title("Welcome to My App")
st.write("Use the sidebar to navigate between pages")

# pages/1_📊_Dashboard.py
import streamlit as st
import pandas as pd

st.title("Dashboard")
data = pd.read_csv("data.csv")
st.dataframe(data)

# pages/2_🔍_Analysis.py
import streamlit as st

st.title("Analysis")
st.write("Detailed analysis page")
```

## Database Connections

### SQL Connection

Connect to SQL databases with built-in query caching.

```python
import streamlit as st

# Initialize connection
conn = st.connection("postgresql", type="sql")

# Query with automatic caching
df = conn.query("SELECT * FROM users WHERE active = true", ttl=600)
st.dataframe(df)

# Parameterized queries
user_id = st.number_input("Enter user ID", min_value=1)
user_data = conn.query(
    "SELECT * FROM users WHERE id = :id",
    params={"id": user_id},
    ttl=300
)
st.write(user_data)

# Using connection for writes
with conn.session as session:
    session.execute("INSERT INTO logs (message) VALUES ('User logged in')")
    session.commit()
```

## Running and CLI Commands

### Streamlit CLI

Launch and manage Streamlit applications from command line.

```bash
# Run basic app
streamlit run app.py

# Run app with custom port
streamlit run app.py --server.port 8080

# Run app from URL
streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py

# View Streamlit version
streamlit version

# Show hello world demo
streamlit hello

# Clear cache
streamlit cache clear

# View configuration
streamlit config show

# View docs
streamlit docs
```

### App Configuration

Configure Streamlit apps using .streamlit/config.toml or command line flags.

```toml
# .streamlit/config.toml
[theme]
primaryColor = "#F63366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200

[browser]
gatherUsageStats = false
serverAddress = "localhost"
serverPort = 8501
```

```python
# Access config values in app
import streamlit as st

# Get config option
config_value = st.config.get_option("server.port")

# Set config option programmatically (for testing)
st.config.set_option("server.headless", True)
```

## Deployment

### Community Cloud Deployment

Deploy apps to Streamlit Community Cloud from GitHub repositories.

```bash
# 1. Prepare repository structure
your_repo/
├── streamlit_app.py
├── requirements.txt
├── packages.txt          # (optional) apt packages
└── .streamlit/
    ├── config.toml       # (optional) configuration
    └── secrets.toml      # (optional, don't commit!)

# requirements.txt example
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.14.0
```

```python
# streamlit_app.py
import streamlit as st

st.title("My Deployed App")
st.write("This app is live on Streamlit Community Cloud!")

# Access secrets in deployed app
api_key = st.secrets["api_keys"]["openai"]
db_password = st.secrets["database"]["password"]

# secrets.toml structure (configure in Community Cloud UI)
# [api_keys]
# openai = "sk-..."
#
# [database]
# host = "db.example.com"
# username = "admin"
# password = "secret123"
```

**Deployment steps:**
1. Push code to GitHub public repository
2. Go to share.streamlit.io
3. Click "Create app" or "Deploy an app"
4. Select repository, branch, and main file path
5. Optional: Configure Python version and secrets in Advanced settings
6. Click "Deploy"
7. App URL: `https://your-custom-name.streamlit.app`

### Docker Deployment

Deploy Streamlit apps using Docker containers.

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Build and run Docker container
docker build -t my-streamlit-app .
docker run -p 8501:8501 my-streamlit-app

# With environment variables and secrets
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=sk-... \
  -v $(pwd)/.streamlit/secrets.toml:/app/.streamlit/secrets.toml \
  my-streamlit-app
```

## Summary

Streamlit documentation provides comprehensive guidance for building data-driven web applications using Python. The framework's primary use cases span rapid prototyping of data science projects, creating internal tools for data exploration and analysis, building machine learning model demos, developing interactive dashboards and reports, and deploying production-grade data applications. Streamlit's declarative API eliminates the complexity of web development, allowing data professionals to focus on their domain logic while the framework handles UI rendering, state management, and user interactions automatically.

Integration patterns include connecting to various data sources through the st.connection API (SQL databases, cloud storage, APIs), incorporating custom visualizations using Altair, Plotly, Matplotlib or other charting libraries, building LLM-powered chat interfaces with streaming responses, implementing authentication flows for multi-user applications, and deploying to multiple platforms including Streamlit Community Cloud, Docker containers, Kubernetes clusters, and cloud services like AWS, GCP, and Azure. The framework's caching decorators, session state management, and fragment execution model enable efficient performance even for computationally intensive applications, while the extensive widget library and layout containers provide flexibility for creating sophisticated user interfaces without writing HTML, CSS, or JavaScript.
