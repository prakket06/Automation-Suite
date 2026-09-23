# *AUTOMATION SUITE*

## OVERVIEW

This project is built to automate some daily tasks on your computer, like:-

1. **Organising files:** Automatically organise files in a folder based on the extension to subfolders.

2. **Logging weather data:** Log current weather data of the city you provide to a csv file.

3. **Get status through E-mail:** Send yourself an E-mail containing details of tasks completed.

---

## FEATURES

1. **Automatic Path Handling:** Specify your parent directory, directly in the code once, then for each use give the sub-paths only, the code will handle full path.

2. **CSV Data Appending:** All your weather search history is saved in a local csv file, without getting overwritten in every use.

3. **Safe & Concise E-mail:** A safe SMTP connection is established before logging in to your mail-id, then a concise mail telling number of files moved & last 5 weather entries is send to you.

---

## PREREQUISITES & INSTALLATION

1. Make sure you have a **Python version 3.6+** installed.

2. This project uses some external libraries to manage files, send mails, get weather data, etc. so download them before running the programme, by running following command in command prompt.

```bash
pip install -r requirements.txt
python main.py
```

---

## CONFIGURATION

Before using the programme you will have to create a **config.env** file & configure these variables in the file.

1. **WEATHER_KEY:** Your OpenWeatherMap API key.

2. **EMAIL:** Your E-mail address.

3. **APP_PASSWORD:** Your google account app password.

4. **MY_PATH:** Your parent drive or directory path.

**<u>NOTE</u>:-** The template for config.env file is also provided in a **config.env.example** file, it can also be used after being renamed to **config.env**

---

## USAGE EXAMPLE

![](C:\Users\Prakket\Desktop\Automation%20Suite\Usage%20Example.png)