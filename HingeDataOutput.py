# Creating a Hinge Data Output script

# Hinge enables you to request and export your data from the app
# Using this export I have created a script to show basic outputs based on likes sent and received

# Please Note: Some code in this project was taken from Michael Johnson's "hinge_cleanup.py" code on GitHub,
# which is referenced below in lines 55-91
# Michael Johnson's hinge code: https://gist.github.com/mistermichaelll/3afcc33188f29576915243a5a2ea2a72

# Author: Selam Haile
# Last Updated: 3rd March 2025

# =====================================================================================================================
# Gathering the Data
# =====================================================================================================================

import os  # Provides functions to interact with the operating system
import json  # Provides functions to work with JSON data
import pandas as pd  # Data manipulation and analysis library
from datetime import datetime  # Provides functions to manipulate date and time
import matplotlib.pyplot as plt  # Library for creating visualizations
import seaborn as sns  # Data visualization library based on matplotlib

# Path to your Hinge matches JSON file
file_path = "C:/Users/YourName/Documents/Data/Hinge Data Export - YourName/export/matches.json"

# Read and normalize the JSON data using pandas
with open(file_path, 'r') as file:  # Open the JSON file in read mode
    matches = json.load(file)  # Load the JSON data into a Python object
data = pd.json_normalize(matches)  # Convert the nested JSON data into a flat pandas DataFrame


# =====================================================================================================================
# Quick Stats on Matches start & end date
# =====================================================================================================================

# Extract the timestamps from the 'match' objects and convert them to datetime objects
timestamps = [datetime.strptime(match['timestamp'], '%Y-%m-%d %H:%M:%S')
              for item in matches if 'match' in item  # Check if 'match' key exists in the item
              for match in item['match'] if 'timestamp' in match]  # Check if 'timestamp' key exists in the 'match'

if timestamps:
    earliest_timestamp = min(timestamps)  # Find the earliest timestamp
    latest_timestamp = max(timestamps)  # Find the latest timestamp
    duration = latest_timestamp - earliest_timestamp  # Calculate the duration between the earliest and latest timestamps

    # Print the results
    print("The first match was on:", earliest_timestamp.strftime('%Y-%m-%d'))
    print("The latest match was on:", latest_timestamp.strftime('%Y-%m-%d'))
    print("The duration between the earliest and latest timestamps is:", duration)
else:
    print("No valid timestamps found in the data.")


# =====================================================================================================================
# Gathering the JSON Matches Data
# =====================================================================================================================
# Code in this section was taken from Michael Johnson's "hinge_cleanup.py" code on GitHub,
# with minor edits made by me
# Michael's Github: https://gist.github.com/mistermichaelll
# Michael's hinge code: https://gist.github.com/mistermichaelll/3afcc33188f29576915243a5a2ea2a72

# =====================================================================================================================
# Filter the DataFrame to get rows where both 'like' and 'match' are not NaN (outgoing matches)
outgoing_matches = data.loc[data["like"].notna() & data["match"].notna()].reset_index(drop=True)

# Filter the DataFrame to get rows where 'like' is not NaN and 'match' is NaN (outgoing no matches)
outgoing_no_matches = data.loc[data["like"].notna() & data["match"].isna()].reset_index(drop=True)

# Filter the DataFrame to get rows where 'match' is not NaN and 'like' is NaN (incoming matches)
incoming_match = data.loc[data["match"].notna() & data["like"].isna()].reset_index(drop=True)

# Filter the DataFrame to get rows where both 'like' and 'match' are NaN (incoming no matches)
incoming_no_match = data.loc[data["like"].isna() & data["match"].isna()].reset_index(drop=True)


# Print quick statistics about likes and matches
total_likes_sent = len(outgoing_matches) + len(outgoing_no_matches)
total_matches_from_likes_sent = len(outgoing_matches)
match_percent_from_likes_sent = round(len(outgoing_matches) / total_likes_sent * 100)

total_likes_received = len(incoming_match) + len(incoming_no_match)
total_matches_from_likes_received = len(incoming_match)
match_percent_from_likes_received = round(len(incoming_match) / total_likes_received * 100)

print("Total Likes Sent:", total_likes_sent)
print("Total Matches from Likes Sent:", total_matches_from_likes_sent)
print("Match % from Likes Sent:", match_percent_from_likes_sent, "%")
print("Total Likes Received:", total_likes_received)
print("Total Matches from Likes Received:", total_matches_from_likes_received)
print("Match % from Likes Received:", match_percent_from_likes_received, "%")

# =====================================================================================================================
# Creating an output pie and bar chart
# =====================================================================================================================

# Set up the plotting style
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))

# Bar Plot: Total Likes Sent and Received
plt.subplot(2, 2, 1)
x = ["Likes Sent", "Likes Received"]
y = [total_likes_sent, total_likes_received]

sns.barplot(x=x, y=y, hue=x, palette="pastel", legend=False)

plt.title("Total Likes Sent vs. Received")
plt.ylabel("Likes")

# Pie Chart: Distribution of Interaction Types
plt.subplot(2, 2, 2)
interaction_counts = pd.Series({
    "Outgoing Matches": total_matches_from_likes_sent,
    "Outgoing No Matches": len(outgoing_no_matches),
    "Incoming Matches": total_matches_from_likes_received,
    "Incoming No Matches": len(incoming_no_match)
})
interaction_counts.plot.pie(autopct="%1.0f%%", colors=sns.color_palette("pastel"), wedgeprops=dict(edgecolor='k'))
plt.title("Distribution of Interaction Types")
plt.ylabel("")

# Display the plots
plt.suptitle("Hinge Data Visualization", fontsize=16)
plt.tight_layout()
plt.show()
