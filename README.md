# Dine On Campus Menu Scraper

A Python Script to fetch specific meal menus for the Highlander Commons dining hall. It interacts with the Dine On Campus API to retrieve daily menu items

## Features

* Date Selection: Supports 'today', 'tomorrow', or a manual 'YYYY-MM-DD' entry
* Meal Filtering: Specifically targets The Daily Plate for all meals and Carved and Crafted for lunch and dinner
* Dynamic ID Mapping: Automatically finds the correct period_id for the requested meal

### Usage

1. Date: Enter 'today', 'tomorrow', or a specific date like '2026-03-15'.
2. Meal: Enter 'breakfast', 'lunch', or 'dinner'.
3. Output: The script will print the items available at The Daily Plate and if lunch/dinner will also print Carved and Crafted stations

## How it Works

1. Period Lookup: It hits the /periods endpoint for the specified date to find the unique ID for the requested meal
2. Menu Retrieval: It uses the period_id and the LOCATION_ID, and provided date to pull the full menu JSON and parses out the specific categories
