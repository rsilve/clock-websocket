class Payload:
    def __init__(self, mode, timestamp, since, to=None):
        self.mode = mode
        self.timestamp = timestamp
        self.since = since
        self.to = to

    def __str__(self):
        return "Payload(type={}, timestamp={}, since={}, to={}".format(self.mode, self.timestamp, self.since, self.to)

    def to_dict(self):
        return {
            "mode": self.mode,
            "timestamp": self.timestamp,
            "since": self.since,
            "to": self.to
        }