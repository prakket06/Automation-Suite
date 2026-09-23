# Importing necessary libraries.
import os, shutil, smtplib, requests, csv, datetime
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file.
load_dotenv("config.env")

# Configuration variables.
WEATHER_KEY = os.environ.get("WEATHER_KEY")
FOLDERS = {
    ".pdf": "Documents", ".docx": "Documents",
    ".jpg": "Images",    ".png": "Images",
    ".mp4": "Videos",    ".mp3": "Music",
}
EMAIL = os.environ.get("EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")
LOG_FILE = "LOG_FILE.csv"
moved_files = {}
MY_PATH = os.environ.get("MY_PATH")

# Functions.
def organize_files(folder):
    """
    Organise files in the given folder to subfolders based on their extensions.

    Args:
        folder: The name of folder to organise., e.g. 'Downloads'
    
    Returns: None
    """

    folder = os.path.join(MY_PATH, folder)  # Create full folder path.

    # Try to loop through each item in the folder and move files to their respective subfolders.
    try:
        for f in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, f)) and not (f.startswith('.') or f.lower() == 'desktop.ini'):
                ext = os.path.splitext(os.path.join(folder, f))[1].lower()                                      # Get the file extension in lowercase.
                dest = FOLDERS.get(ext, "Others")                                                            # Get the destination folder based on the extension, if not found then move to "Others" folder.
                os.makedirs(os.path.join(folder, dest), exist_ok = True)                                        # Create the destination folder if it doesn't exist.
                shutil.move(os.path.join(folder, f), os.path.join(folder, dest))                                # Move the file to the destination folder.
                moved_files[dest] = moved_files[dest] + 1 if dest in moved_files else 1
        return True
    except FileNotFoundError:
        print(f"Folder not found: {folder}.")
        return False
    except Exception as e:
        print("Something happened.")
        print(f"Error: {e}.")
        return None



def send_email(to, subject, body):
    """
    Send an email to myself with status of the automation suite.
    
    Args:
        to: The email address to send the email to, which is also the sender's email address.
        subject: The subject of the email.
        body: The body of the email.
    
    Returns:
        None
    """

    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)     # Create a SMTP connection to Gmail's SMTP server on port 587.
        s.starttls()                                 # Upgrade the connection to a secure encrypted SSL/TLS connection.
        s.login(to, APP_PASSWORD)                    # Login to the Gmail account using the provided email address and app password.
        msg = EmailMessage()                        # Create a new email message object.
        msg["Subject"] = subject                     # Set the subject of the email.
        msg["From"] = to                            # Set the sender's email address.
        msg["To"] = to                              # Set the recipient's email address, which is the same as the sender's email address.
        msg.set_content(body)                         # Set the body of the email.
        s.send_message(msg)                          # Send the email message using the SMTP connection.
        s.quit()                                    # Close the SMTP connection.
        print("Mail sent.")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def log_weather(city):
    """
    Log the weather data of the given city to a CSV file.
    
    Args:
        city: The name of the city to log the weather data for.
        
    Returns:
        None"""

    # URL for weather data from OenWeatherMap API.
    url = ("https://api.openweathermap.org/data/2.5/weather"
           f"?q={city}&appid={WEATHER_KEY}&units=metric")

    # Try to fetch weather data from API, if there is an error print error message & return None.
    try:
        r = requests.get(url, timeout=10)
    except requests.exceptions.RequestException:
        print("Network Problem! Check Internet")
        return None

    # If the data is fetched successfully, log the weather data to a CSV file, else print error message.
    if r.status_code == 200:
        try:
            with open(LOG_FILE, "a", newline = "") as f:
                writer = csv.writer(f)
                data = r.json()
                writer.writerow([data["name"], data["main"]["temp"], data["weather"][0]["description"], datetime.datetime.now().strftime("%d %b, %Y %H:%M:%S")])
                print(f"Weather logged for {city.title()}.")
                return True
        except Exception as e:
            print(f"Error writing to log file: {e}")
            return None

    elif r.status_code == 404:
        print(f"City not found: {city}.")
        return False
    return None

def fetch_weather_data():
    """
    Fetch the last 5 entries of weather data from the CSV file.
    
    Args:
        None
    
    Returns:
        A list of the last 5 entries of weather data from the CSV file, if available else all data."""

    try:
        with open(LOG_FILE, "r") as f:
                reader = csv.reader(f)
                data = list(reader)
                return data[-5:] if len(data) >= 5 else data
    except FileNotFoundError:
        print("Log file not found.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def generate_mail_body(weather_data):
    """
    Generate the body of the email to send status, with the weather data and file organization status.
    
    Args:
        weather_data: A list of the last 5 entries of weather data from the CSV file
        
    Returns:
        A string containing the body of the email to send status, with the weather data and file organization status.
    """

    body = "Automation Suite Status:\n\nWeather Data of Last 5 Entries:\n"

    # Add each entry of weather_data to the body of the email.
    try:
        for row in weather_data:
            body += f"{row[0]}: {row[1]}°C, {row[2]} on {row[3]}\n"

        body += "\nFile Organization:\n"

        # If any files were moved, add the count of files moved to each folder to the body of the email.
        if (len(moved_files) > 0):
            for folder, count in moved_files.items():
                body += f"Moved {count} files to {folder}.\n"

        return body
    except Exception as e:
        print(f"Error generating email body: {e}")
        return "Error generating email body."

def main():
    """
    Main function to take user input and call the appropriate functions based on the user's choice.
    
    Args:
        None
    
    Returns:
        None
    """

    while True:
        print("\n=== MY AUTOMATION SUITE ===")
        print("1. Organize files  2. Weather log")
        print("3. Email me a status  4. Quit")

        try:
            choice = input("Choose: ").lower().replace(" ", "")

            if (choice == "1" or choice == "organizefiles"):
                folder_name = input("Enter name of folder you want to organize: ")
                organize_files(folder_name)
            elif (choice == "2" or choice == "weatherlog"):
                city = input("Enter city name: ")
                log_weather(city)
            elif (choice == "3" or choice == "emailstatus"):
                subject = "Automation Suite Status"
                weather_data = fetch_weather_data()
                body = generate_mail_body(weather_data)
                send_email(EMAIL, subject, body)
            elif (choice == "4" or choice == "quit"):
                print("Bye!")
                break
            else:
                print("Invalid choice! Try again.")
        except TypeError:
            print("Invalid input! Try again.")
        except Exception as e:
            print(f"Error: {e}. Try again.")

if (__name__ == "__main__"):
    main()