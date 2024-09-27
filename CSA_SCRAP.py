# This code is not working anymore. We need to change it
import requests 
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession

#def get_url(link):
#    url = link
#    response = requests.get(url)
#    html = response.text
#    soup = BeautifulSoup(html,'html.parser')
#    adress = soup.find_all('p')[0].text.strip()
#    return adress
#print(get_url('https://www.osc.ca/en/investors/warnings/blackbear-ecapital'))

session = HTMLSession()

def get_url(link):
    try:
        # Render the page
        response = session.get(link)
        response.html.render()
        
        # The rest of the code is similar, using response.html instead of response.text
        soup = BeautifulSoup(response.html.html, 'html.parser')
        th_tag = soup.find('th', string=lambda text: "Note" in text)
        if th_tag:
            td_tag = th_tag.find_next('td')
            if td_tag:
                note_text = td_tag.text.strip()
                return note_text
            else:
                return "TD element not found after TH"
        else:
            return "TH element with 'Note' not found"
    except Exception as e:
        return f"An error occurred: {e}"

# Function to process a list of URLs and save the results in a DataFrame
def process_urls_from_csv(input_csv, output_csv):
    # Read the CSV file into a DataFrame
    input_df = pd.read_csv(input_csv)

    # Assuming the column containing URLs is named 'URL'
    data = []
    for url in input_df['URL']:
        address = get_url(url)
        data.append({'URL': url, 'Address': address})
    
    # Creating a DataFrame
    output_df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    output_df.to_csv(output_csv, index=False)

    return output_df

# Example usage
input_csv = 'CSA_input.csv'  
output_csv = 'CSA_output.csv' 

result_df = process_urls_from_csv(input_csv, output_csv)