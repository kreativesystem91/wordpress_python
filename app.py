from flask import Flask, render_template, request
import os
import urllib.request
import tarfile
import requests
import random
import string

app = Flask(__name__)

def generate_random_word(length=10):
    # Generate a random word using lowercase letters
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def get_latest_wordpress_version():
    # Fetch the latest WordPress version number from the WordPress API
    response = requests.get('https://api.wordpress.org/core/version-check/1.7/')
    if response.status_code == 200:
        return response.json()['offers'][0]['version']
    else:
        print("Failed to fetch the latest WordPress version.")
        exit()

def download_wordpress(wp_download_url, wp_file_path):
    if os.path.exists(wp_file_path):
        print("WordPress archive already exists. Skipping download.")
    else:
        print('Downloading WordPress...')
        try:
            urllib.request.urlretrieve(wp_download_url, wp_file_path)
            print('Downloaded WordPress.')
        except Exception as e:
            print(f'Failed to download WordPress: {e}')
            exit()

def extract_wordpress(archive_path, extract_dir):
    print('Extracting WordPress...')
    try:
        with tarfile.open(archive_path, 'r:gz') as tfile:
            tfile.extractall(extract_dir)
        print('Extracted WordPress.')
    except tarfile.TarError as e:
        print(f'Failed to extract WordPress: {e}')
        exit()
              
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup', methods=['POST'])
def setup_wordpress():
    business_description = request.form['business_description'].strip().lower()
    website_code = generate_random_word()

    unique_dir = os.path.join('websites', f"{business_description}-{website_code}")
    os.makedirs(unique_dir)

    latest_wp_version = get_latest_wordpress_version()
    wordpress_dir = os.path.join('wordpress', latest_wp_version)
    websites_dir = 'websites'

    if not os.path.exists(wordpress_dir):
        os.makedirs(wordpress_dir)

    wp_dl = f'https://wordpress.org/wordpress-{latest_wp_version}.tar.gz'
    wp_file = os.path.join(wordpress_dir, f'wordpress-{latest_wp_version}.tar.gz')
    download_wordpress(wp_dl, wp_file)
    extract_wordpress(wp_file, unique_dir)

    return f'WordPress setup completed in {unique_dir}.'

if __name__ == "__main__":
    app.run(debug=True)
