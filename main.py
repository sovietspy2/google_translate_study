import logging
logging.basicConfig(level=logging.INFO)
from google_util import download_process
from html_util import html_process
from ftp_util import upload_html

def main():
    download_process()
    html_process()
    upload_html()

if __name__ == '__main__':
    main()