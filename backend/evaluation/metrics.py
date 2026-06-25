correct = 0
total = 10

# Manually inspect

correct += 1  # data mining (partial)
correct += 1  # clustering
correct += 0  # classification
correct += 1  # association rule mining
correct += 1  # data warehouse
correct += 1  # kmeans
correct += 0  # regression
correct += 0  # outlier detection
correct += 0  # supervised
correct += 0  # unsupervised

recall_at_3 = correct / total

print("Recall@3 =", recall_at_3)