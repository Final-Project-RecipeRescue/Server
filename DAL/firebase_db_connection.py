import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import db
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
        #cred_obj = firebase_admin.credentials.Certificate('../config/fb_credentials.json')
        current_directory = os.path.dirname(os.path.abspath(__file__))
        credentials_path = os.path.join(current_directory, '..', 'config', 'fb_credentials.json')
        cred_obj = firebase_admin.credentials.Certificate(credentials_path)
        default_app = firebase_admin.initialize_app(cred_obj, {
            'databaseURL': databaseURL
        })
        self.ref = db.reference("/")

    #TODO: write to database, read from database, delete from database
    def write_firebase_data(self, reference: str, data: dict) -> None:
        self.ref.child(reference).set(data)
    def delete_firebase_data(self, reference: str) -> None:
        self.ref.child(reference).delete()
    def get_firebase_data(self, reference: str) -> object:
        return self.ref.child(reference).get()
    def update_firebase_data(self, reference: str, data: dict) -> None:
        self.ref.child(reference).update(data)


'''if __name__ == "__main__":
    inst = FirebaseDbConnection.get_instance()
    household_id = "1223"
    x = {
        "aisle": "Milk, Eggs, Other Dairy",
        "amount": 1.0,
        "consitency": "solid",
        "id": 1001,
        "image": "butter-sliced.jpg",
        "measures": {
            "metric": {
                "amount": 1.0,
                "unitLong": "Tbsp",
                "unitShort": "Tbsp"
            },
            "us": {
                "amount": 1.0,
                "unitLong": "Tbsp",
                "unitShort": "Tbsp"
            }
        },
        "meta": [],
        "name": "butter",
        "original": "1 tbsp butter",
        "originalName": "butter",
        "unit": "tbsp"
    }
    y = IngredientEntitySpoonacular(x)
    inst.write_firebase_data((f'households/{household_id}/ingredients/{y.id}'),y.__dict__)'''