from db.cosmos_db_handler import CosmosDBHandler
from typing import Optional

class CosmosWrapper():
    def __init__(self, auth) -> None:
        self.auth = auth
        self.client = CosmosDBHandler(self.auth)
        self.database, self.container = self.client.session()

    def get_request_charge(self):
        return self.client.get_request_charge(self.container)
    
    def create_item(self, body):
        response = self.client.create_item(self.container, body)
        
        charge = self.get_request_charge()

        return response, charge
    
    def create_item_batches(self, items):
        len_items = len(items)
        
        counter = 0

        for item in items:
            counter += 1
            response = self.client.create_item(self.container, item)

            print(f"Progress: {counter}/{len_items}")
        
        charge = self.get_request_charge()

        return charge
    
    def read_item(self, item_id, partition_key):
        response = self.client.read_item(self.container, item_id, partition_key)

        charge = self.get_request_charge()

        return response, charge
    
    def read_items(self, limit: Optional[int] = None):
        response = self.client.read_items(self.container, max_count=limit)

        return response
    


    