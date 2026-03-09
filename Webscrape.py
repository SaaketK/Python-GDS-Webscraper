import cloudscraper
import json
import datetime
from datetime import date

print("Enter today/tomorrow or a specific date in YYYY-MM-DD format: ")
DATE = input()

if DATE == "today":
    DATE = date.today()
if DATE == "tomorrow":
    DATE = date.today() + datetime.timedelta(days=1)

print("Enter breakfast/lunch/dinner: ")
MEAL_NAME = input()

# Highlander Commons Location ID
LOCATION_ID = "615f4f93a9f13a32678e5feb"

scraper = cloudscraper.create_scraper()

print(f"Getting {MEAL_NAME} for {DATE} ")

periods_url = f"https://apiv4.dineoncampus.com/locations/{LOCATION_ID}/periods?platform=0&date={DATE}"
print(periods_url)

try:
    response = scraper.get(periods_url)

    if response.status_code != 200:
        print(f"Error fetching periods. Status: {response.status_code}")
        # Print first 100 chars to check if 404 page
        print(f"Response: {response.text[:100]}")
        exit()

    data = response.json()

except Exception as e:
    print(f"critical error: {e}")
    exit()

period_id = None

# The API returns a list of periods for the day (Breakfast, Lunch, Dinner)
# Match the period to user input
if 'periods' in data:
    for period in data['periods']:
        if period['name'].lower() == MEAL_NAME.lower():
            period_id = period['id']
            print(f"Period ID: {period_id}")
            break

if not period_id:
    print(f"Error: '{MEAL_NAME}' was not found in the schedule for {DATE}.")
    print("Available meals found:", [p['name'] for p in data.get('periods', [])])
    exit()

# Use parameters to create API request for menu items
menu_url = f"https://apiv4.dineoncampus.com/locations/{LOCATION_ID}/menu?date={DATE}&period={period_id}"

menu_response = scraper.get(menu_url)
menu_data = menu_response.json()

print(f"\nMENU FOR {MEAL_NAME.upper()}")

# Get categories
categories = menu_data.get('menu', {}).get('periods', {}).get('categories', [])
if not categories:
    categories = menu_data.get('period', {}).get('categories', [])

found = False
for category in categories:
    # Filter for The Daily Plate
    if MEAL_NAME.lower() == "breakfast":
        if category['name'] == "The Daily Plate":
            found = True
            print(f"{category['name']} ")
            for item in category['items']:
                print(f"  - {item['name']}")
            break
    else:
        # Check for Carvery
        if category['name'] == "The Daily Plate" or category['name'] == "Carved & Crafted":
            found = True
            if category['name'] == "Carved & Crafted" and len(category['items']) == 0:
                break
            print(f"{category['name']} ")
            for item in category['items']:
                print(f"  - {item['name']}")


if not found:
    print("(The Daily Plate not found)")