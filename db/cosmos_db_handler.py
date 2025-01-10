from azure.cosmos import cosmos_client, exceptions
from azure.cosmos.cosmos_client import CosmosClient
from dotenv import dotenv_values
from typing import Optional

class CosmosDBHandler():
    """
        Either configure a .env or pass auth with proper dictionary values \n
        auth: auth =  {
            "ACCOUNT_HOST": "{ACCOUNT_HOST}",
            "ACCOUNT_KEY": "{ACCOUNT_KEY}",
            "COSMOS_DATABASE": "{COSMOS_DATABASE}",
            "COSMOS_CONTAINER": "{COSMOS_CONTAINER}"
        }
    """
    def __init__(self, auth: dict = None) -> None:
        auth = auth or {}
        config = dotenv_values(".env")

        def get_connection_value(key):
            return auth.get(key) or config.get(key)

        self.ACCOUNT_HOST = get_connection_value("ACCOUNT_HOST") 
        self.ACCOUNT_KEY = get_connection_value("ACCOUNT_KEY") 
        self.COSMOS_DATABASE = get_connection_value("COSMOS_DATABASE") 
        self.COSMOS_CONTAINER = get_connection_value("COSMOS_CONTAINER")

        missing_connection_value = [
            key for key, value in {
                "ACCOUNT_HOST": self.ACCOUNT_HOST,
                "ACCOUNT_KEY": self.ACCOUNT_KEY,
                "COSMOS_DATABASE": self.COSMOS_DATABASE,
                "COSMOS_CONTAINER": self.COSMOS_CONTAINER
            }.items() if not value
        ]

        if missing_connection_value:
            raise Exception(f"Missing required configuration: {', '.join(missing_connection_value)}")


    def database(self, client:CosmosClient):
        try:
            return client.get_database_client(self.COSMOS_DATABASE)
        except exceptions.CosmosResourceNotFoundError:
            raise Exception("Database not found")
        except Exception as error:
            raise Exception(f"An error occured while fetching database: {error}")
    
    def container(self, client: CosmosClient):
        try:
            database_obj = self.database(client)
            return database_obj.get_container_client(self.COSMOS_CONTAINER)
        except exceptions.CosmosResourceNotFoundError:
            raise Exception("Container not found")
        except Exception as error:
            raise Exception(f"An error occured while fetching container: {error}")
        
    def session(self):
        client = cosmos_client.CosmosClient(self.ACCOUNT_HOST, self.ACCOUNT_KEY)
        try:
            database = self.database(client)
            container = self.container(client)
            return database, container
        except Exception as error:
            return {"error": str(error)}
    
    def read_item(self, container_obj, item_id: str, partition_key: str) -> dict:
        return container_obj.read_item(item_id, partition_key)
    
    def read_items(self, container_obj, max_count: Optional[int] = None) -> dict:
        return container_obj.read_all_items(max_item_count = max_count)
    
    def create_item(self, container_obj, body: dict) -> dict:
        return container_obj.create_item(body)
    
    def get_request_charge(self, container_obj):
        return container_obj.client_connection.last_response_headers['x-ms-request-charge']

        
    

        
    
    





















"""
def get_items(self):
        database, container = self.session()

        items = list(container.read_all_items(max_item_count=100))
        request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

        return items, request_charge
    
    def get_item(self, container, item_id, partition_key):
        container = self.get_instance()
        item = container.read_item(item=item_id, partition_key=partition_key)
        request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

        return item, request_charge
    
    def create_item(self, container, item_body):
        new_item = container.create_item(body=item_body, enable_automatic_id_generation=True)
        request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

        return new_item
    
    def delete_item(self, item_id, partition_key):
        database, container = self.session()
        response = container.delete_item(item=item_id, partition_key=partition_key)
        request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

        return response, request_charge
    
    def get_instance(self):
        database, container = self.session()

        return container
    


def cosmos_session(self):
        return cosmos_client(self.ACCOUNT_HOST, self.ACCOUNT_KEY)
    
    def get_creds(self):
        return {
            "ACCOUNT_HOST": self.ACCOUNT_HOST,
            "ACCOUNT_KEY": self.ACCOUNT_KEY,
            "COSMOS_DATABASE": self.COSMOS_DATABASE,
            "COSMOS_CONTAINER": self.COSMOS_CONTAINER
        }
    
    async def get_or_create_db(self, databse_name: Optional[str] = None):
        databse_name = databse_name if databse_name else self.COSMOS_DATABASE
        async with self.cosmos_session() as client:
            try:
                database_obj = client.get_database_client(databse_name)
                await database_obj.read()
                return database_obj
            except exceptions.CosmosResourceNotFoundError:
                return "Database not found"

    
    async def get_or_create_container(self, database_obj, container_name: Optional[str] = None):
        container_name = container_name if container_name else self.COSMOS_CONTAINER
        try:
            items_container = database_obj.get_container_client(container_name)
            await items_container.read()
            return items_container
        except exceptions.CosmosResourceNotFoundError:
            return f"Container: {container_name} not found"
    
    async def read_itmes(self, container_obj, items_to_read):
        for family in items_to_read:
            item_response = await container_obj.read_item(item=family['id'], partition_key=family['Author'])
            print(item_response)


"""