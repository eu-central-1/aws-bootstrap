# -*- coding: utf-8 -*-

import logging
import boto3
import botocore

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

MY = 'a. w. s. cloud stacks'
FACTS = 'Deine AWS <lang xml:lang="en-US">cloud stacks</lang> haben folgenden Status: '
NODATA = 'Du hast momentan keine AWS <lang xml:lang="en-US">cloud stacks</lang>.'
EXCEPTION = 'Entschuldigung. Ich kann dir damit nicht helfen.'
HELP = 'Du kannst mich fragen wie der Status deiner AWS <lang xml:lang="en-US">cloud stacks</lang> ist... Was kann ich für dich tun?'
FALLBACK = '{} {}'.format(EXCEPTION, HELP)
REPROMPT = 'Wie kann ich dir helfen?'
STOP = 'Und tschüss.'

sb = SkillBuilder()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# TODO: Uncomment the following lines of code for request logs
@sb.global_request_interceptor()
def request_logger(handler_input):
    print("Request received: {}".format(handler_input.request_envelope.request))

# TODO: Uncomment the following lines of code for response logs
@sb.global_response_interceptor()
def response_logger(handler_input, response):
    print("Response generated: {}".format(response))

def getSpeechAndCard():
    ec2 = boto3.client('ec2')
    log.debug("At Describe Regions")
    regions = ec2.describe_regions()['Regions']
    data = []
    counters = {}
    for region in regions:
        log.debug("At Init Cloudformation")
        client = boto3.client('cloudformation', region_name=region['RegionName'])
        log.debug("At Start Cloudformation")
        stacks = client.list_stacks()['StackSummaries']
        log.debug("At Listed Stacks")
        for i in stacks:
            if i['StackStatus'] == 'DELETE_COMPLETE':
                continue
            if region['RegionName'] not in counters:
                geo,loc,number = region['RegionName'].split('-')
                data.append('In Region {}<lang xml:lang="en-US">{}</lang> {}:'.format(geo.upper(),loc,number))
                counters[region['RegionName']] = 0
            counters[region['RegionName']] = counters[region['RegionName']] = 1
            status = i['StackStatus'].lower().replace('_', ' ')
            data.append('Stack {} ist im Status <lang xml:lang="en-US">{}</lang>.'.format(i['StackName'],status))
    log.debug("At Data collected")
    return [ FACTS + " ".join(data) if data else NODATA, "\n".join(data) ]

@sb.request_handler(can_handle_func=is_intent_name("LaunchRequest"))
def launch_request_handler(handler_input):
    log.info("In LaunchRequestHandler")
    result = getSpeechAndCard()
    log.info("In LaunchRequestHandler Build")
    handler_input.response_builder.speak(result[0]) \
        .set_card(SimpleCard(MY, result[1])) \
        .set_should_end_session(False)
    log.info("In LaunchRequestHandler Respond")
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("GetNewFactHandler"))
def get_new_fact_handler(handler_input):
    log.info("In GetNewFactHandler")
    result = getSpeechAndCard()
    log.info("In GetNewFactHandler Build")
    handler_input.response_builder.speak(result[0]) \
        .set_card(SimpleCard(MY, result[1])) \
        .set_should_end_session(True)
    log.info("In GetNewFactHandler Respond")
    return handler_input.response_builder.response

# Built-in Intent Handlers
@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    log.info("In HelpIntentHandler")
    handler_input.response_builder.speak(HELP).ask(REPROMPT).set_card(SimpleCard(MY, HELP))
    return handler_input.response_builder.response

@sb.request_handler(
    can_handle_func=lambda handler_input : is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    log.info("In CancelOrStopIntentHandler")
    handler_input.response_builder.speak(STOP)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    log.info("In SessionEndedRequestHandler")
    log.info("Session ended reason: {}".format(handler_input.request_envelope.request.reason))
    return handler_input.response_builder.response

@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    log.info("In CatchAllExceptionHandler")
    log.error(exception, exc_info=True)
    handler_input.response_builder.speak(EXCEPTION).ask(REPROMPT)
    return handler_input.response_builder.response

handler = sb.lambda_handler()