import winsound
from win10toast import ToastNotifier

def timer(remider, seconds):
    notificator=ToastNotifier()
    notificatoer.show_toast("Reminder", f"""Alarm will go off in {seconds} Seconds, """, duration=20)
    notificator.show_toast(f"Reminder", reminder, duration=20)

    #alarm
    frequency=2500
    duration=1000
    winsound.Beep(frequency, duration)

if __name__=="__main__":
    words=input("What would you reminds of: ")
    sec=int(input("Enter seconds: "))
    timer(words,sec)