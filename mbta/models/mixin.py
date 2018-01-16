class DirectionMixin:
    @property
    def direction_name(self):
        if self.direction_id is not None and self.route is not None:
            return self.route.direction_names[self.direction_id]

        return '<unknown>'


class LocationMixin:
    @property
    def location(self):
        from .common import Point
        return Point(latitude=self.latitude, longitude=self.longitude)
