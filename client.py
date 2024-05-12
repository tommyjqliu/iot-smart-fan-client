
# import machineid
from fan import Fan
from pusher import pusher
import RPi.GPIO as GPIO

# MACHINE_ID = machineid.hashed_id()

def main():

    print(MACHINE_ID)
    fan = Fan(MACHINE_ID)
    pusher.connection.bind('pusher:connection_established', lambda data: pusher.subscribe('my-channel').bind('my-event', fan.message_handler))
    pusher.connect()

    while True:
        pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting program...")
        GPIO.cleanup()
        pass