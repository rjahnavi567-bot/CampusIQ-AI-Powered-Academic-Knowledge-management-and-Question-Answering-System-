from .upload_statistics import upload_stats


class StatisticsCollector:
    """
    Single interface used by every pipeline.
    Pipelines never directly touch upload_stats.
    """

    def increment(self, name, value=1):
        upload_stats.increment(name, value)

    def add_time(self, name, seconds):
        upload_stats.add_time(name, seconds)

    def set(self, name, value):
        upload_stats.set(name, value)

    def report(self):
        return upload_stats.report()

    def reset(self):
        upload_stats.reset()


collector = StatisticsCollector()