from config.settings.base import BASE_DIR
import os


# File existence check is done in the wsgi.py file
KEY_FILE_PATHS = {
    'DOCUSIGN_PRIVATE_KEY_DEV': os.path.join(BASE_DIR, 'keys', "docusign_private_key_demo.txt"),
    'DOCUSIGN_PRIVATE_KEY_PROD': os.path.join(BASE_DIR, 'keys', "docusign_private_key_prod.txt"),
}
