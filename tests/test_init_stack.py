import unittest

from aws_cdk import core
from aws_bootstrap.init_cloudstacks_skill import AlexaConstruct

class TestAlexaConstruct(unittest.TestCase):

    def setUp(self):
        self.app = core.App()
        self.stack = core.Stack(self.app, "teststack")

    def test_alexa_function(self):
        test_alexa_function = AlexaConstruct(self.stack, "testalexa")
        assert test_alexa_function
