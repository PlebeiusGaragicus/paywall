from queue import Queue

from .rapaygoSingleton import rapaygoSingleton


threading_message_queue = Queue()

rapaygo: rapaygoSingleton = None

DEBUG = False

SECRET_GAME_IS_RUNNING_FLAG = "--gameisrunning"

FREE_PLAY = False
