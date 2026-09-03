import sys

class CafeteriaSystem:
    def __init__(self):
        self.users = {
            "student1": {"role": "Student", "balance": 500.0, "pin": "1234"},
            "vendor1": {"role": "Vendor", "balance": 0.0, "pin": "0000"},
            "staff1": {"role": "Kitchen", "balance": 0.0, "pin": "1111"}
        }
        self.menu = {
            1: {"name": "Burger", "price": 50.0, "available": True},
            2: {"name": "Pizza Slice", "price": 80.0, "available": True},
            3: {"name": "Cold Coffee", "price": 40.0, "available": True}
        }
        self.orders = []
        self.current_user = None

    def login(self):
        print("\n--- Login ---")
        username = input("Enter Username (student1, vendor1, staff1): ").strip()
        if username in self.users:
            pin = input("Enter PIN: ").strip()
            if pin == self.users[username]["pin"]:
                self.current_user = username
                print(f"Welcome, {username}! Role: {self.users[username]['role']}")
                return True
        print("Invalid credentials.")
        return False

    def student_menu(self):
        while True:
            print(f"\n--- Student Menu (Balance: ${self.users[self.current_user]['balance']:.2f}) ---")
            print("1. View Menu")
            print("2. Place Order")
            print("3. Logout")
            choice = input("Select option: ").strip()
            
            if choice == "1":
                self.view_menu()
            elif choice == "2":
                self.place_order()
            elif choice == "3":
                self.current_user = None
                break
            else:
                print("Invalid choice.")

    def view_menu(self):
        print("\n--- Current Menu ---")
        for item_id, details in self.menu.items():
            status = "Available" if details["available"] else "Out of Stock"
            print(f"{item_id}. {details['name']} - ${details['price']:.2f} [{status}]")

    def place_order(self):
        self.view_menu()
        item_id = input("Enter Item ID to order: ").strip()
        try:
            item_id = int(item_id)
            if item_id in self.menu and self.menu[item_id]["available"]:
                item = self.menu[item_id]
                if self.users[self.current_user]["balance"] >= item["price"]:
                    self.users[self.current_user]["balance"] -= item["price"]
                    order_id = len(self.orders) + 1
                    order = {
                        "id": order_id,
                        "student": self.current_user,
                        "item": item["name"],
                        "price": item["price"],
                        "status": "Received"
                    }
                    self.orders.append(order)
                    print(f"\n[Digital Receipt] Order #{order_id} placed successfully!")
                    print(f"Item: {item['name']} | Paid: ${item['price']:.2f}")
                else:
                    print("Insufficient Campus ID balance.")
            else:
                print("Invalid item or item is out of stock.")
        except ValueError:
            print("Please enter a valid number.")

    def vendor_menu(self):
        while True:
            print("\n--- Vendor Menu ---")
            print("1. Toggle Item Availability")
            print("2. View All Orders")
            print("3. Logout")
            choice = input("Select option: ").strip()
            
            if choice == "1":
                self.view_menu()
                item_id = input("Enter Item ID to toggle availability: ").strip()
                try:
                    item_id = int(item_id)
                    if item_id in self.menu:
                        self.menu[item_id]["available"] = not self.menu[item_id]["available"]
                        status = "Available" if self.menu[item_id]["available"] else "Out of Stock"
                        print(f"Item {self.menu[item_id]['name']} is now {status}.")
                    else:
                        print("Invalid item ID.")
                except ValueError:
                    print("Invalid input.")
            elif choice == "2":
                self.view_orders()
            elif choice == "3":
                self.current_user = None
                break
            else:
                print("Invalid choice.")

    def kitchen_menu(self):
        while True:
            print("\n--- Kitchen Display System (KDS) ---")
            print("1. View Active Orders")
            print("2. Update Order Status")
            print("3. Logout")
            choice = input("Select option: ").strip()
            
            if choice == "1":
                self.view_orders()
            elif choice == "2":
                self.view_orders()
                order_id = input("Enter Order ID to mark as 'Ready': ").strip()
                try:
                    order_id = int(order_id)
                    found = False
                    for o in self.orders:
                        if o["id"] == order_id:
                            o["status"] = "Ready"
                            print(f"Order #{order_id} marked as Ready.")
                            found = True
                            break
                    if not found:
                        print("Order not found.")
                except ValueError:
                    print("Invalid input.")
            elif choice == "3":
                self.current_user = None
                break
            else:
                print("Invalid choice.")

    def view_orders(self):
        print("\n--- Order Queue ---")
        if not self.orders:
            print("No orders yet.")
            return
        for o in self.orders:
            print(f"Order #{o['id']} | Student: {o['student']} | Item: {o['item']} | Status: {o['status']}")

    def run(self):
        print("=== Smart Campus Cafeteria CLI Prototype (Sprint 1) ===")
        while True:
            if not self.current_user:
                success = self.login()
                if not success:
                    cont = input("Try again? (y/n): ").strip().lower()
                    if cont != 'y':
                        break
            else:
                role = self.users[self.current_user]["role"]
                if role == "Student":
                    self.student_menu()
                elif role == "Vendor":
                    self.vendor_menu()
                elif role == "Kitchen":
                    self.kitchen_menu()

if __name__ == "__main__":
    app = CafeteriaSystem()
    app.run()