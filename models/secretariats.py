class secretariats:
    def __init__(self, s_id, name, campus, building, timetable,description):
        self.name = name
        self.campus = campus
        self.building = building
        self.id = s_id
        self.timetable=timetable
        self.description=description

    def __str__(self):
        return "%d - %s - %s - %s - %s - %s" % (self.id, self.name, self.campus, self.building, self.timetable, self.description)