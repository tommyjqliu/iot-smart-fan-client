import os
import pysher
from dotenv import load_dotenv

load_dotenv()

PUSHER_CLUSTER = os.getenv("PUSHER_CLUSTER")
PUSHER_KEY = os.getenv("PUSHER_KEY")

if not PUSHER_CLUSTER or not PUSHER_KEY:
    print("Please provide PUSHER_SECRET, PUSHER_CLUSTER, PUSHER_APP_ID, and PUSHER_KEY in .env file")
    exit(1)


pusher = pysher.Pusher(PUSHER_KEY, PUSHER_CLUSTER)