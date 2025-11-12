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
    "https://gis.vgsi.com/bridgeportct/Streets.aspx?Letter=T"
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
