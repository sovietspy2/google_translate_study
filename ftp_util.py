import os
from ftplib import FTP
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

def upload_html():
    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")
    local_html_file = os.getenv("LOCAL_HTML_FILE")
    remote_directory = os.getenv("REMOTE_DIRECTORY")

    logging.info(f"uploading file to {ftp_host}")

    ftp = FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)

    ftp.cwd(remote_directory)

    try:
        with open(local_html_file, 'rb') as file:
            # Upload the file to the remote server
            ftp.storbinary('STOR ' + os.path.basename(local_html_file), file)
    except Exception as e:
        logging.error(e)

    ftp.quit()
    logging.info(f"uploading complete, check your website")