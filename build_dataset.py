import json
import pandas as pd
import helper
import ast
import numpy as np

file_path = "Yelp-JSON/Yelp JSON/yelp_dataset/yelp_academic_dataset_business.json"

# Extract each line from the JSON file
data = []
with open(file_path, "r", encoding = "utf-8") as file:
    for line in file:
        data.append(json.loads(line))

# Convert to data frame
df = pd.DataFrame(data)

# Filter data to only include restaurants in the Tampa Bay area
df = df[df["state"] == "FL"]
df["city"] = df["city"].apply(helper.normalize_cities)
df = df[df["city"].isin(helper.tampa_bay_cities)]
df = df[df["categories"].str.contains("Restaurants")]
df = df[df["is_open"] == 1]
df["address"] = df["address"].replace(["", "None", "none"], np.nan)
df = df.dropna(subset=["address"])

def parse_attributes(attribute):
    # Handle null cases
    if pd.isna(attribute):
        return ""
    
    # Convert all attributes to dicts
    if isinstance(attribute, str):
        try:
            attribute = ast.literal_eval(attribute)
        except:
            return ""
    
    # If not a dict, return empty
    if not isinstance(attribute, dict):
        return ""
    
    features = []
    for key, value in attribute.items():
        # If its a bool, only add if the value is true
        if isinstance(value, bool) and value:
            features.append(key.lower())
        # If its a dict, only add the true values in the dict
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if sub_value:
                    features.append(f"{key}_{sub_key}".lower())
        elif isinstance(value, str):
            # If its a stringed dict, convert to a dict and only add the true values
            if value.startswith('{'):
                nested = ast.literal_eval(value)
                for sub_key, sub_value in nested.items():
                    if sub_value:
                        features.append(f"{key}_{sub_key}".lower())
                continue
            clean_value = value.strip("u'\"").lower()
            # For restaurant prices, add readable descriptors
            if key.lower() == "restaurantspricerange2":
                price_map = {
                    "1": "cheap budget inexpensive affordable",
                    "2": "moderate casual",
                    "3": "upscale fancy",
                    "4": "luxury premium fine dining"
                }
                if clean_value in price_map:
                    features.append(price_map[clean_value])
                    continue
            # If its just a string, only add if the string is true or some other value that does not mean false
            if clean_value == "true":
                features.append(key.lower())
            elif clean_value not in ["none", "false", "no", ""]:
                features.append(f"{key}_{clean_value}".lower())
 
    return " ".join(features)

# Parse attributes
df["parsed_attributes"] = df["attributes"].apply(parse_attributes)
# Replace commas with whitespaces in categories
df["categories"] = df["categories"].str.replace(",", " ")
# Create restaurant tags
df["tags"] = df["categories"] + " " + df["categories"] + " " + df["parsed_attributes"]
# Remove extra whitespaces and normalize tags
df["tags"] = df["tags"].str.replace(r"\s+", " ", regex=True).str.strip()
df["tags"] = df["tags"].apply(helper.normalize_text)

# Only include columns needed
df = df[[
    "name",
    "address",
    "city",
    "stars",
    "review_count",
    "tags"
]]

# Create new cleaned dataset file
df.to_csv("dataset.csv", index=False)