import requests
from bs4 import BeautifulSoup

def extract_direct_links(input_file, output_file):
    with open(input_file, 'r') as f:
        links = f.readlines()

    links = [link.strip() for link in links]

    direct_links = []
    for link in links:
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')
            download_button = soup.find(id='downloadButton')

            if download_button and 'href' in download_button.attrs:
                direct_links.append(download_button['href'])
                print(f"Extracted direct link for {link}")

        except Exception as e:
            print(f"Failed to extract direct link for {link}: {e}")

    with open(output_file, 'w') as f:
        for direct_link in direct_links:
            f.write(f"{direct_link}\n")

    print("Direct links extraction completed. Check the output file.")

# Replace 'links.txt' with your input file and 'direct_links.txt' with the desired output file
extract_direct_links('links.txt', 'direct_links.txt')
