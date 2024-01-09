class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline_time, weight):
        """Initialize the package with the provided attributes."""
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.status = "At Hub"
        self.departure_time = None
        self.delivery_time = None

        self.corrected_address = False

    def __str__(self):
        """Return a string representation of the package."""
        return (f"{self.ID}, {self.address}, {self.city}, {self.state}, {self.zipcode}, "
                f"{self.deadline_time}, {self.weight}Kg, Delivered at: {self.delivery_time}, Status: {self.status}")

    def update_status(self, current_time):
        """Update package status based on current time."""
        if self.delivery_time and self.delivery_time <= current_time:
            self.status = "Delivered"
        elif self.departure_time and self.departure_time <= current_time:
            self.status = "En route"
        else:
            self.status = "At Hub"
