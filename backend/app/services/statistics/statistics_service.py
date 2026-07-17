import time
import json
import os
from collections import defaultdict


class StatisticsService:
    """
    Stores runtime statistics for the AI Academic System.
    """

    _instance = None


    def __init__(self):

        self.counters = defaultdict(int)

        self.timers = defaultdict(list)

        self.statistics_file = os.path.join(
    os.path.dirname(__file__),
    "statistics.json"
)

        self.load()

    # ---------------------------------------------------
    # Singleton
    # ---------------------------------------------------

    @classmethod
    def get_instance(cls):

        if cls._instance is None:
            cls._instance = StatisticsService()

        return cls._instance

    # ---------------------------------------------------
    # Counters
    # ---------------------------------------------------

    def increment(self, name, value=1):

        self.counters[name] += value
        self.save()

    def set_value(self, name, value):

        self.counters[name] = value
        self.save()

    def get(self, name):

        return self.counters.get(name, 0)

    # ---------------------------------------------------
    # Timers
    # ---------------------------------------------------

    def add_time(self, name, seconds):

        self.timers[name].append(seconds)
        self.save()

    def average_time(self, name):

        values = self.timers.get(name, [])

        if len(values) == 0:
            return 0

        return round(sum(values) / len(values), 3)

    # ---------------------------------------------------
    # Report
    # ---------------------------------------------------

    def report(self):

        data = {}

        for key, value in self.counters.items():
            data[key] = value

        for key in self.timers:

            data[f"Average {key}"] = self.average_time(key)

        return data
    
        # ---------------------------------------------------
    # Merge upload statistics into global statistics
    # ---------------------------------------------------

    def merge_upload_statistics(self, upload_stats):

        # Merge counters
        for key, value in upload_stats.counters.items():

            self.counters[key] += value

        # Merge timers
        for key, values in upload_stats.timers.items():

            self.timers[key].extend(values)
        self.save()
    # ---------------------------------------------------
# Persistence
# ---------------------------------------------------

    def load(self):
      """
    Load saved statistics from disk.
      """

      if not os.path.exists(self.statistics_file):
         return

      try:

        with open(
            self.statistics_file,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        self.counters.update(
            data.get("counters", {})
        )

        self.timers.update(
            data.get("timers", {})
        )

      except Exception as e:

        print(
            "Statistics load failed:",
            e
        )


    def save(self):
      """
    Save statistics to disk.
      """

      data = {

        "counters": dict(self.counters),

        "timers": dict(self.timers)

    }

      with open(
        self.statistics_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )