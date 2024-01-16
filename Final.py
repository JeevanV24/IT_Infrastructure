import mysql.connector
import re

class InventoryManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="it"
        )
        self.cursor = self.conn.cursor()
        self.software_list = []  # Initialize an empty list to store software items

    def register_software(self, software_name, software_version):
        version_pattern = r'\d+\.\d+\.\d+'  # Regular Expression for x.x.x format
        if re.match(version_pattern, software_version):
            query = "INSERT INTO software_inventory (software_name, software_version) VALUES (%s, %s)"
            values = (software_name, software_version)
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Software registered successfully.")
        else:
            print("Invalid software version format. Please use x.x.x format.")

    def update_software_status(self, software_id, new_status):
        query = "UPDATE software_inventory SET software_status = %s WHERE software_id = %s"
        values = (new_status, software_id)
        self.cursor.execute(query, values)
        self.conn.commit()
        print(f"Software {software_id} status updated to {new_status}.")

    def track_software(self, software_id):
        query = "SELECT * FROM software_inventory WHERE software_id = %s"
        self.cursor.execute(query, (software_id,))
        software = self.cursor.fetchone()
        if software:
            print(f"Software tracked successfully: {software}")
        else:
            print(f"Software with ID {software_id} not found in the inventory.")

    def list_all_software(self):
        query = "SELECT * FROM software_inventory"
        self.cursor.execute(query)
        software_list = self.cursor.fetchall()
        if software_list:
            print("All Software Items:")
            print("ID\tName\tVersion\tStatus")
            # List comprehension being implemented
            formatted_list = [f"{software[0]}\t{software[1]}\t{software[2]}\t{software[3]}" for software in software_list]
            for item in formatted_list:
                print(item)
        else:
            print("No software items found in the inventory.")

    def delete_software(self, software_id):
        check_query = "SELECT * FROM software_inventory WHERE software_id = %s"
        self.cursor.execute(check_query, (software_id,))
        software = self.cursor.fetchone()

        if software:
            delete_query = "DELETE FROM software_inventory WHERE software_id = %s"
            self.cursor.execute(delete_query, (software_id,))
            self.conn.commit()
            print(f"Software {software_id} deleted successfully.")
        else:
            print(f"Software with ID {software_id} not found in the inventory.")


    
    def inventory_menu(self):
        while True:
            print("\nInventory Management Menu:")
            print("1. Register New Software")
            print("2. Update Software Status")
            print("3. Track Software")
            print("4. List All Software")
            print("5. Delete Software")
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                software_name = input("Enter software name: ")
                software_version = input("Enter software version: ")
                self.register_software(software_name, software_version)
            elif choice == '2':
                software_id = int(input("Enter software ID to update status: "))
                new_status = input("Enter new status: ")
                self.update_software_status(software_id, new_status)
            elif choice == '3':
                software_id = int(input("Enter software ID to track: "))
                self.track_software(software_id)
            elif choice == '4':
                self.list_all_software()
            elif choice == '5':
                software_id = int(input("Enter software ID to delete: "))
                self.delete_software(software_id)
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please select again.")

    def __del__(self):
        self.cursor.close()
        self.conn.close()







class AssetManager:
    # Set containing valid statuses and the use of Lambda function
    valid_statuses = lambda self, status: status in {"Use", "Repair"}    
    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='it'
        )
        self.cursor = self.db.cursor()

    def register_asset(self, asset_name, asset_status):
        #Exception Handling
        try:
            if not self.valid_statuses(asset_status):
                raise ValueError("Invalid status. Status should be 'Use' or 'Repair'.")

            sql = "INSERT INTO assets (name, status) VALUES (%s, %s)"
            values = (asset_name, asset_status)
            self.cursor.execute(sql, values)
            self.db.commit()
            print("Asset registered successfully.")
        except ValueError as e:
            print(str(e))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        

    def update_asset_status(self, asset_id):
        # Check if the asset with the given ID exists
        self.cursor.execute("SELECT * FROM assets WHERE id = %s", (asset_id,))
        existing_asset = self.cursor.fetchone()

        if existing_asset:
            new_status = input("Enter new status: ")
            if not self.valid_statuses(new_status):
                print("Invalid status. Status should be 'Use' or 'Repair'.")
                return
            sql = "UPDATE assets SET status = %s WHERE id = %s"
            values = (new_status, asset_id)
            self.cursor.execute(sql, values)
            self.db.commit()
            print(f"Asset {asset_id} status updated to {new_status}.")
        else:
            print(f"Asset {asset_id} not found.")
            return  # Exit the method if asset not found


    def delete_asset(self, asset_id):
        #Error Handling
        try:
            self.cursor.execute("SELECT * FROM assets WHERE id = %s", (asset_id,))
            existing_asset = self.cursor.fetchone()

            if existing_asset:
                sql = "DELETE FROM assets WHERE id = %s"
                self.cursor.execute(sql, (asset_id,))
                self.db.commit()
                print(f"Asset {asset_id} deleted successfully.")
            else:
                print(f"Asset {asset_id} not found.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        

            

    def list_all_assets(self):
        self.cursor.execute("SELECT id, name, status FROM assets")
        assets = self.cursor.fetchall()

        if assets:
            print("\nList of Assets:")
            print("ID\tName\tStatus")
            for asset in assets:
                print(f"{asset[0]}\t{asset[1]}\t{asset[2]}")
        else:
            print("No assets found.")        
    


    def asset_menu(self):
        while True:
            print("\nAsset Management Menu:")
            print("1. Register New Asset")
            print("2. Update Asset Status")
            print("3. Delete Asset")
            print("4. List All Assets")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                asset_name = input("Enter asset name: ")
                asset_status = input("Enter asset status: ")
                self.register_asset(asset_name, asset_status)
            elif choice == '2':
                update_id = int(input("Enter asset ID to update status: "))
                #new_status = input("Enter new status: ")
                self.update_asset_status(update_id)
            elif choice == '3':
                delete_id = int(input("Enter asset ID to delete: "))
                self.delete_asset(delete_id)
            elif choice == '4':
                self.list_all_assets()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please select again.")

    def close_connection(self):
        self.cursor.close()
        self.db.close()






class SecuritySystem:
    def __init__(self):
        # Dictionary containing the users, passwords and their role 
        self.users = {
            "user1": {"password": "pass1", "role": "asset"},
            "user2": {"password": "pass2", "role": "manager"}
        }

    def login(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            role = self.users[username]["role"]
            if role == "asset":
                print("Logged in as asset user.")
                return AssetManager()  # Return AssetInventory for asset users
            elif role == "manager":
                print("Logged in as inventory manager.")
                return InventoryManager()  # Return InventoryManager for manager users
        else:
            print("Invalid username or password.")
            return None


while(1):
    security_system = SecuritySystem()
    # Login attempt
    username = input("Enter username: ")
    password = input("Enter password: ")

    system_access = security_system.login(username, password)

    if system_access:
        if isinstance(system_access, AssetManager):
            # Access Asset Inventory functionality
            manager = AssetManager()
            manager.asset_menu()
            manager.close_connection()
            # Additional asset functionalities can be accessed here based on requirements
        elif isinstance(system_access, InventoryManager):
            # Access Inventory Manager functionality
            inventory_manager = InventoryManager()
            inventory_manager.inventory_menu()
