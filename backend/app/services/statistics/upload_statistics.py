from collections import defaultdict


class UploadStatistics:

    def __init__(self):
        self.reset()

    def reset(self):
        self.counters = defaultdict(int)
        self.timers = defaultdict(list)

    def increment(self, name, value=1):
        self.counters[name] += value

    def set(self, name, value):
        self.counters[name] = value

    def add_time(self, name, seconds):
        self.timers[name].append(seconds)

    def average(self, name):
        values = self.timers.get(name, [])

        if len(values) == 0:
            return 0

        return round(sum(values) / len(values), 3)

    def report(self):

        report = {}

        report.update(self.counters)

        for key in self.timers:
            report[f"Average {key}"] = self.average(key)

        return report


# Singleton instance
upload_stats = UploadStatistics()