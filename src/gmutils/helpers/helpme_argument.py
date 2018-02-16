#!/usr/bin/env python

from argparse import ArgumentParser

class Arguments():
    def __init__(self):
        self.parser = ArgumentParser()

        self.results = {}

    def load(self, **options):
        pass

    def addArgument(self, argument_name, group=None)
        pass