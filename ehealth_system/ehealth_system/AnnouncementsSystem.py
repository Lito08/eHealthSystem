# Define the AnnouncementSystem class
class AnnouncementSystem:
    """
    Announcement System for managing announcements and subscribers (residents).
    """

    def __init__(self):
        self.subscribers = []  # List of subscribed residents
        self.announcements = {}  # Dictionary to store announcements (id: content)

    def subscribe(self, resident):
        """
        Add a resident to the subscribers list.
        """
        self.subscribers.append(resident)

    def notify_all(self, announcement_id):
        """
        Notify all subscribed residents about the given announcement.
        """
        announcement = self.announcements.get(announcement_id)
        if announcement:
            for subscriber in self.subscribers:
                subscriber.update(announcement)

    def delete_announcement(self, announcement_id):
        """
        Delete an announcement by its ID.
        """
        if announcement_id in self.announcements:
            del self.announcements[announcement_id]
            print(f"Announcement ID {announcement_id} deleted.")
        else:
            print("Error: Announcement ID does not exist!")


# Define the Resident class
class Resident:
    """
    Resident class representing users who receive notifications.
    """

    def __init__(self, name):
        self.name = name  # Name of the resident
        self.notifications = []  # List to store received notifications

    def update(self, announcement):
        """
        Receive a notification and store it.
        """
        self.notifications.append(announcement)
        print(f"Notification for {self.name}: {announcement}")

    def view_notifications(self):
        """
        Display all notifications received by the resident.
        """
        print(f"\n{self.name}'s Notification History:")
        for i, notification in enumerate(self.notifications, 1):
            print(f"{i}. {notification}")


# Define the Admin class
class Admin:
    """
    Admin class for creating, updating, and deleting announcements.
    """

    def __init__(self, system):
        self.system = system  # Reference to the announcement system

    def create_announcement(self):
        """
        Create a new announcement and add it to the system.
        """
        content = input("Enter the announcement content: ")
        # Generate a dynamic announcement ID
        announcement_id = max(self.system.announcements.keys(), default=0) + 1
        self.system.announcements[announcement_id] = content
        print(f"Announcement ID {announcement_id} created: {content}")
        self.system.notify_all(announcement_id)

    def update_announcement(self):
        """
        Update an existing announcement by its ID.
        """
        try:
            announcement_id = int(input("Enter the announcement ID to update: "))
            if announcement_id in self.system.announcements:
                new_content = input("Enter the new announcement content: ")
                self.system.announcements[announcement_id] = new_content
                print(f"Announcement ID {announcement_id} updated: {new_content}")
                self.system.notify_all(announcement_id)
            else:
                print("Error: Announcement ID does not exist!")
        except ValueError:
            print("Error: Please enter a valid numerical ID.")

    def delete_announcement(self):
        """
        Delete an announcement from the system.
        """
        try:
            announcement_id = int(input("Enter the announcement ID to delete: "))
            self.system.delete_announcement(announcement_id)
        except ValueError:
            print("Error: Please enter a valid numerical ID.")


# Main logic
# Create the announcement system
announcement_system = AnnouncementSystem()

# Create admin instance
admin = Admin(announcement_system)

# Create resident instances
resident1 = Resident("Alice")
resident2 = Resident("Bob")
resident3 = Resident("Charlie")

# Subscribe residents to the announcement system
announcement_system.subscribe(resident1)
announcement_system.subscribe(resident2)
announcement_system.subscribe(resident3)

# Interactive admin menu
while True:
    print("\nAdmin Menu:")
    print("1. Post a new announcement")
    print("2. Update an announcement")
    print("3. Delete an announcement")
    print("4. View all residents' notifications")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        admin.create_announcement()
    elif choice == "2":
        admin.update_announcement()
    elif choice == "3":
        admin.delete_announcement()
    elif choice == "4":
        print("\nResidents' Notifications:")
        resident1.view_notifications()
        resident2.view_notifications()
        resident3.view_notifications()
    elif choice == "5":
        print("Exiting the system. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
