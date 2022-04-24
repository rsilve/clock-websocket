class Payload:
    def __init__(self, mode, timestamp, delay, since):
        self.mode = mode
        self.timestamp = timestamp
        self.delay = delay
        self.since = since

    def __str__(self):
        return "Payload(type={}, timestamp={}, delay={}, since={}".format(self.mode, self.timestamp, self.delay, self.since)

    def to_dict(self):
        return {
            "mode": self.mode,
            "timestamp": self.timestamp,
            "delay": self.delay,
            "since": self.since
        }