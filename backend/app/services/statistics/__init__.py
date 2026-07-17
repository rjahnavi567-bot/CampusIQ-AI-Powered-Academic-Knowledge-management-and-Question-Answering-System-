from .statistics_service import StatisticsService
from .upload_statistics import upload_stats
from .statistics_collector import collector

stats = StatisticsService.get_instance()