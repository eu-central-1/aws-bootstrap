# -*- coding: utf-8 -*-

import os
from typing import Optional, Callable
import boto3
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils.predicate import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.request import Request
from ask_sdk_model.session_ended_request import SessionEndedRequest
from ask_sdk_model.response import Response
from ask_sdk_model.ui.simple_card import SimpleCard
from aws_lambda_powertools import Logger


logger = Logger(service=os.environ['POWERTOOLS_SERVICE_NAME'])

MY = {
    'en-US': 'a. w. s. demo',
    'de-DE': 'A. W. S. Demo'
}
DEFAULT_LOCALE = 'en-US'
AWS_SPELLOUT = '<say-as interpret-as="spell-out">AWS</say-as>'
FACTS = {
    'en-US': 'Your {} cloud stacks have following status: '.format(AWS_SPELLOUT),
    'de-DE': 'Deine {} <lang xml:lang="en-US">cloud stacks</lang> haben folgenden Status: '.format(AWS_SPELLOUT)
}
NODATA = {
    'en-US': 'Currently, you don\'t have any {} cloud stacks.'.format(AWS_SPELLOUT),
    'de-DE': 'Du hast momentan keine {} <lang xml:lang="en-US">cloud stacks</lang>.'.format(AWS_SPELLOUT)
}
EXCEPTION = {
    'en-US': 'Sorry there was a problem. I can\'t help you with this.',
    'de-DE': 'Entschuldigung. Ich kann dir damit nicht helfen.'
}
REPROMPT = {
    'en-US': 'How can I help you with {} ?'.format(AWS_SPELLOUT),
    'de-DE': 'Wie kann ich dir mit {} helfen?'.format(AWS_SPELLOUT)
}
STOP = {
    'en-US': 'Goodbye.',
    'de-DE': 'Und tschüss.'
}
HELP = {
    'en-US': 'You can ask me, what is status of your {} cloud stacks... {}'.format(AWS_SPELLOUT, REPROMPT['en-US']),
    'de-DE': ('Du kannst mich fragen wie der Status deiner {} '
              '<lang xml:lang="en-US">cloud stacks</lang> ist... {}').format(AWS_SPELLOUT, REPROMPT['de-DE'])
}

# @logger.inject_lambda_context
sb = SkillBuilder()


# TODO: Uncomment the following lines of code for request logs
@sb.global_request_interceptor()
def request_logger(handler_input: HandlerInput):
    print("Request received: {}".format(handler_input.request_envelope.request))


# TODO: Uncomment the following lines of code for response logs
@sb.global_response_interceptor()
def response_logger(handler_input: HandlerInput, response: Response):
    print("Response generated: {}".format(response))


def get_speech_and_card(locale: str):
    ec2 = boto3.client('ec2')
    logger.debug("At Describe Regions")
    regions = ec2.describe_regions()['Regions']
    data = []
    counters = {}
    for region in regions:
        logger.debug("At Init Cloudformation")
        client = boto3.client('cloudformation', region_name=region['RegionName'])
        logger.debug("At Start Cloudformation")
        stacks = client.list_stacks()['StackSummaries']
        logger.debug("At Listed Stacks")
        for i in stacks:
            if i['StackStatus'] == 'DELETE_COMPLETE':
                continue
            if region['RegionName'] not in counters:
                geo, loc, number = region['RegionName'].split('-')
                data.append('In Region {}<lang xml:lang="en-US">{}</lang> {}:'.format(geo.upper(), loc, number))
                counters[region['RegionName']] = 0
            counters[region['RegionName']] = counters[region['RegionName']] = 1
            status = i['StackStatus'].lower().replace('_', ' ')
            data.append('Stack {} ist im Status <lang xml:lang="en-US">{}</lang>.'.format(i['StackName'], status))
    logger.debug("At Data collected")
    return [FACTS[locale] + " ".join(data) if data else NODATA[locale], "\n".join(data)]


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input: HandlerInput):
    logger.info("In LaunchRequestHandler")
    request: Optional[Request] = handler_input.request_envelope.request
    locale = request.locale if request and request.locale else DEFAULT_LOCALE
    result = get_speech_and_card(locale)
    logger.info("In LaunchRequestHandler Build")
    handler_input.response_builder.speak(result[0]) \
        .set_card(SimpleCard(MY[locale], result[1])) \
        .set_should_end_session(False)
    logger.info("In LaunchRequestHandler Respond")
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("GetNewFactHandler"))
def get_new_fact_handler(handler_input: HandlerInput):
    logger.info("In GetNewFactHandler")
    request: Optional[Request] = handler_input.request_envelope.request
    locale = request.locale if request and request.locale else DEFAULT_LOCALE
    result = get_speech_and_card(locale)
    logger.info("In GetNewFactHandler Build")
    handler_input.response_builder.speak(result[0]) \
        .set_card(SimpleCard(MY[locale], result[1])) \
        .set_should_end_session(True)
    logger.info("In GetNewFactHandler Respond")
    return handler_input.response_builder.response


# Built-in Intent Handlers
@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input: HandlerInput):
    logger.info("In HelpIntentHandler")
    request: Optional[Request] = handler_input.request_envelope.request
    locale = request.locale if request and request.locale else DEFAULT_LOCALE
    handler_input.response_builder.speak(HELP[locale]) \
        .ask(REPROMPT[locale]) \
        .set_card(SimpleCard(MY[locale], HELP[locale]))
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input: HandlerInput):
    logger.info("In SessionEndedRequestHandler")
    request: Optional[SessionEndedRequest] = handler_input.request_envelope.request  # type: ignore [no-redef]
    reason = "Request is None" if (request is None) else request.reason
    logger.info("Session ended reason: {}".format(reason))
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input: HandlerInput, exception: Exception):
    logger.info("In CatchAllExceptionHandler")
    request: Optional[Request] = handler_input.request_envelope.request
    locale = request.locale if request and request.locale else DEFAULT_LOCALE
    logger.error(exception, exc_info=True)
    handler_input.response_builder.speak(EXCEPTION[locale]).ask(REPROMPT[locale])
    return handler_input.response_builder.response


can_handle_cancel_and_stop_intent: Callable[[HandlerInput], bool] = lambda handler_input: \
                    is_intent_name("AMAZON.CancelIntent")(handler_input) \
                    or is_intent_name("AMAZON.StopIntent")(handler_input)


@sb.request_handler(can_handle_func=can_handle_cancel_and_stop_intent)
def cancel_and_stop_intent_handler(handler_input: HandlerInput):
    logger.info("In CancelOrStopIntentHandler")
    request: Optional[Request] = handler_input.request_envelope.request
    locale = request.locale if request and request.locale else DEFAULT_LOCALE
    handler_input.response_builder.speak(STOP[locale])
    return handler_input.response_builder.response


handler = sb.lambda_handler()
