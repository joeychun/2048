import time

i = 0

def password():
    global i
    a = input("password:")
    if a == "i dont know":
        print("right")
    else:
        print("wrong")
        i += 1
        if i != 5:
            password()
        else:
            print("try after 1 min")
            time.sleep(60)
password()
