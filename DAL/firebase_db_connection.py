import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import db, storage

load_dotenv()
import logging

logger = logging.getLogger("my_logger")


class FirebaseDbConnection:
    _instance = None

    @staticmethod
    def get_instance():
        if FirebaseDbConnection._instance is None:
            FirebaseDbConnection._instance = FirebaseDbConnection()
        return FirebaseDbConnection._instance

    def __init__(self):
        if FirebaseDbConnection._instance is not None:
            raise Exception("Singleton instance firebase already exists.")
        databaseURL = os.getenv("databaseURL")
        storageURL = os.getenv("storageURL")
        # cred_obj = firebase_admin.credentials.Certificate('../config/fb_credentials.json')
        current_directory = os.path.dirname(os.path.abspath(__file__))
        credentials_path = os.path.join(current_directory, '..', 'config', 'fb_credentials.json')
        try:
            cred_obj = firebase_admin.credentials.Certificate(credentials_path)
            default_app = firebase_admin.initialize_app(cred_obj, {
                'databaseURL': databaseURL,
                'storageBucket': storageURL
            })
            self.ref = db.reference("/")
            self.bucket = storage.bucket()
            logger.info("Firebase connection initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase connection: {e}")
            raise e

    def write_firebase_data(self, reference: str, data: dict) -> None:
        try:
            self.ref.child(reference).set(data)
            logger.info(f"Data written to Firebase at reference '{reference}' successfully.")
        except Exception as e:
            logger.error(f"Failed to write data to Firebase at reference '{reference}': {e}")

    def delete_firebase_data(self, reference: str) -> None:
        try:
            self.ref.child(reference).delete()
            logger.info(f"Data deleted from Firebase at reference '{reference}' successfully.")
        except Exception as e:
            logger.error(f"Failed to delete data from Firebase at reference '{reference}': {e}")
            raise e

    def get_firebase_data(self, reference: str) -> object:
        try:
            data = self.ref.child(reference).get()
            logger.info(f"Data retrieved from Firebase at reference '{reference}' successfully.")
            return data
        except Exception as e:
            logger.error(f"Failed to retrieve data from Firebase at reference '{reference}': {e}")
            raise e

    def update_firebase_data(self, reference: str, data: dict) -> None:
        try:
            self.ref.child(reference).update(data)
            logger.info(f"Data updated in Firebase at reference '{reference}' successfully.")
        except Exception as e:
            logger.error(f"Failed to update data in Firebase at reference '{reference}': {e}")
            raise e

    def upload_file(self, local_file_path: str, storage_path: str) -> None:
        try:
            blob = self.bucket.blob(f"{storage_path}/{os.path.basename(local_file_path)}")
            blob.upload_from_filename(local_file_path)
            logger.info(f"File '{local_file_path}' uploaded to Firebase storage at '{storage_path}' successfully.")
        except Exception as e:
            logger.error(f"Failed to upload file '{local_file_path}' to Firebase storage at '{storage_path}': {e}")
            raise e

    def download_file(self, local_file_path: str, storage_path: str) -> None:
        try:
            blob = self.bucket.blob(f"{storage_path}")
            blob.download_to_filename(local_file_path)
            logger.info(f"File downloaded from Firebase storage '{storage_path}' to '{local_file_path}' successfully.")
        except Exception as e:
            logger.error(f"Failed to download file from Firebase storage '{storage_path}' to '{local_file_path}': {e}")
            raise e