from config.settings.base import BASE_DIR
import os


KEY_FILE_PATHS = {
    'DOCUSIGN_PRIVATE_KEY': os.path.join(BASE_DIR, 'keys', "docusign_private_key_demo.txt"),
}
