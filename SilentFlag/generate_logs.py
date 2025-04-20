import random
from datetime import datetime, timedelta
import pandas as pd
import os

def generate_mock_logs(num_logs=50):
    users = ['Abhishek Tiwari', 'Sahil Singh', 'Kumar Satyam', 'Karan Sharma']
    logs = []

    for _ in range(num_logs):
        user = random.choice(users)
        timestamp = datetime.now() - timedelta(minutes=random.randint(0, 10000))
        file_downloads = random.randint(0, 50)
        logs.append({
            'username': user,
            'timestamp': timestamp,
            'downloads': file_downloads
        })

    df = pd.DataFrame(logs)

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/user_logs.csv", index=False)
    print("✅ Log data saved to data/user_logs.csv")

if __name__ == "__main__":
    generate_mock_logs()
