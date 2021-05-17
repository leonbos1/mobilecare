#import winsound
#from win10toast import ToastNotifier

#def timer(remider, seconds):
#    notificator=ToastNotifier()
#    notificator.show_toast("Reminder", f"""Alarm will go off in {seconds} Seconds, """, duration=20)
#    notificator.show_toast(f"Reminder", reminder, duration=20)

    #alarm
#    frequency=2500
#    duration=1000
#    winsound.Beep(frequency, duration)

#if __name__=="__main__":
#    words=input("What would you reminds of: ")
#    sec=int(input("Enter seconds: "))
#    timer(words,sec)

import numpy as np
import matplotlib.pyplot as plt

data = np.random.randn(5000) * 20 + 20 #Als voorbeeld.

# Zoekt afwijkingen.

def find_anomalies(data):
    anomalies = []

    random_data_std = std(random_data)
    random_data_mean = mean(random_data)
    anomaly_cut_off = random_data_std * 3

    lower_limit = random_data_mean - anomaly_cut_off
    upper_limit = random_data_mean + anomaly_cut_off
    print(lower_limit)

    for outlier in random_data:
        if outlier > upper_limit or outlier < lower_limit:
            anomalies.append(outlier)
    return anomalies

find_anomalies(data)
