class Cafe:
    def __init__(self, name, google_map, picture, location_area, sockets, toilets, wifi, calls, seats, coffee):
        self.name = name
        self.map_url = google_map
        self.picture_url = picture
        self.location = location_area
        self.has_sockets = self.has(sockets)
        self.has_toilets = self.has(toilets)
        self.has_wifi = self.has(wifi)
        self.can_take_calls = self.has(calls)
        self.seats_num = seats
        self.coffee_price = coffee

    def has(self, item):
        if item == 1:
            return "Yes"
        else:
            return "No"