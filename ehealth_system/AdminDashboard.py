# Import necessary libraries
import matplotlib.pyplot as plt


# User authentication class
class Authentication:
    """
    Handles user authentication for the admin dashboard.
    """
    def __init__(self):
        self.credentials = {"ayla": "ayla123"}  # Default admin credentials

    def login(self):
        print("\n--- Admin Login ---")
        username = input("Enter username: ")
        password = input("Enter password: ")
        if self.credentials.get(username) == password:
            print("Login successful!\n")
            return True
        else:
            print("Invalid credentials. Please try again.\n")
            return False

# Resident class
class Resident:
    def __init__(self, name):
        self.name = name
        self.notifications = []

    def update(self, announcement):
        self.notifications.append(announcement)
        print(f"Notification for {self.name}: {announcement}")

    def view_notifications(self):
        print(f"\n{self.name}'s Notification History:")
        for i, notification in enumerate(self.notifications, 1):
            print(f"{i}. {notification}")

# Announcement System class
class AnnouncementSystem:
    def __init__(self):
        self.residents = []
        self.announcements = []

    def subscribe(self, resident):
        if resident not in self.residents:
            self.residents.append(resident)

    def post_announcement(self, announcement):
        self.announcements.append(announcement)
        for resident in self.residents:
            resident.update(announcement)

    def view_announcements(self):
        print("\n--- All Announcements ---")
        for i, announcement in enumerate(self.announcements, 1):
            print(f"{i}. {announcement}")

    def delete_announcement(self, announcement_id):
        if 0 < announcement_id <= len(self.announcements):
            deleted = self.announcements.pop(announcement_id - 1)
            print(f"Announcement '{deleted}' deleted successfully.")
        else:
            print("Error: Announcement ID not found.")

# Admin Dashboard class
class AdminDashboard:
    def __init__(self, announcement_system):
        self.infection_data = {}
        self.recovery_data = {}
        self.announcement_system = announcement_system

    def show_dashboard(self):
        while True:
            print("\n--- Admin Dashboard ---")
            print("1. View Infection Trends")
            print("2. Manage Announcements")
            print("3. Update Infection Data")
            print("4. Visualize Infection Trends")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_infection_trends()
            elif choice == "2":
                self.manage_announcements()
            elif choice == "3":
                self.update_infection_data()
            elif choice == "4":
                self.visualize_infection_trends()
            elif choice == "5":
                print("Exiting dashboard. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def view_infection_trends(self):
        print("\n--- Infection Trends ---")
        for area, cases in self.infection_data.items():
            recoveries = self.recovery_data.get(area, 0)
            print(f"{area}: {cases} active cases, {recoveries} recoveries")
        self.identify_hotspots()

    def identify_hotspots(self):
        print("\n--- Hotspots ---")
        hotspots = [area for area, cases in self.infection_data.items() if cases > 10]
        if hotspots:
            print(f"High infection areas: {', '.join(hotspots)}")
        else:
            print("No hotspots detected.")

    def manage_announcements(self):
        while True:
            print("\n--- Manage Announcements ---")
            print("1. Post an Announcement")
            print("2. View All Announcements")
            print("3. Delete an Announcement")
            print("4. Back to Dashboard")
            choice = input("Enter your choice: ")

            if choice == "1":
                announcement = input("Enter the announcement: ")
                self.announcement_system.post_announcement(announcement)
            elif choice == "2":
                self.announcement_system.view_announcements()
            elif choice == "3":
                try:
                    announcement_id = int(input("Enter the Announcement ID to delete: "))
                    self.announcement_system.delete_announcement(announcement_id)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    def update_infection_data(self):
        print("\n--- Update Infection Data ---")
        while True:
            area = input("Enter area name (or type 'done' to finish): ")
            if area.lower() == 'done':
                break
            try:
                cases = int(input(f"Enter active cases for {area}: "))
                recoveries = int(input(f"Enter recoveries for {area}: "))
                self.infection_data[area] = cases
                self.recovery_data[area] = recoveries
                print(f"Data updated for {area}.")
            except ValueError:
                print("Invalid input. Please enter numbers for cases and recoveries.")

    def visualize_infection_trends(self):
        areas = list(self.infection_data.keys())
        cases = list(self.infection_data.values())
        recoveries = [self.recovery_data.get(area, 0) for area in areas]

        plt.figure(figsize=(10, 6))
        plt.bar(areas, cases, color='red', label='Active Cases')
        plt.bar(areas, recoveries, color='green', label='Recoveries', alpha=0.7)
        plt.xlabel("Areas")
        plt.ylabel("Number of Cases")
        plt.title("Infection and Recovery Trends")
        plt.legend()
        plt.show()

# Main function
if __name__ == "__main__":
    # Authenticate admin
    auth = Authentication()
    if auth.login():
        # Initialize Announcement System
        announcement_system = AnnouncementSystem()

        # Create residents and subscribe them
        resident1 = Resident("Alice")
        resident2 = Resident("Bob")
        resident3 = Resident("Charlie")
        announcement_system.subscribe(resident1)
        announcement_system.subscribe(resident2)
        announcement_system.subscribe(resident3)

        # Initialize and run Admin Dashboard
        admin_dashboard = AdminDashboard(announcement_system)
        admin_dashboard.show_dashboard()