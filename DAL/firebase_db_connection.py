import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import db, storage

load_dotenv()


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
        cred_obj = firebase_admin.credentials.Certificate(credentials_path)
        default_app = firebase_admin.initialize_app(cred_obj, {
            'databaseURL': databaseURL,
            'storageBucket': storageURL
        })
        self.ref = db.reference("/")
        self.bucket = storage.bucket()

    def write_firebase_data(self, reference: str, data: dict) -> None:
        self.ref.child(reference).set(data)

    def delete_firebase_data(self, reference: str) -> None:
        self.ref.child(reference).delete()

    def get_firebase_data(self, reference: str) -> object:
        return self.ref.child(reference).get()

    def update_firebase_data(self, reference: str, data: dict) -> None:
        self.ref.child(reference).update(data)

    def upload_file(self, local_file_path: str, storage_path: str) -> None:
        blob = self.bucket.blob(f"{storage_path}/{local_file_path}")
        blob.upload_from_filename(local_file_path)

    def download_file(self, local_file_path: str, storage_path: str) -> None:
        blob = self.bucket.blob(f"{storage_path}")
        blob.download_to_filename(local_file_path)
