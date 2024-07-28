import json

from pydantic import TypeAdapter

from app.autograder_request_bodies import InputOutputRequestBody, UnitTestRequestBody


def convert_input_output(submission: dict):
    return TypeAdapter(InputOutputRequestBody).validate_json(json.dumps(submission))


def convert_unit_test(submission: dict):
    return TypeAdapter(UnitTestRequestBody).validate_json(json.dumps(submission))
