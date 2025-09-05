"""
Utility functions for formatting consistent JSON API responses.
Used across Flask route handlers to standardize output.
"""

from flask import jsonify
from http import HTTPStatus


def create_api_response(data: str, error: bool = False):
    payload = {"data": data, "error": error}
    return jsonify(payload)


def return_api_response(data: str, status_code: int):
    resp = create_api_response(data)
    resp.status_code = status_code
    return resp


def return_internal_error_response(data: str):
    resp = create_api_response(data, error=True)
    resp.status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    return resp
