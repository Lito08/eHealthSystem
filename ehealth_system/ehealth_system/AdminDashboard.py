# Import required library for data visualization
import matplotlib.pyplot as plt

# Announcement System classes (from the previous implementation)
class Resident:
    """
    Represents a resident subscribed to announcements.
    """
    def __init__(self, name):
        self.name = name
        self.notifications = []

    def update(self, announcement):
        self.notifications.append(announcement)  # Add announcement to resident's notifications
        print(f"Notification for {self.name}: {announcement}")  # Display notification

    def view_notifications(self):
        print(f"\n{self.name}'s Notification History:")
        for i, notification in enumerate(self.notifications, 1):
            print(f"{i}. {notification}")  # Display notification history


class AnnouncementSystem:
    """
    Manages announcements and notifies subscribed residents.
    """
    def __init__(self):
        self.residents = []
        self.announcements = []

    def subscribe(self, resident):
        self.residents.append(resident)  # Add resident to the subscriber list

    def post_announcement(self, announcement):
        self.announcements.append(announcement)  # Add announcement to the list
        for resident in self.residents:
            resident.update(announcement)  # Notify all subscribed residents

    def view_announcements(self):
        print("\n--- All Announcements ---")
        for i, announcement in enumerate(self.announcements, 1):
            print(f"{i}. {announcement}")  # Display all announcements

    def delete_announcement(self, announcement_id):
        if 0 < announcement_id <= len(self.announcements):
            deleted = self.announcements.pop(announcement_id - 1)  # Remove the announcement
            print(f"Announcement '{deleted}' deleted successfully.")
        else:
            print("Error: Announcement ID not found.")  # Handle invalid IDs


# Admin Dashboard class for infection trends and analytics
class AdminDashboard:
    """
    Provides analytics, trends, and management options for admins.
    """
    def __init__(self, announcement_system):
        self.infection_data = {"Area A": 10, "Area B": 5, "Area C": 15}  # Infection data
        self.recovery_data = {"Area A": 3, "Area B": 2, "Area C": 4}    # Recovery data
        self.announcement_system = announcement_system  # Link to announcement system

    def show_dashboard(self):
        """
        Main menu for the admin dashboard.
        """
        while True:
            print("\n--- Admin Dashboard ---")
            print("1. View Infection Trends")
            print("2. Manage Announcements")
            print("3. Visualize Infection Trends")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_infection_trends()
            elif choice == "2":
                self.manage_announcements()
            elif choice == "3":
                self.visualize_infection_trends()
            elif choice == "4":
                print("Exiting dashboard. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def view_infection_trends(self):
        """
        Display infection and recovery trends for different areas.
        """
        print("\n--- Infection Trends ---")
        for area, cases in self.infection_data.items():
            recoveries = self.recovery_data.get(area, 0)
            print(f"{area}: {cases} active cases, {recoveries} recoveries")
        self.identify_hotspots()

    def identify_hotspots(self):
        """
        Identify areas with high infection rates.
        """
        print("\n--- Hotspots ---")
        hotspots = [area for area, cases in self.infection_data.items() if cases > 10]
        if hotspots:
            print(f"High infection areas: {', '.join(hotspots)}")
        else:
            print("No hotspots detected.")

    def manage_announcements(self):
        """
        Manage announcements (post, view, delete).
        """
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

    def visualize_infection_trends(self):
        """
        Generate a bar chart to visualize infection and recovery trends.
        """
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


# Main function to initialize and run the system
if __name__ == "__main__":
    # Initialize Announcement System
    announcement_system = AnnouncementSystem()

    # Create residents and subscribe them to the announcement system
    resident1 = Resident("Alice")
    resident2 = Resident("Bob")
    resident3 = Resident("Charlie")
    announcement_system.subscribe(resident1)
    announcement_system.subscribe(resident2)
    announcement_system.subscribe(resident3)

    # Initialize and run Admin Dashboard
    admin_dashboard = AdminDashboard(announcement_system)
    admin_dashboard.show_dashboard()
