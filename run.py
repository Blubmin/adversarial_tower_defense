import argparse

from tower_defense import App
from mongo_wrapper import MongoWrapper

if __name__ == "__main__":
    MongoWrapper().clear_collections()
    theApp = App()
    theApp.on_execute()