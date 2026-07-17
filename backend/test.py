from app.services.statistics import stats

stats.increment("documents_uploaded")

stats.increment("documents_uploaded")

print(stats.report())