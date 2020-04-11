import unittest

from aws_cdk import core
from aws_bootstrap_multiaccount.init_alexacloud_skill import AlexaConstruct

class TestAlexaConstruct(unittest.TestCase):

    def setUp(self):
        self.app = core.App()
        self.stack = core.Stack(self.app, "TestStack")

    def test_alexa_function(self):
        test_alexa_function = AlexaConstruct(self.stack, "Test1")
        assert test_alexa_function
