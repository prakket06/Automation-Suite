# Importing necessary libraries.
import os, importlib.util
import streamlit as st
from main import organize_files, log_weather, fetch_weather_data, generate_mail_body, send_email, EMAIL
import pandas as pd

# Configure the Streamlit page settings and layout.
st.set_page_config(
    page_title="Automation Suite",
    page_icon="🤖⚡",
    layout="centered",
    initial_sidebar_state="expanded")

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
                "⚠️ **Cloud Environment Restriction**\n\n"
                "Since this application is currently hosted on a cloud server, it operates in an isolated sandbox "
                "and cannot physically access your local system's file directory trees. "
                "To utilize the automated File Organiser workspace, please download the repository files from my "
                "[GitHub repository](https://github.com/prakket06/Automation-Suite) and execute the application suite locally on your machine!"
            )
        else:
            if folder_name:
                organizing_status = organize_files(folder_name)
                if organizing_status is True:
                    st.success(f"🟢 Files in {folder_name} have been organised successfully.")
                elif organizing_status is False:
                    st.error(f"🔴 Folder not found: {folder_name}.")
                else:
                    st.error(f"🔴 Failed to organise files in {folder_name}.")
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
                    st.success(f"🟢 Weather data for {city.title()} has been fetched and logged successfully.")
                elif fetch_status is False:
                    st.error(f"🔴 City not found: {city.title()}.")
                else:
                    st.error(f"🔴 Failed to fetch weather data for {city.title()}.")
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
                    st.dataframe(df.iloc[::-1], use_container_width = True, hide_index = True)                                      # Reverse the dataframe to show the latest entry at the top.
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
            st.success(f"🟢 Execution report successfully dispatched to {EMAIL}!")
        else:
            st.error(f"🔴 Transmission failed. Verify your internet connection or check your Google App Password configuration.")