"""
Auto-generated from Webscrappinffinal.ipynb
This script concatenates code cells in order. Review & refactor into functions/CLI as needed.
"""


# ---- Code cells ----

# Cell 1
Found 15 tables.

Table 1:
               0   1
0  BRIDGEPORT,CT NaN

========================================

Table 2:
   Valuation Year Improvements      Land     Total
0            2024     $108,720  $112,720  $221,440

========================================

Table 3:
   Valuation Year Improvements     Land     Total
0            2024      $76,100  $78,900  $155,000

========================================

Table 4:
          0                                       1
0     Owner                 LARES JOSE J & PATRICIA
1  Co-Owner                                     NaN
2   Address  48 GASPEE RD BRIDGEPORT, CT 06606-1709

========================================

Table 5:
             0          1
0   Sale Price   $250,000
1  Certificate        NaN
2  Book & Page  10284/207
3          NaN        NaN
4          NaN        NaN

========================================

Table 6:
                            Owner Sale Price  Certificate Book & Page  \
0         LARES JOSE J & PATRICIA   $250,000          NaN   10284/207   
1                  ESPINOSA LUISA         $0          NaN   10036/127   
2  ESPINOSA LUIS & LUISA ESPINOSA   $258,000          NaN   6304/0100   
3              ROSENKRANZ SARAH L   $175,000          NaN   4824/0245   
4    SAMPAIO AMILCAR & LEOPOLDINA   $132,000          NaN   4232/0069   

  Instrument   Sale Date  
0         00  09/21/2020  
1         01  06/10/2019  
2       UNKQ  03/21/2005  
3       UNKQ  02/19/2002  
4       UNKQ  11/01/1999  

========================================

Table 7:
                                      0         1
0                           Year Built:      1960
1                          Living Area:      1092
2                     Replacement Cost:  $155,318
3                Building Percent Good:        70
4  Replacement Cost  Less Depreciation:  $108,720

========================================

Table 8:
        Field  Description
0      Style:        Ranch
1       Model  Residential
2      Grade:            C
3    Stories:         1.00
4  Occupancy:            1

========================================

Table 9:
  Code                 Description  Gross Area  Living Area
0  BAS                 First Floor        1092         1092
1  BSM                    Basement        1092            0
2  FEP              Enclosed Porch         212            0
3  PTO                       Patio         145            0
4  UST  Unfinished Utility Storage         286            0

========================================

Table 10:
                            0                           1  \
0  No Data for Extra Features  No Data for Extra Features   

                            2                           3  \
0  No Data for Extra Features  No Data for Extra Features   

                            4                           5  \
0  No Data for Extra Features  No Data for Extra Features   

                            6                           7  \
0  No Data for Extra Features  No Data for Extra Features   

                            8  
0  No Data for Extra Features  

========================================

Table 11:
               0              1
0       Use Code            101
1    Description  Single Family
2           Zone             RA
3   Neighborhood             20
4  Alt Land Appr             No

========================================

Table 12:
                 0         1
0     Size (Acres)      0.20
1         Frontage         0
2            Depth         0
3   Assessed Value   $78,900
4  Appraised Value  $112,720

========================================

Table 13:
                          0                         1  \
0  No Data for Outbuildings  No Data for Outbuildings   

                          2                         3  \
0  No Data for Outbuildings  No Data for Outbuildings   

                          4                         5  \
0  No Data for Outbuildings  No Data for Outbuildings   

                          6                         7  \
0  No Data for Outbuildings  No Data for Outbuildings   

                          8  
0  No Data for Outbuildings  

========================================

Table 14:
   Valuation Year Improvements      Land     Total
0            2023     $108,720  $112,720  $221,440
1            2022     $108,720  $112,720  $221,440
2            2021     $108,720  $112,720  $221,440

========================================

Table 15:
   Valuation Year Improvements     Land     Total
0            2023      $76,100  $78,900  $155,000
1            2022      $76,100  $78,900  $155,000
2            2021      $76,100  $78,900  $155,000

========================================


# Cell 2
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

# List of URLs to scrape
urls = [
    "https://gis.vgsi.com/bridgeportct/Parcel.aspx?pid=1763",
    "https://gis.vgsi.com/bridgeportct/Parcel.aspx?pid=2326",
    "https://gis.vgsi.com/bridgeportct/Parcel.aspx?pid=1764",
    "https://gis.vgsi.com/bridgeportct/Parcel.aspx?pid=27051",
"https://gis.vgsi.com/bridgeportct/Parcel.aspx?pid=26995",
"https://gis.vgsi.com/bridgeportct/Parcel.aspx?pid=27052",
]

# Function to fetch page and parse the HTML
def fetch_page(url):
    # Fetch the page content
    response = requests.get(url, verify=False)
    response.raise_for_status()  # Check if the request was successful

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the entire page content
    page_content = soup.prettify()
    
    return page_content

# Function to process and extract data from the page
def process_page(page_content):
    # Use pandas to read the tables from the HTML
    tables = pd.read_html(page_content)

    # Extract specific tables (Table 6, Table 9, and Table 4)
    table_6 = tables[5]  # Table 6 is at index 5
    table_9 = tables[8]  # Table 9 is at index 8
    table_4 = tables[3]  # Table 4 is at index 3

    # Extract "Owner" from the first row, second column in Table 4
    owner = table_4.iloc[0, 1]

    # Extract "Address" from the third row, second column in Table 4
    address = table_4.iloc[2, 1]

    # Extract the pincode from the address (assuming the pincode is the last part of the address)
    pincode_match = re.search(r'\d{5}(-\d{4})?', address)
    pincode = pincode_match.group(0) if pincode_match else 'Unknown'

    # Filter out "Co-Owner" and "Address" rows, keeping only "Owner"
    table_4_cleaned = table_4[table_4[0] == 'Owner']

    # Add address and pincode columns to each table
    table_6['Address'] = address
    table_6['Pincode'] = pincode

    table_9['Address'] = address
    table_9['Pincode'] = pincode

    # Using .loc to modify the cleaned table, avoiding the SettingWithCopyWarning
    table_4_cleaned.loc[:, 'Address'] = address
    table_4_cleaned.loc[:, 'Pincode'] = pincode

    return table_6, table_9, table_4_cleaned

# Lists to store the combined tables for all URLs
combined_table_6 = []
combined_table_9 = []
combined_table_4_cleaned = []

# Scrape and process each URL
for url in urls:
    print(f"Scraping {url}...")
    page_content = fetch_page(url)
    table_6, table_9, table_4_cleaned = process_page(page_content)
    
    # Append the processed tables to the combined lists
    combined_table_6.append(table_6)
    combined_table_9.append(table_9)
    combined_table_4_cleaned.append(table_4_cleaned)

# Concatenate the data from all URLs for each table
final_table_6 = pd.concat(combined_table_6, ignore_index=True)
final_table_9 = pd.concat(combined_table_9, ignore_index=True)
final_table_4_cleaned = pd.concat(combined_table_4_cleaned, ignore_index=True)

# Create a new Excel file with 3 sheets
with pd.ExcelWriter('property_details_combined.xlsx') as writer:
    final_table_6.to_excel(writer, sheet_name='Sales Data', index=False)
    final_table_9.to_excel(writer, sheet_name='Area Details', index=False)
    final_table_4_cleaned.to_excel(writer, sheet_name='Owner Details', index=False)

print("All tables have been combined and saved to property_details_combined.xlsx.")


# Cell 3
!pip install pandas beautifulsoup4 lxml


# Cell 5
# working on this to scrap the whole database of bridgeport
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests

# Function to fetch the main street page and extract all the street URLs
def fetch_main_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    street_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Streets.aspx?Name=' in link['href']
    ]
    
    return street_links

# Function to fetch the street page and extract all property links
def fetch_street_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    property_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Parcel.aspx?pid=' in link['href']
    ]
    
    return property_links

# Function to fetch page and parse the HTML
def fetch_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser').prettify()

# Function to process and extract data from the page
def process_page(page_content):
    tables = pd.read_html(page_content)
    
    table_6 = tables[5]
    table_9 = tables[8]
    table_4 = tables[3]
    table_2 = tables[1]
    table_3 = tables[2]
    table_14 = tables[13]
    table_15 = tables[14]
    table_7 = tables[6]
    table_11 = tables[10]
    table_12 = tables[11]
    
    owner = table_4.iloc[0, 1]
    address = table_4.iloc[2, 1]
    pincode_match = re.search(r'\d{5}(-\d{4})?', address)
    pincode = pincode_match.group(0) if pincode_match else 'Unknown'
    
    table_4_cleaned = table_4[table_4[0] == 'Owner']
    
    for table in [table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15]:
        table['Address'] = address
        table['Pincode'] = pincode
    
    # Transform Table 7 to a horizontal format
    table_7_transposed = table_7.set_index(table_7.columns[0]).T.reset_index(drop=True)
    table_7_transposed['Address'] = address
    table_7_transposed['Pincode'] = pincode
    
    # Transform Table 11 to a horizontal format
    table_11_transposed = table_11.set_index(table_11.columns[0]).T.reset_index(drop=True)
    table_11_transposed['Address'] = address
    table_11_transposed['Pincode'] = pincode
    
    # Transform Table 12 to a horizontal format
    table_12_transposed = table_12.set_index(table_12.columns[0]).T.reset_index(drop=True)
    table_12_transposed['Address'] = address
    table_12_transposed['Pincode'] = pincode
    
    return table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_7_transposed, table_11_transposed, table_12_transposed

# Initialize lists to store all scraped data
combined_table_6 = []
combined_table_9 = []
combined_table_4_cleaned = []
combined_table_2 = []
combined_table_3 = []
combined_table_14 = []
combined_table_15 = []
combined_table_7 = []
combined_table_11 = []
combined_table_12 = []

# Main URL for scraping all street links
main_url = "https://gis.vgsi.com/bridgeportct/Streets.aspx"
street_links = fetch_main_page(main_url)

# Iterate through each street URL and scrape data
for street_url in street_links:
    print(f"Processing {street_url}")
    
    # Fetch all property links from the street page
    property_links = fetch_street_page(street_url)
    
    # Scrape and process each property URL
    for url in property_links:
        page_content = fetch_page(url)
        table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_7_transposed, table_11_transposed, table_12_transposed = process_page(page_content)
        
        combined_table_6.append(table_6)
        combined_table_9.append(table_9)
        combined_table_4_cleaned.append(table_4_cleaned)
        combined_table_2.append(table_2)
        combined_table_3.append(table_3)
        combined_table_14.append(table_14)
        combined_table_15.append(table_15)
        combined_table_7.append(table_7_transposed)
        combined_table_11.append(table_11_transposed)
        combined_table_12.append(table_12_transposed)

# Concatenate all the data into final tables
final_table_6 = pd.concat(combined_table_6, ignore_index=True)
final_table_9 = pd.concat(combined_table_9, ignore_index=True)
final_table_4_cleaned = pd.concat(combined_table_4_cleaned, ignore_index=True)
final_table_2 = pd.concat(combined_table_2, ignore_index=True)
final_table_3 = pd.concat(combined_table_3, ignore_index=True)
final_table_14 = pd.concat(combined_table_14, ignore_index=True)
final_table_15 = pd.concat(combined_table_15, ignore_index=True)
final_table_7 = pd.concat(combined_table_7, ignore_index=True)
final_table_11 = pd.concat(combined_table_11, ignore_index=True)
final_table_12 = pd.concat(combined_table_12, ignore_index=True)

# Create a new Excel file with 11 sheets (removed Table 8)
with pd.ExcelWriter('property_details_combined_all_streets_full_website.xlsx') as writer:
    final_table_6.to_excel(writer, sheet_name='Sales Data', index=False)
    final_table_9.to_excel(writer, sheet_name='Area Details', index=False)
    final_table_4_cleaned.to_excel(writer, sheet_name='Owner Details', index=False)
    final_table_2.to_excel(writer, sheet_name='Appraisal', index=False)
    final_table_3.to_excel(writer, sheet_name='Assessment', index=False)
    final_table_14.to_excel(writer, sheet_name='Past Appraisal', index=False)
    final_table_15.to_excel(writer, sheet_name='Past Assessment', index=False)
    final_table_7.to_excel(writer, sheet_name='Building Details', index=False)
    final_table_11.to_excel(writer, sheet_name='Use and Zone', index=False)
    final_table_12.to_excel(writer, sheet_name='Size and Value', index=False)


# Cell 6
#this scrip will scrap whole I street ,  table 8 has removed becuz of concate issues
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests

# URL of the main page listing streets starting with "I"
main_page_url = r"https://gis.vgsi.com/bridgeportct/Streets.aspx?Letter=I"

# Function to fetch the main page and extract all street links
def fetch_main_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    street_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Streets.aspx?Name=' in link['href']
    ]
    
    return street_links

# Function to fetch the street page and extract all property links
def fetch_street_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    property_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Parcel.aspx?pid=' in link['href']
    ]
    
    return property_links

# Function to fetch page and parse the HTML
def fetch_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser').prettify()

# Function to process and extract data from the page
def process_page(page_content):
    tables = pd.read_html(page_content)
    
    table_6 = tables[5]
    table_9 = tables[8]
    table_4 = tables[3]
    table_2 = tables[1]
    table_3 = tables[2]
    table_14 = tables[13]
    table_15 = tables[14]
    table_7 = tables[6]
    table_11 = tables[10]
    table_12 = tables[11]
    
    owner = table_4.iloc[0, 1]
    address = table_4.iloc[2, 1]
    pincode_match = re.search(r'\d{5}(-\d{4})?', address)
    pincode = pincode_match.group(0) if pincode_match else 'Unknown'
    
    table_4_cleaned = table_4[table_4[0] == 'Owner']
    
    for table in [table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15]:
        table['Address'] = address
        table['Pincode'] = pincode
    
    # Transform Table 7 to a horizontal format
    table_7_transposed = table_7.set_index(table_7.columns[0]).T.reset_index(drop=True)
    table_7_transposed['Address'] = address
    table_7_transposed['Pincode'] = pincode
    
    # Transform Table 11 to a horizontal format
    table_11_transposed = table_11.set_index(table_11.columns[0]).T.reset_index(drop=True)
    table_11_transposed['Address'] = address
    table_11_transposed['Pincode'] = pincode
    
    # Transform Table 12 to a horizontal format
    table_12_transposed = table_12.set_index(table_12.columns[0]).T.reset_index(drop=True)
    table_12_transposed['Address'] = address
    table_12_transposed['Pincode'] = pincode
    
    return table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_7_transposed, table_11_transposed, table_12_transposed

# Initialize lists to store all scraped data
combined_table_6 = []
combined_table_9 = []
combined_table_4_cleaned = []
combined_table_2 = []
combined_table_3 = []
combined_table_14 = []
combined_table_15 = []
combined_table_7 = []
combined_table_11 = []
combined_table_12 = []

# Fetch the list of street URLs from the main page
street_urls = fetch_main_page(main_page_url)

# Iterate through each street URL and scrape data
for street_url in street_urls:
    property_links = fetch_street_page(street_url)
    
    # Scrape and process each property URL
    for url in property_links:
        page_content = fetch_page(url)
        table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_7_transposed, table_11_transposed, table_12_transposed = process_page(page_content)
        
        combined_table_6.append(table_6)
        combined_table_9.append(table_9)
        combined_table_4_cleaned.append(table_4_cleaned)
        combined_table_2.append(table_2)
        combined_table_3.append(table_3)
        combined_table_14.append(table_14)
        combined_table_15.append(table_15)
        combined_table_7.append(table_7_transposed)
        combined_table_11.append(table_11_transposed)
        combined_table_12.append(table_12_transposed)

# Concatenate all the data into final tables
final_table_6 = pd.concat(combined_table_6, ignore_index=True)
final_table_9 = pd.concat(combined_table_9, ignore_index=True)
final_table_4_cleaned = pd.concat(combined_table_4_cleaned, ignore_index=True)
final_table_2 = pd.concat(combined_table_2, ignore_index=True)
final_table_3 = pd.concat(combined_table_3, ignore_index=True)
final_table_14 = pd.concat(combined_table_14, ignore_index=True)
final_table_15 = pd.concat(combined_table_15, ignore_index=True)
final_table_7 = pd.concat(combined_table_7, ignore_index=True)
final_table_11 = pd.concat(combined_table_11, ignore_index=True)
final_table_12 = pd.concat(combined_table_12, ignore_index=True)

# Create a new Excel file with 11 sheets (removed Table 8)
with pd.ExcelWriter('property_details_combined_all_streets.xlsx') as writer:
    final_table_6.to_excel(writer, sheet_name='Sales Data', index=False)
    final_table_9.to_excel(writer, sheet_name='Area Details', index=False)
    final_table_4_cleaned.to_excel(writer, sheet_name='Owner Details', index=False)
    final_table_2.to_excel(writer, sheet_name='Appraisal', index=False)
    final_table_3.to_excel(writer, sheet_name='Assessment', index=False)
    final_table_14.to_excel(writer, sheet_name='Past Appraisal', index=False)
    final_table_15.to_excel(writer, sheet_name='Past Assessment', index=False)
    final_table_7.to_excel(writer, sheet_name='Building Details', index=False)
    final_table_11.to_excel(writer, sheet_name='Use and Zone', index=False)
    final_table_12.to_excel(writer, sheet_name='Size and Value', index=False)


# Cell 7
#this scrip will scrap multiple street table 8 has removed becuz of concate issues
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests

# List of street URLs you want to scrape
street_urls = [
    r"https://gis.vgsi.com/bridgeportct/Streets.aspx?Name=OAKDALE%20ST",
    r"https://gis.vgsi.com/bridgeportct/Streets.aspx?Name=IMPERIAL%20ST",
    r"https://gis.vgsi.com/bridgeportct/Streets.aspx?Name=INDIAN%20AV",
    r"https://gis.vgsi.com/bridgeportct/Streets.aspx?Name=INDIAN%20AVE"
]

# Function to fetch the street page and extract all property links
def fetch_street_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    property_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Parcel.aspx?pid=' in link['href']
    ]
    
    return property_links

# Function to fetch page and parse the HTML
def fetch_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser').prettify()

# Function to process and extract data from the page
def process_page(page_content):
    tables = pd.read_html(page_content)
    
    table_6 = tables[5]
    table_9 = tables[8]
    table_4 = tables[3]
    table_2 = tables[1]
    table_3 = tables[2]
    table_14 = tables[13]
    table_15 = tables[14]
    table_7 = tables[6]
    table_11 = tables[10]
    table_12 = tables[11]
    
    owner = table_4.iloc[0, 1]
    address = table_4.iloc[2, 1]
    pincode_match = re.search(r'\d{5}(-\d{4})?', address)
    pincode = pincode_match.group(0) if pincode_match else 'Unknown'
    
    table_4_cleaned = table_4[table_4[0] == 'Owner']
    
    for table in [table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15]:
        table['Address'] = address
        table['Pincode'] = pincode
    
    # Transform Table 7 to a horizontal format
    table_7_transposed = table_7.set_index(table_7.columns[0]).T.reset_index(drop=True)
    table_7_transposed['Address'] = address
    table_7_transposed['Pincode'] = pincode
    
    # Transform Table 11 to a horizontal format
    table_11_transposed = table_11.set_index(table_11.columns[0]).T.reset_index(drop=True)
    table_11_transposed['Address'] = address
    table_11_transposed['Pincode'] = pincode
    
    # Transform Table 12 to a horizontal format
    table_12_transposed = table_12.set_index(table_12.columns[0]).T.reset_index(drop=True)
    table_12_transposed['Address'] = address
    table_12_transposed['Pincode'] = pincode
    
    return table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_7_transposed, table_11_transposed, table_12_transposed

# Initialize lists to store all scraped data
combined_table_6 = []
combined_table_9 = []
combined_table_4_cleaned = []
combined_table_2 = []
combined_table_3 = []
combined_table_14 = []
combined_table_15 = []
combined_table_7 = []
combined_table_11 = []
combined_table_12 = []

# Iterate through each street URL and scrape data
for street_url in street_urls:
    property_links = fetch_street_page(street_url)
    
    # Scrape and process each property URL
    for url in property_links:
        page_content = fetch_page(url)
        table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_7_transposed, table_11_transposed, table_12_transposed = process_page(page_content)
        
        combined_table_6.append(table_6)
        combined_table_9.append(table_9)
        combined_table_4_cleaned.append(table_4_cleaned)
        combined_table_2.append(table_2)
        combined_table_3.append(table_3)
        combined_table_14.append(table_14)
        combined_table_15.append(table_15)
        combined_table_7.append(table_7_transposed)
        combined_table_11.append(table_11_transposed)
        combined_table_12.append(table_12_transposed)

# Concatenate all the data into final tables
final_table_6 = pd.concat(combined_table_6, ignore_index=True)
final_table_9 = pd.concat(combined_table_9, ignore_index=True)
final_table_4_cleaned = pd.concat(combined_table_4_cleaned, ignore_index=True)
final_table_2 = pd.concat(combined_table_2, ignore_index=True)
final_table_3 = pd.concat(combined_table_3, ignore_index=True)
final_table_14 = pd.concat(combined_table_14, ignore_index=True)
final_table_15 = pd.concat(combined_table_15, ignore_index=True)
final_table_7 = pd.concat(combined_table_7, ignore_index=True)
final_table_11 = pd.concat(combined_table_11, ignore_index=True)
final_table_12 = pd.concat(combined_table_12, ignore_index=True)

# Create a new Excel file with 11 sheets (removed Table 8)
with pd.ExcelWriter('property_details_combined_multiple_streets.xlsx') as writer:
    final_table_6.to_excel(writer, sheet_name='Sales Data', index=False)
    final_table_9.to_excel(writer, sheet_name='Area Details', index=False)
    final_table_4_cleaned.to_excel(writer, sheet_name='Owner Details', index=False)
    final_table_2.to_excel(writer, sheet_name='Appraisal', index=False)
    final_table_3.to_excel(writer, sheet_name='Assessment', index=False)
    final_table_14.to_excel(writer, sheet_name='Past Appraisal', index=False)
    final_table_15.to_excel(writer, sheet_name='Past Assessment', index=False)
    final_table_7.to_excel(writer, sheet_name='Building Details', index=False)
    final_table_11.to_excel(writer, sheet_name='Use and Zone', index=False)
    final_table_12.to_excel(writer, sheet_name='Size and Value', index=False)


# Cell 8
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

# URL for the street
street_url =r"https://gis.vgsi.com/bridgeportct/Streets.aspx?Name=OAKDALE%20ST" #"https://gis.vgsi.com/bridgeportct/Streets.aspx?Name=PACIFIC%20ST"

# Function to fetch the street page and extract all property links
def fetch_street_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()  # Check if the request was successful
    
    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all links to individual property details pages
    property_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'Parcel.aspx?pid=' in href:  # Only interested in links to property pages
            property_links.append('https://gis.vgsi.com/bridgeportct/' + href)
    
    return property_links

# Function to fetch page and parse the HTML
def fetch_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()  # Check if the request was successful

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the entire page content
    page_content = soup.prettify()
    
    return page_content

# Function to process and extract data from the page
def process_page(page_content):
    # Use pandas to read the tables from the HTML
    tables = pd.read_html(page_content)

    # Extract specific tables (Table 6, Table 9, and Table 4)
    table_6 = tables[5]  # Table 6 is at index 5
    table_9 = tables[8]  # Table 9 is at index 8
    table_4 = tables[3]  # Table 4 is at index 3

    # Extract "Owner" from the first row, second column in Table 4
    owner = table_4.iloc[0, 1]

    # Extract "Address" from the third row, second column in Table 4
    address = table_4.iloc[2, 1]

    # Extract the pincode from the address (assuming the pincode is the last part of the address)
    pincode_match = re.search(r'\d{5}(-\d{4})?', address)
    pincode = pincode_match.group(0) if pincode_match else 'Unknown'

    # Filter out "Co-Owner" and "Address" rows, keeping only "Owner"
    table_4_cleaned = table_4[table_4[0] == 'Owner']

    # Add address and pincode columns to each table
    table_6['Address'] = address
    table_6['Pincode'] = pincode

    table_9['Address'] = address
    table_9['Pincode'] = pincode

    # Using .loc to modify the cleaned table, avoiding the SettingWithCopyWarning
    table_4_cleaned.loc[:, 'Address'] = address
    table_4_cleaned.loc[:, 'Pincode'] = pincode

    return table_6, table_9, table_4_cleaned

# Fetch all the property links for the street
property_links = fetch_street_page(street_url)
print(f"Found {len(property_links)} property links.")

# Lists to store the combined tables for all URLs
combined_table_6 = []
combined_table_9 = []
combined_table_4_cleaned = []

# Scrape and process each property URL
for url in property_links:
    print(f"Scraping {url}...")
    page_content = fetch_page(url)
    table_6, table_9, table_4_cleaned = process_page(page_content)
    
    # Append the processed tables to the combined lists
    combined_table_6.append(table_6)
    combined_table_9.append(table_9)
    combined_table_4_cleaned.append(table_4_cleaned)

# Concatenate the data from all URLs for each table
final_table_6 = pd.concat(combined_table_6, ignore_index=True)
final_table_9 = pd.concat(combined_table_9, ignore_index=True)
final_table_4_cleaned = pd.concat(combined_table_4_cleaned, ignore_index=True)

# Create a new Excel file with 3 sheets
with pd.ExcelWriter('property_details_combined.xlsx') as writer:
    final_table_6.to_excel(writer, sheet_name='Sales Data', index=False)
    final_table_9.to_excel(writer, sheet_name='Area Details', index=False)
    final_table_4_cleaned.to_excel(writer, sheet_name='Owner Details', index=False)

print("All tables have been combined and saved to property_details_combined.xlsx.")


# Cell 9
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

# List of URLs to scrape
urls = [
    "https://gis.vgsi.com/bridgeportct/Parcel.aspx?pid=1763",
    "https://gis.vgsi.com/bridgeportct/Parcel.aspx?pid=2326",
    "https://gis.vgsi.com/bridgeportct/Parcel.aspx?pid=1764"
]

# Function to fetch page and parse the HTML
def fetch_page(url):
    # Fetch the page content
    response = requests.get(url, verify=False)
    response.raise_for_status()  # Check if the request was successful

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the entire page content
    page_content = soup.prettify()
    
    return page_content

# Function to process and extract data from the page
def process_page(page_content):
    # Use pandas to read the tables from the HTML
    tables = pd.read_html(page_content)

    # Extract specific tables (Table 6, Table 9, and Table 4)
    table_6 = tables[5]  # Table 6 is at index 5
    table_9 = tables[8]  # Table 9 is at index 8
    table_4 = tables[3]  # Table 4 is at index 3

    # Extract "Owner" from the first row, second column in Table 4
    owner = table_4.iloc[0, 1]

    # Extract "Address" from the third row, second column in Table 4
    address = table_4.iloc[2, 1]

    # Extract the pincode from the address (assuming the pincode is the last part of the address)
    pincode_match = re.search(r'\d{5}(-\d{4})?', address)
    pincode = pincode_match.group(0) if pincode_match else 'Unknown'

    # Filter out "Co-Owner" and "Address" rows, keeping only "Owner"
    table_4_cleaned = table_4[table_4[0] == 'Owner']

    # Add address and pincode columns to each table
    table_6['Address'] = address
    table_6['Pincode'] = pincode

    table_9['Address'] = address
    table_9['Pincode'] = pincode

    # Using .loc to modify the cleaned table, avoiding the SettingWithCopyWarning
    table_4_cleaned.loc[:, 'Address'] = address
    table_4_cleaned.loc[:, 'Pincode'] = pincode

    return table_6, table_9, table_4_cleaned

# List to store the tables from all URLs
all_table_6 = []
all_table_9 = []
all_table_4_cleaned = []

# Scrape and process each URL
for url in urls:
    print(f"Scraping {url}...")
    page_content = fetch_page(url)
    table_6, table_9, table_4_cleaned = process_page(page_content)
    
    # Append the processed tables to the list
    all_table_6.append(table_6)
    all_table_9.append(table_9)
    all_table_4_cleaned.append(table_4_cleaned)

# Create a new Excel file with each table in a separate sheet
with pd.ExcelWriter('property_details_all_urls.xlsx') as writer:
    # Write data from all URLs to the Excel file
    for i, (table_6, table_9, table_4_cleaned) in enumerate(zip(all_table_6, all_table_9, all_table_4_cleaned)):
        table_6.to_excel(writer, sheet_name=f'Sales Data {i+1}', index=False)
        table_9.to_excel(writer, sheet_name=f'Area Details {i+1}', index=False)
        table_4_cleaned.to_excel(writer, sheet_name=f'Owner Details {i+1}', index=False)

print("All tables have been saved to property_details_all_urls.xlsx.")


# Cell 11
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

# Base URL for all streets
base_url = "https://gis.vgsi.com/bridgeportct/Streets.aspx"

# Function to fetch all letter-based street listing pages (A-Z)
def fetch_all_letter_pages():
    response = requests.get(base_url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    letter_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if "Streets.aspx?Letter=" in href:  
            letter_links.append("https://gis.vgsi.com/bridgeportct/" + href)
    
    return letter_links

# Function to fetch all street links from a letter page
def fetch_all_streets(letter_url):
    response = requests.get(letter_url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    street_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if "Streets.aspx?Name=" in href:  
            street_links.append("https://gis.vgsi.com/bridgeportct/" + href)
    
    return street_links

# Function to fetch all property links from a street page
def fetch_street_page(street_url):
    response = requests.get(street_url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    property_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'Parcel.aspx?pid=' in href:
            property_links.append('https://gis.vgsi.com/bridgeportct/' + href)
    
    return property_links

# Function to fetch and parse the property page
def fetch_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    return BeautifulSoup(response.content, 'html.parser').prettify()

# Function to extract property data
def process_page(page_content):
    tables = pd.read_html(page_content)

    table_6 = tables[5] if len(tables) > 5 else pd.DataFrame()
    table_9 = tables[8] if len(tables) > 8 else pd.DataFrame()
    table_4 = tables[3] if len(tables) > 3 else pd.DataFrame()

    if table_4.empty:
        return None, None, None

    owner = table_4.iloc[0, 1] if table_4.shape[0] > 0 else "Unknown"
    address = table_4.iloc[2, 1] if table_4.shape[0] > 2 else "Unknown"

    pincode_match = re.search(r'\d{5}(-\d{4})?', address)
    pincode = pincode_match.group(0) if pincode_match else 'Unknown'

    table_4_cleaned = table_4[table_4[0] == 'Owner']
    
    table_6['Address'], table_6['Pincode'] = address, pincode
    table_9['Address'], table_9['Pincode'] = address, pincode
    table_4_cleaned.loc[:, 'Address'], table_4_cleaned.loc[:, 'Pincode'] = address, pincode

    return table_6, table_9, table_4_cleaned

# Get all letter-based street listing pages
letter_links = fetch_all_letter_pages()
print(f"Found {len(letter_links)} letter pages.")

# Lists to store final combined data
final_table_6, final_table_9, final_table_4_cleaned = [], [], []

# Iterate through each letter page
for letter_url in letter_links:
    print(f"Processing letter page: {letter_url}")
    
    # Get all street links for the current letter
    street_links = fetch_all_streets(letter_url)
    print(f"Found {len(street_links)} streets.")

    # Iterate through each street
    for street_url in street_links:
        print(f"Processing street: {street_url}")
        
        # Get all property links in the street
        property_links = fetch_street_page(street_url)
        print(f"Found {len(property_links)} properties.")

        # Process each property
        for prop_url in property_links:
            print(f"Scraping property: {prop_url}")
            page_content = fetch_page(prop_url)
            table_6, table_9, table_4_cleaned = process_page(page_content)

            if table_6 is not None:
                final_table_6.append(table_6)
            if table_9 is not None:
                final_table_9.append(table_9)
            if table_4_cleaned is not None:
                final_table_4_cleaned.append(table_4_cleaned)

# Combine all data and save to an Excel file
with pd.ExcelWriter('all_properties.xlsx') as writer:
    if final_table_6:
        pd.concat(final_table_6, ignore_index=True).to_excel(writer, sheet_name='Sales Data', index=False)
    if final_table_9:
        pd.concat(final_table_9, ignore_index=True).to_excel(writer, sheet_name='Area Details', index=False)
    if final_table_4_cleaned:
        pd.concat(final_table_4_cleaned, ignore_index=True).to_excel(writer, sheet_name='Owner Details', index=False)

print("Scraping completed. Data saved to all_properties.xlsx.")


# Cell 13
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests

# URL for the street
street_url = r"https://gis.vgsi.com/bridgeportct/Streets.aspx?Name=OAKDALE%20ST"

# Function to fetch the street page and extract all property links
def fetch_street_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    property_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Parcel.aspx?pid=' in link['href']
    ]
    
    return property_links

# Function to fetch page and parse the HTML
def fetch_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser').prettify()

# Function to process and extract data from the page
def process_page(page_content):
    tables = pd.read_html(page_content)
    
    table_6 = tables[5]
    table_9 = tables[8]
    table_4 = tables[3]
    table_2 = tables[1]
    table_3 = tables[2]
    table_14 = tables[13]
    table_15 = tables[14]
    table_7 = tables[6]
    table_8 = tables[7]
    table_11 = tables[10]
    table_12 = tables[11]
    
    owner = table_4.iloc[0, 1]
    address = table_4.iloc[2, 1]
    pincode_match = re.search(r'\d{5}(-\d{4})?', address)
    pincode = pincode_match.group(0) if pincode_match else 'Unknown'
    
    table_4_cleaned = table_4[table_4[0] == 'Owner']
    
    for table in [table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15]:
        table['Address'] = address
        table['Pincode'] = pincode
    
    # Transform Table 7 to a horizontal format
    table_7_transposed = table_7.set_index(table_7.columns[0]).T.reset_index(drop=True)
    table_7_transposed['Address'] = address
    table_7_transposed['Pincode'] = pincode
    
    # Transform Table 8 to a horizontal format
    table_8_transposed = table_8.set_index(table_8.columns[0]).T.reset_index(drop=True)
    table_8_transposed['Address'] = address
    table_8_transposed['Pincode'] = pincode
    
    # Transform Table 11 to a horizontal format
    table_11_transposed = table_11.set_index(table_11.columns[0]).T.reset_index(drop=True)
    table_11_transposed['Address'] = address
    table_11_transposed['Pincode'] = pincode
    
    # Transform Table 12 to a horizontal format
    table_12_transposed = table_12.set_index(table_12.columns[0]).T.reset_index(drop=True)
    table_12_transposed['Address'] = address
    table_12_transposed['Pincode'] = pincode
    
    return table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_7_transposed, table_8_transposed, table_11_transposed, table_12_transposed

# Fetch all property links
property_links = fetch_street_page(street_url)

combined_table_6 = []
combined_table_9 = []
combined_table_4_cleaned = []
combined_table_2 = []
combined_table_3 = []
combined_table_14 = []
combined_table_15 = []
combined_table_7 = []
combined_table_8 = []
combined_table_11 = []
combined_table_12 = []

# Scrape and process each property URL
for url in property_links:
    page_content = fetch_page(url)
    table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_7_transposed, table_8_transposed, table_11_transposed, table_12_transposed = process_page(page_content)
    
    combined_table_6.append(table_6)
    combined_table_9.append(table_9)
    combined_table_4_cleaned.append(table_4_cleaned)
    combined_table_2.append(table_2)
    combined_table_3.append(table_3)
    combined_table_14.append(table_14)
    combined_table_15.append(table_15)
    combined_table_7.append(table_7_transposed)
    combined_table_8.append(table_8_transposed)
    combined_table_11.append(table_11_transposed)
    combined_table_12.append(table_12_transposed)

final_table_6 = pd.concat(combined_table_6, ignore_index=True)
final_table_9 = pd.concat(combined_table_9, ignore_index=True)
final_table_4_cleaned = pd.concat(combined_table_4_cleaned, ignore_index=True)
final_table_2 = pd.concat(combined_table_2, ignore_index=True)
final_table_3 = pd.concat(combined_table_3, ignore_index=True)
final_table_14 = pd.concat(combined_table_14, ignore_index=True)
final_table_15 = pd.concat(combined_table_15, ignore_index=True)
final_table_7 = pd.concat(combined_table_7, ignore_index=True)
final_table_8 = pd.concat(combined_table_8, ignore_index=True)
final_table_11 = pd.concat(combined_table_11, ignore_index=True)
final_table_12 = pd.concat(combined_table_12, ignore_index=True)

# Create a new Excel file with 12 sheets
with pd.ExcelWriter('property_details_combined.xlsx') as writer:
    final_table_6.to_excel(writer, sheet_name='Sales Data', index=False)
    final_table_9.to_excel(writer, sheet_name='Area Details', index=False)
    final_table_4_cleaned.to_excel(writer, sheet_name='Owner Details', index=False)
    final_table_2.to_excel(writer, sheet_name='Appraisal', index=False)
    final_table_3.to_excel(writer, sheet_name='Assessment', index=False)
    final_table_14.to_excel(writer, sheet_name='Past Appraisal', index=False)
    final_table_15.to_excel(writer, sheet_name='Past Assessment', index=False)
    final_table_7.to_excel(writer, sheet_name='Building Details', index=False)
    final_table_8.to_excel(writer, sheet_name='Property Features', index=False)
    final_table_11.to_excel(writer, sheet_name='Use and Zone', index=False)
    final_table_12.to_excel(writer, sheet_name='Size and Value', index=False)


# Cell 15
# working on this to scrap the whole database of bridgeport
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests

# Function to fetch the main street page and extract all the street URLs
def fetch_main_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    street_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Streets.aspx?Name=' in link['href']
    ]
    
    return street_links

# Function to fetch the street page and extract all property links
def fetch_street_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    property_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Parcel.aspx?pid=' in link['href']
    ]
    
    return property_links

# Function to fetch page and parse the HTML
def fetch_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser').prettify()

# Function to process and extract data from the page
def process_page(page_content):
    tables = pd.read_html(page_content)
    
    table_6 = tables[5]
    table_9 = tables[8]
    table_4 = tables[3]
    table_2 = tables[1]
    table_3 = tables[2]
    table_14 = tables[13]
    table_15 = tables[14]
    table_7 = tables[6]
    table_11 = tables[10]
    table_12 = tables[11]
    
    owner = table_4.iloc[0, 1]
    address = table_4.iloc[2, 1]
    pincode_match = re.search(r'\d{5}(-\d{4})?', address)
    pincode = pincode_match.group(0) if pincode_match else 'Unknown'
    
    table_4_cleaned = table_4[table_4[0] == 'Owner']
    
    for table in [table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15]:
        table['Address'] = address
        table['Pincode'] = pincode
    
    # Transform Table 7 to a horizontal format
    table_7_transposed = table_7.set_index(table_7.columns[0]).T.reset_index(drop=True)
    table_7_transposed['Address'] = address
    table_7_transposed['Pincode'] = pincode
    
    # Transform Table 11 to a horizontal format
    table_11_transposed = table_11.set_index(table_11.columns[0]).T.reset_index(drop=True)
    table_11_transposed['Address'] = address
    table_11_transposed['Pincode'] = pincode
    
    # Transform Table 12 to a horizontal format
    table_12_transposed = table_12.set_index(table_12.columns[0]).T.reset_index(drop=True)
    table_12_transposed['Address'] = address
    table_12_transposed['Pincode'] = pincode
    
    return table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_7_transposed, table_11_transposed, table_12_transposed

# Initialize lists to store all scraped data
combined_table_6 = []
combined_table_9 = []
combined_table_4_cleaned = []
combined_table_2 = []
combined_table_3 = []
combined_table_14 = []
combined_table_15 = []
combined_table_7 = []
combined_table_11 = []
combined_table_12 = []

# Main URL for scraping all street links
main_url = "https://gis.vgsi.com/bridgeportct/Streets.aspx"
street_links = fetch_main_page(main_url)

# Iterate through each street URL and scrape data
for street_url in street_links:
    print(f"Processing {street_url}")
    
    # Fetch all property links from the street page
    property_links = fetch_street_page(street_url)
    
    # Scrape and process each property URL
    for url in property_links:
        page_content = fetch_page(url)
        table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_7_transposed, table_11_transposed, table_12_transposed = process_page(page_content)
        
        combined_table_6.append(table_6)
        combined_table_9.append(table_9)
        combined_table_4_cleaned.append(table_4_cleaned)
        combined_table_2.append(table_2)
        combined_table_3.append(table_3)
        combined_table_14.append(table_14)
        combined_table_15.append(table_15)
        combined_table_7.append(table_7_transposed)
        combined_table_11.append(table_11_transposed)
        combined_table_12.append(table_12_transposed)

# Concatenate all the data into final tables
final_table_6 = pd.concat(combined_table_6, ignore_index=True)
final_table_9 = pd.concat(combined_table_9, ignore_index=True)
final_table_4_cleaned = pd.concat(combined_table_4_cleaned, ignore_index=True)
final_table_2 = pd.concat(combined_table_2, ignore_index=True)
final_table_3 = pd.concat(combined_table_3, ignore_index=True)
final_table_14 = pd.concat(combined_table_14, ignore_index=True)
final_table_15 = pd.concat(combined_table_15, ignore_index=True)
final_table_7 = pd.concat(combined_table_7, ignore_index=True)
final_table_11 = pd.concat(combined_table_11, ignore_index=True)
final_table_12 = pd.concat(combined_table_12, ignore_index=True)

# Create a new Excel file with 11 sheets (removed Table 8)
with pd.ExcelWriter('property_details_combined_all_streets_full_website.xlsx') as writer:
    final_table_6.to_excel(writer, sheet_name='Sales Data', index=False)
    final_table_9.to_excel(writer, sheet_name='Area Details', index=False)
    final_table_4_cleaned.to_excel(writer, sheet_name='Owner Details', index=False)
    final_table_2.to_excel(writer, sheet_name='Appraisal', index=False)
    final_table_3.to_excel(writer, sheet_name='Assessment', index=False)
    final_table_14.to_excel(writer, sheet_name='Past Appraisal', index=False)
    final_table_15.to_excel(writer, sheet_name='Past Assessment', index=False)
    final_table_7.to_excel(writer, sheet_name='Building Details', index=False)
    final_table_11.to_excel(writer, sheet_name='Use and Zone', index=False)
    final_table_12.to_excel(writer, sheet_name='Size and Value', index=False)


# Cell 16
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests

def fetch_main_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    street_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Streets.aspx?Name=' in link['href']
    ]
    
    return street_links

def fetch_street_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    property_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Parcel.aspx?pid=' in link['href']
    ]
    
    return property_links

def fetch_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser').prettify()

def process_page(page_content):
    tables = pd.read_html(page_content)
    
    table_6 = tables[5] table_9 = tables[8] table_4 = tables[3]table_2 = tables[1]table_3 = tables[2]
    table_14 = tables[13]
    table_15 = tables[14]
    table_7 = tables[6]
    table_8 = tables[7] 
    table_11 = tables[10]
    table_12 = tables[11]
    
    owner = table_4.iloc[0, 1]
    address = table_4.iloc[2, 1]
    pincode_match = re.search(r'\d{5}(-\d{4})?', address)
    pincode = pincode_match.group(0) if pincode_match else 'Unknown'
    
    table_4_cleaned = table_4[table_4[0] == 'Owner']
    
    for table in [table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_8]:
        table['Address'] = address
        table['Pincode'] = pincode
    
    table_7_transposed = table_7.set_index(table_7.columns[0]).T.reset_index(drop=True)
    table_7_transposed['Address'] = address
    table_7_transposed['Pincode'] = pincode
    
    table_11_transposed = table_11.set_index(table_11.columns[0]).T.reset_index(drop=True)
    table_11_transposed['Address'] = address
    table_11_transposed['Pincode'] = pincode
    
    table_12_transposed = table_12.set_index(table_12.columns[0]).T.reset_index(drop=True)
    table_12_transposed['Address'] = address
    table_12_transposed['Pincode'] = pincode
    
    return table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_7_transposed, table_8, table_11_transposed, table_12_transposed

combined_data = {i: [] for i in range(11)}
urls = ["https://gis.vgsi.com/bridgeportct/Streets.aspx?Letter=I", "https://gis.vgsi.com/bridgeportct/Streets.aspx?Letter=K"]

for main_url in urls:
    street_links = fetch_main_page(main_url)
    
    for street_url in street_links:
        print(f"Processing {street_url}")
        property_links = fetch_street_page(street_url)
        
        for url in property_links:
            try:
                page_content = fetch_page(url)
                extracted_data = process_page(page_content)
                
                for idx, table in enumerate(extracted_data):
                    combined_data[idx].append(table)
            except Exception as e:
                print(f"Error processing {url}: {e}")

final_dataframes = {idx: pd.concat(tables, ignore_index=True) for idx, tables in combined_data.items() if tables}

with pd.ExcelWriter('property_details_I_K.xlsx') as writer:
    sheet_names = ['Sales Data', 'Area Details', 'Owner Details', 'Appraisal', 'Assessment', 'Past Appraisal', 'Past Assessment', 'Building Details', 'Table 8', 'Use and Zone', 'Size and Value']
    
    for idx, df in final_dataframes.items():
        df.to_excel(writer, sheet_name=sheet_names[idx], index=False)


# Cell 17
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests

def fetch_main_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    street_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Streets.aspx?Name=' in link['href']
    ]
    
    return street_links

def fetch_street_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    property_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Parcel.aspx?pid=' in link['href']
    ]
    
    return property_links

def fetch_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser').prettify()

def process_page(page_content):
    tables = pd.read_html(page_content)
    
    table_6 = tables[5]
    table_9 = tables[8]
    table_4 = tables[3]
    table_2 = tables[1]
    table_3 = tables[2]
    table_14 = tables[13]
    table_15 = tables[14]
    table_7 = tables[6]
    table_8 = tables[7] 
    table_11 = tables[10]
    table_12 = tables[11]
    
    owner = table_4.iloc[0, 1]
    address = table_4.iloc[2, 1]
    pincode_match = re.search(r'\d{5}(-\d{4})?', address)
    pincode = pincode_match.group(0) if pincode_match else 'Unknown'
    
    table_4_cleaned = table_4[table_4[0] == 'Owner']
    
    for table in [table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_8]:
        table['Address'] = address
        table['Pincode'] = pincode
    
    table_7_transposed = table_7.set_index(table_7.columns[0]).T.reset_index(drop=True)
    table_7_transposed['Address'] = address
    table_7_transposed['Pincode'] = pincode
    
    table_11_transposed = table_11.set_index(table_11.columns[0]).T.reset_index(drop=True)
    table_11_transposed['Address'] = address
    table_11_transposed['Pincode'] = pincode
    
    table_12_transposed = table_12.set_index(table_12.columns[0]).T.reset_index(drop=True)
    table_12_transposed['Address'] = address
    table_12_transposed['Pincode'] = pincode
    
    return table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_7_transposed, table_8, table_11_transposed, table_12_transposed

combined_data = {i: [] for i in range(11)}
urls = [
    "https://gis.vgsi.com/bridgeportct/Streets.aspx?Letter=A",  # New URL for Q Street
    "https://gis.vgsi.com/bridgeportct/Streets.aspx?Letter=B"   # New URL for U Street
]

# Scrape data for Q and U streets
for main_url in urls:
    street_links = fetch_main_page(main_url)
    
    for street_url in street_links:
        print(f"Processing {street_url}")
        property_links = fetch_street_page(street_url)
        
        for url in property_links:
            try:
                page_content = fetch_page(url)
                extracted_data = process_page(page_content)
                
                for idx, table in enumerate(extracted_data):
                    combined_data[idx].append(table)
            except Exception as e:
                print(f"Error processing {url}: {e}")

final_dataframes = {idx: pd.concat(tables, ignore_index=True) for idx, tables in combined_data.items() if tables}

# Read the existing Excel file and append the new data
with pd.ExcelWriter('property_details_I_K.xlsx', mode='a', if_sheet_exists='overlay') as writer:  # Open in append mode
    sheet_names = ['Sales Data', 'Area Details', 'Owner Details', 'Appraisal', 'Assessment', 'Past Appraisal', 'Past Assessment', 'Building Details', 'Table 8', 'Use and Zone', 'Size and Value']
    
    for idx, df in final_dataframes.items():
        df.to_excel(writer, sheet_name=sheet_names[idx], index=False)


# Cell 19
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Cell 20
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor
def fetch_main_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    street_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Streets.aspx?Name=' in link['href'] ]
    return street_links
def fetch_street_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    property_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Parcel.aspx?pid=' in link['href'] ]
    return property_links
def fetch_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser').prettify()
def process_page(page_content):
    tables = pd.read_html(page_content) table_6 = tables[5] table_9 = tables[8] table_4 = tables[3]table_2 = tables[1]table_3 = tables[2] table_14 = tables[13]
    table_15 = tables[14] table_7 = tables[6] table_8 = tables[7] table_11 = tables[10] table_12 = tables[11]
    address = table_4.iloc[2, 1]
    pincode_match = re.search(r'\d{5}(-\d{4})?', address)
    pincode = pincode_match.group(0) if pincode_match else 'Unknown'
    table_4_cleaned = table_4[table_4[0] == 'Owner']
    for table in [table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_8]:
        table['Address'] = address
        table['Pincode'] = pincode
    table_7_transposed = table_7.set_index(table_7.columns[0]).T.reset_index(drop=True)
    table_7_transposed['Address'] = address
    table_7_transposed['Pincode'] = pincode
    table_11_transposed = table_11.set_index(table_11.columns[0]).T.reset_index(drop=True)
    table_11_transposed['Address'] = address
    table_11_transposed['Pincode'] = pincode
    table_12_transposed = table_12.set_index(table_12.columns[0]).T.reset_index(drop=True)
    table_12_transposed['Address'] = address
    table_12_transposed['Pincode'] = pincode
    return table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_7_transposed, table_8, table_11_transposed, table_12_transposed
def process_property(url):
    try:
        page_content = fetch_page(url)
        return process_page(page_content)
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None
combined_data = {i: [] for i in range(11)}
urls = [ "https://gis.vgsi.com/bridgeportct/Streets.aspx?Letter=I","https://gis.vgsi.com/bridgeportct/Streets.aspx?Letter=J"]
for main_url in urls:
    street_links = fetch_main_page(main_url)
    for street_url in street_links:
    property_links = fetch_street_page(street_url)
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = list(executor.map(process_property, property_links))
             for extracted_data in results:
            if extracted_data:
                for idx, table in enumerate(extracted_data):
                    combined_data[idx].append(table)
final_dataframes = {idx: pd.concat(tables, ignore_index=True) for idx, tables in combined_data.items() if tables}
with pd.ExcelWriter('hproperty_details.xlsx', mode='w') as writer:
    sheet_names = ['Sales Data', 'Area Details', 'Owner Details', 'Appraisal', 'Assessment', 'Past Appraisal', 'Past Assessment', 'Building Details', 'Table 8', 'Use and Zone', 'Size and Value']
     for idx, df in final_dataframes.items():
        df.to_excel(writer, sheet_name=sheet_names[idx], index=False)


# Cell 21
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor

def fetch_main_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    street_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Streets.aspx?Name=' in link['href']
    ]
    
    return street_links

def fetch_street_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    property_links = [
        'https://gis.vgsi.com/bridgeportct/' + link['href']
        for link in soup.find_all('a', href=True) if 'Parcel.aspx?pid=' in link['href']
    ]
    
    return property_links

def fetch_page(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser').prettify()

def process_page(page_content):
    tables = pd.read_html(page_content)
    
    table_6 = tables[5]
    table_9 = tables[8]
    table_4 = tables[3]
    table_2 = tables[1]
    table_3 = tables[2]
    table_14 = tables[13]
    table_15 = tables[14]
    table_7 = tables[6]
    table_8 = tables[7] 
    table_11 = tables[10]
    table_12 = tables[11]
    
    address = table_4.iloc[2, 1] if len(table_4) > 2 else 'Unknown'
    pincode_match = re.search(r'\d{5}(-\d{4})?', address)
    pincode = pincode_match.group(0) if pincode_match else 'Unknown'
    
    table_4_cleaned = table_4[table_4[0] == 'Owner']
    
    for table in [table_6, table_9, table_4_cleaned, table_2, table_3, table_14, table_15, table_8]:
        if not table.empty:
            table.loc[:, 'Address'] = address
            table.loc[:, 'Pincode'] = pincode
    
    def transpose_table(table):
        if not table.empty:
            table_transposed = table.set_index(table.columns[0]).T.reset_index(drop=True)
            table_transposed.loc[:, 'Address'] = address
            table_transposed.loc[:, 'Pincode'] = pincode
            return table_transposed
        return pd.DataFrame()
    
    return (
        table_6, table_9, table_4_cleaned, table_2, table_3, table_14, 
        table_15, transpose_table(table_7), table_8, transpose_table(table_11), transpose_table(table_12)
    )

def process_property(url):
    try:
        page_content = fetch_page(url)
        return process_page(page_content)
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

combined_data = {i: [] for i in range(11)}
urls = [
    "https://gis.vgsi.com/bridgeportct/Streets.aspx?Letter=T",
    "https://gis.vgsi.com/bridgeportct/Streets.aspx?Letter=U",
    "https://gis.vgsi.com/bridgeportct/Streets.aspx?Letter=V",
    "https://gis.vgsi.com/bridgeportct/Streets.aspx?Letter=Y"
]

for main_url in urls:
    street_links = fetch_main_page(main_url)
    
    for street_url in street_links:
        property_links = fetch_street_page(street_url)
        
        with ThreadPoolExecutor(max_workers=15) as executor:
            results = list(executor.map(process_property, property_links))
            
        for extracted_data in results:
            if extracted_data:
                for idx, table in enumerate(extracted_data):
                    if table is not None and not table.empty:
                        combined_data[idx].append(table.reset_index(drop=True))

final_dataframes = {idx: pd.concat(tables, ignore_index=True) for idx, tables in combined_data.items() if tables}

with pd.ExcelWriter('TUVYproperty_details.xlsx', mode='w') as writer:
    sheet_names = ['Sales Data', 'Area Details', 'Owner Details', 'Appraisal', 'Assessment', 'Past Appraisal', 'Past Assessment', 'Building Details', 'Table 8', 'Use and Zone', 'Size and Value']
    
    for idx, df in final_dataframes.items():
        df.to_excel(writer, sheet_name=sheet_names[idx], index=False)
