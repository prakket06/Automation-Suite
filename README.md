# *AUTOMATION SUITE*

## OVERVIEW

This project is built to automate some of the basic daily tasks on your computer, like:-

1. **Organising files:** Automatically organise files in a folder based on the extension to subfolders.

2. **Logging weather data:** Log current weather data of the city you provide to a csv file.

3. **Get status through E-mail:** Send yourself an E-mail containing details of tasks completed.

---

## FEATURES

1. **Automatic Path Handling:** Specify your parent directory, in the **config.env** file once, then for each use give the sub-paths only, the code will handle full path itself.

2. **CSV Data Appending:** All your weather search history is saved in a local csv file, without getting overwritten in every use.

3. **Safe & Concise E-mail:** A safe SMTP connection is established before logging in to your mail-id, then a concise mail telling number of files organised & last 5 weather entries is sent to you.

4. **Streamlit Interactive Shell Dashboard:** An interactive graphic interface setup to interact with the app on browser graphically. The workspace breaks operations into dedicated, click-responsive navigation tabs (`📁 Organise Files`, `🌤️ Fetch Weather Data`, `📧 Send Email`) for clean, minimalistic space desktop management.

---

## SYSTEM CONTROL PANEL & DIAGNOSTICS

The dashboard loads with an integrated pre-flight safety control panel pinned to the persistent left sidebar browser window. It acts defensively to scan deployment environments before any computational engine tasks execute:

* **Configuration Status Check:** Instantly parses local workspace root trees to verify if the cryptographic credential parameters file (`config.env`) physically exists.
* **Dependency Monitoring Array:** Runs a complete environmental module scan checking external required third-party installations (`requests`, `python-dotenv`, `pandas`). If any runtime modules are absent, the array flags the anomaly and visualizes the recovery script block.

---

## PREREQUISITES & INSTALLATION

1. Make sure you have a **Python version 3.6+** installed.

2. This project uses some external libraries to manage files, send mails, get weather data, etc. so download them before running the programme, by running following command in terminal window.

```bash
pip install -r requirements.txt
```

To boot the graphical web dashboard interface, execute the following custom run command in your terminal window:

```bash
streamlit run app.py
```

---

## CONFIGURATION

Before using the programme you will have to create a **config.env** file & configure these variables in the file.

1. **WEATHER_KEY:** Your OpenWeatherMap API key.

2. **EMAIL:** Your E-mail address.

3. **APP_PASSWORD:** Your google account apps password.

4. **MY_PATH:** Your parent drive or directory path.

**<u>NOTE</u>:-** The template for config.env file is also provided in a **config.env.example** file, it can also be used after being renamed to **config.env**

---

## USAGE EXAMPLE

<img title="" src="Usage Example.png" alt="Home Page" data-align="center">

<sup><i>Home Page</i></sup>



<img title="" src="File Organiser.png" alt="File Organiser" data-align="center">

<sup><i>File Organiser</i></sup>


<img src="usage_preview.gif" alt="Fetch Weather Usage gif" width="80%" data-align = "center">

<sup><i>Fetch Weather Usage</i></sup>
