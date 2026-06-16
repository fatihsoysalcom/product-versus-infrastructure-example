import time
import random

# --- INFRASTRUCTURE LAYER ---
# These components provide foundational services.
# Users don't directly interact with them; they support the product.

class DatabaseService:
    """Simulates a database for storing application data."""
    def __init__(self):
        self.data_store = {}
        print("INFRASTRUCTURE: DatabaseService initialized.")

    def save(self, key, value):
        """Simulates saving data to the database."""
        time.sleep(0.05) # Simulate latency
        self.data_store[key] = value
        print(f"INFRASTRUCTURE: Data '{key}' saved.")
        return True

    def retrieve(self, key):
        """Simulates retrieving data from the database."""
        time.sleep(0.03) # Simulate latency
        value = self.data_store.get(key)
        print(f"INFRASTRUCTURE: Data '{key}' retrieved: {value}")
        return value

class LoggingService:
    """Simulates a logging system for recording events."""
    def __init__(self):
        print("INFRASTRUCTURE: LoggingService initialized.")

    def log_event(self, event_type, message):
        """Logs an event with a timestamp."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"INFRASTRUCTURE: [{timestamp}] {event_type.upper()}: {message}")

class NotificationService:
    """Simulates sending notifications (e.g., email, SMS)."""
    def __init__(self):
        print("INFRASTRUCTURE: NotificationService initialized.")

    def send_notification(self, recipient, subject, body):
        """Simulates sending a notification to a recipient."""
        time.sleep(0.1) # Simulate network delay
        print(f"INFRASTRUCTURE: Notification sent to {recipient} - Subject: '{subject}'")
        return True

# --- PRODUCT LAYER ---
# This is the user-facing application that delivers value.
# It uses the infrastructure services to perform its functions.

class UserManagementProduct:
    """
    A product that allows users to register, login, and manage profiles.
    It provides direct value to the end-user.
    """
    def __init__(self, db_service, log_service, notif_service):
        self.db = db_service
        self.logger = log_service
        self.notifier = notif_service
        self.users = {} # In-memory cache for simplicity
        print("PRODUCT: UserManagementProduct initialized.")

    def register_user(self, username, password, email):
        """
        Product feature: Allows a new user to register.
        Uses infrastructure services (database, logging, notification).
        """
        if self.db.retrieve(f"user_{username}"):
            self.logger.log_event("WARNING", f"Registration attempt for existing user: {username}")
            print(f"PRODUCT: Registration failed. User '{username}' already exists.")
            return False

        user_data = {"password": password, "email": email, "created_at": time.time()}
        self.db.save(f"user_{username}", user_data)
        self.users[username] = user_data # Update cache
        self.logger.log_event("INFO", f"New user registered: {username}")
        self.notifier.send_notification(email, "Welcome to our service!", f"Hi {username}, welcome aboard!")
        print(f"PRODUCT: User '{username}' registered successfully.")
        return True

    def login_user(self, username, password):
        """
        Product feature: Allows an existing user to log in.
        Uses infrastructure services (database, logging).
        """
        user_data = self.db.retrieve(f"user_{username}")
        if user_data and user_data["password"] == password:
            self.logger.log_event("INFO", f"User logged in: {username}")
            print(f"PRODUCT: User '{username}' logged in successfully.")
            return True
        else:
            self.logger.log_event("ERROR", f"Failed login attempt for user: {username}")
            print(f"PRODUCT: Login failed for '{username}'. Invalid credentials.")
            return False

    def get_user_profile(self, username):
        """
        Product feature: Retrieves a user's profile.
        Uses infrastructure services (database).
        """
        user_data = self.db.retrieve(f"user_{username}")
        if user_data:
            print(f"PRODUCT: Profile for '{username}': Email={user_data['email']}, Created={time.ctime(user_data['created_at'])}")
            self.logger.log_event("INFO", f"Profile viewed for: {username}")
            return user_data
        else:
            print(f"PRODUCT: User '{username}' not found.")
            self.logger.log_event("WARNING", f"Attempt to view non-existent user profile: {username}")
            return None

# --- MAIN APPLICATION EXECUTION ---
if __name__ == "__main__":
    print("--- Initializing Digital Ecosystem ---")

    # Initialize Infrastructure Services
    # These are the underlying "building blocks" that the product relies on.
    # They provide common, reusable functionalities.
    db_service = DatabaseService()
    log_service = LoggingService()
    notif_service = NotificationService()

    print("\n--- Initializing Product ---")
    # Initialize the Product, injecting the infrastructure services it needs.
    # The product is what the end-user directly interacts with and derives value from.
    user_product = UserManagementProduct(db_service, log_service, notif_service)

    print("\n--- Demonstrating Product Usage ---")

    # User 1 interacts with the product
    print("\n--- User Alice's Journey ---")
    user_product.register_user("alice", "pass123", "alice@example.com")
    user_product.login_user("alice", "pass123")
    user_product.get_user_profile("alice")

    # User 2 interacts with the product
    print("\n--- User Bob's Journey ---")
    user_product.register_user("bob", "securepwd", "bob@example.com")
    user_product.login_user("bob", "wrongpwd") # Failed login
    user_product.login_user("bob", "securepwd") # Successful login

    # Attempt to register an existing user
    print("\n--- Attempting Duplicate Registration ---")
    user_product.register_user("alice", "newpass", "alice2@example.com")

    print("\n--- Digital Ecosystem Demonstration Complete ---")
