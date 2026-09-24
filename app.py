# Importing necessary libraries.
import os, importlib.util
import streamlit as st
from main import organize_files, log_weather, fetch_weather_data, generate_mail_body, send_email, EMAIL
import pandas as pd

# Configure the Streamlit page settings and layout.
st.set_page_config(
    page_title = "Automation Suite",
    page_icon = "🤖⚡",
    layout = "centered",
    initial_sidebar_state = "expanded")

st.markdown(
    """
    <style>

    /* Targets Streamlit blocks directly inside vertical containers. */
    div[data-testid="stVerticalBlock"] > div[data-testid="stBlock"] {
        border-radius: 12px; /* Rounds the block corners. */
    }

    /* Targets primary Streamlit buttons. */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00D4FF 0%, #0088FF 100%); /* Adds the primary button gradient. */
        color: #0B0F19 !important; /* Sets primary button label color. */
        font-weight: 700 !important; /* Makes the primary label bold. */
        border: none; /* Removes the default border. */
        border-radius: 8px; /* Rounds the primary button corners. */
        padding: 0.6rem 1.2rem; /* Adds vertical and horizontal button space. */
        transition: all 0.25s ease; /* Smooths button state changes. */
    }

    /* Targets secondary Streamlit buttons. */
    div.stButton > button[kind="secondary"] {
        background-color: #161F33; /* Sets the secondary button background. */
        color: #00D4FF !important; /* Sets secondary button label color. */
        border: 1px solid #00D4FF40; /* Adds a translucent cyan border. */
        border-radius: 8px; /* Rounds the secondary button corners. */
        font-weight: 600 !important; /* Makes the secondary label semi-bold. */
        transition: all 0.25s ease; /* Smooths button state changes. */
    }

    /* Targets primary buttons while the pointer is over them. */
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px); /* Moves the primary button upward. */
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.35); /* Adds a cyan hover glow. */
    }
    
    /* Targets secondary buttons while the pointer is over them. */
    div.stButton > button[kind="secondary"]:hover {
       background-color: #1E2D4A; /* Lightens the secondary background. */
        border-color: #00D4FF; /* Brightens the secondary border. */
        transform: translateY(-1px); /* Moves the secondary button upward. */
    }

    /* Targets paragraph text rendered inside every Streamlit button. */
    div.stButton > button p {
        color: #0B0F19 !important; /* Sets the default button label color. */
        font-style: italic !important; /* Makes the button label italic. */
        font-weight: 700 !important; /* Makes the button label bold. */
        display: inline-block; /* Allows the text transform to apply. */
        transform: skewX(-8deg); /* Slants the label when the font lacks italics. */
    }

    /* Targets paragraph text inside secondary button labels. */
    div.stButton > button[kind="secondary"] p {
        color: #00D4FF !important; /* Sets secondary label color to cyan. */
    }

    /* Targets placeholder text inside Streamlit text inputs. */
    div[data-testid = "stTextInput"] input::placeholder {
        display: inline-block; /* Allows the placeholder transform to apply. */
        transform: skewX(-8deg); /* Slants the placeholder text. */
    }

    /* Targets inline code values inside Streamlit alert messages. */
    div[data-testid="stAlert"] code {
        background-color: #0B0F19 !important; /* Adds a dark code background. */
        border-radius: 4px; /* Rounds the code background corners. */
        padding: 0.1rem 0.35rem; /* Adds space around the code value. */
        font-weight: 700; /* Makes the code value bold. */
    }

    /* Targets the currently selected Streamlit tab. */
    .stTabs [aria-selected="true"] {
        background-color: #162238 !important; /* Sets the active tab background. */
        color: #00D4FF !important; /* Sets the active tab label color. */
        border-color: #00D4FF80 !important; /* Sets the active tab border color. */
    }    
    </style>
    """,
    unsafe_allow_html = True
)

# Set the title and description of the main app page.
st.title("🤖 Automation Suite")
st.markdown("An automation suite to automate your daily tasks such as organising files, fetching weather data & sending an email to yourself with data of tasks completed.")
st.divider()

# Sidebar section to display status information and configuration checks.
st.sidebar.title("📡 Status Bar")
st.sidebar.markdown("This is a status bar to show, if all the dependencies are installed and configured.")
st.sidebar.divider()

# Check if the environment configuration file exists and show the target folder path.
st.sidebar.subheader("🔌 Configuration Status")
if os.path.exists("config.env") or ("WEATHER_KEY" in st.secrets):
    st.sidebar.success("🔒 Configuration: Connected")
    
    # Handle path display depending on environment
    if "WEATHER_KEY" in st.secrets:
        st.sidebar.info("🌐 Running on Cloud Server\nUsing Secure Vault Environment")
    else:
        from main import MY_PATH
        st.sidebar.info(f"📁 Target Root:\n`{MY_PATH}`")
else:
    st.sidebar.error("❌ Configuration: Missing")

st.sidebar.divider()

# Check whether required libraries are installed before running the app features.
st.sidebar.subheader("📦 Dependency Tracking")

required_libraries = ["requests", "dotenv", "pandas"]
missing_libraries = []

for lib in required_libraries:

    if importlib.util.find_spec(lib) is not None:
        st.sidebar.write(f"🟢 `{lib}` status: Installed")
    else:
        st.sidebar.write(f"🔴 `{lib}` status: Missing")
        missing_libraries.append(lib)

if missing_libraries:
    st.sidebar.error("🔴 Critical dependencies missing!")
    st.sidebar.warning(
        "🟡 To fix this, execute the following command in your terminal:\n"
        "```powershell\n"
        "pip install -r requirements.txt\n"
        "```"
    )

else:
    st.sidebar.success("🎉 All systems operational!")

# Create the main tabs for the different automation features.
tab1, tab2, tab3 = st.tabs(["📁 Organise Files",
                            "🌤️ Fetch Weather Data",
                            "📧 Send Email"
                           ])

# File organiser tab.
with tab1:
    st.header("📑 File Organiser")
    st.markdown("Organise your files in a folder by moving them to their respective folders based on their file extensions.")
    folder_name = st.text_input("Enter the name or path of the folder you want to organise:", placeholder="e.g. Documents\\MyFolder, Downloads, etc.")

    if (st.button("Organise Files", type = "primary", use_container_width = True)):
        # Organise files only if the app is running locally, not on a cloud server.
        if "WEATHER_KEY" in st.secrets:
            st.warning(
                "🟡 **Cloud Environment Restriction**\n\n"
                "Since this application is currently hosted on a cloud server, it operates in an isolated sandbox "
                "and cannot physically access your local system's file directory trees. "
                "To utilize the automated File Organiser workspace, please download the repository files from my "
                "[`GitHub repository`](https://github.com/prakket06/Automation-Suite) and execute the application suite locally on your machine!"
            )
        else:
            if folder_name:
                organizing_status = organize_files(folder_name)
                if organizing_status is True:
                    st.success(f"🟢 Files in `{folder_name}` have been organised successfully.")
                elif organizing_status is False:
                    st.error(f"🔴 Folder not found: `{folder_name}`.")
                else:
                    st.error(f"🔴 Failed to organise files in `{folder_name}`.")
            else:
                st.warning("🟡 Please enter a folder name first!!")

# Weather data fetcher tab.
with tab2:
    st.header("🌤️ Weather Data Fetcher")
    st.markdown("Fetch the weather data of a city of your choice and log it to a CSV file.")

    city = st.text_input("Enter the name of the city you want to fetch weather data for:", placeholder="e.g. Kanpur, Delhi, etc.")
    col1, col2 = st.columns([3, 2])

    with col1:
        if (st.button("Fetch & Log Weather Data", type = "primary", use_container_width=True)):
            if city:
                fetch_status = log_weather(city)
                if fetch_status is True:
                    st.success(f"🟢 Weather data for `{city.title()}` has been fetched and logged successfully.")
                elif fetch_status is False:
                    st.error(f"🔴 City not found: `{city.title()}`.")
                else:
                    st.error(f"🔴 Failed to fetch weather data for `{city.title()}`.")
            else:
                st.warning("🟡 Please enter a city name first!!")

    with col2:
        if ("show_history" not in st.session_state):
            st.session_state.show_history = False

        def toggle_history():
            """This function will toggle the show_history state variable to show or hide the weather log history on clicking the button.
              Args:
                   None
              Returns:
                  None
              """
            st.session_state.show_history = not st.session_state.show_history

        button_label = "Hide Weather Log History" if st.session_state.show_history else "Show Weather Log History"

        st.button(button_label, use_container_width=True, on_click=toggle_history)      # Toggle the show_history state variable on clicking the button.

    # Display the weather log history if the show_history state variable is True.
    if st.session_state.show_history:
        st.divider()
        st.subheader("📊 Weather Data")

        LOG_FILE = "LOG_FILE.csv"

        with st.spinner("Fetching weather log..."):
            if (os.path.exists(LOG_FILE)):
                try:
                    df = pd.read_csv(LOG_FILE, names = ["City", "Temperature (°C)", "Weather Description", "Date & Time"])
                    st.dataframe(df.iloc[::-1], use_container_width = True, hide_index = True)                                    # Reverse the dataframe to show the latest entry at the top.
                    button_label = "Hide Weather Log History" if st.session_state.show_history else "Show Weather Log History"
                except Exception as e:
                    st.error(f"🔴 Could not load Log File: {e}")
            else:
                st.warning(f"🟡 Log file not found. Please fetch weather data first.")

# Email sender tab.
with tab3:
    st.header("📨 Status Email Sender")
    st.markdown("Send an email to yourself with the status of the automation suite, including the weather data of the last 5 entries and the file organisation status.")

    # Fetch the latest weather data and generate the email body before sending.
    weather_data = fetch_weather_data()
    email_body = generate_mail_body(weather_data)

    if st.button("Send Status Email", type = "primary", use_container_width = True):
        with st.spinner("Establishing secure connection to SMTP server..."):
            mail_status = send_email(EMAIL, "Automation Suite Status - Web App", email_body)

        if mail_status is True:
            st.success(f"🟢 Execution report successfully dispatched to `{EMAIL}`!")
        else:
            st.error(f"🔴 Transmission failed. Verify your internet connection or check your Google App Password configuration.")