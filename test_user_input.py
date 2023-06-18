'''
Shinwuu
Date 06/17/2023

Summary:
This code is to help learn the Jenkins CI/CD Pipeline
Unit Tests are extremely important in the SSDLC

'''

from datetime import datetime, timedelta
from flask import Flask
from flask.testing import FlaskClient

from main import app, validate_ipv4, validate_subnet, validate_gateway

'''
def client() -> FlaskClient:
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

def test_user_input_valid(client):
    response = client.post('/', data={
        'ipv4': '192.168.0.1/32',
        'subnet': '255.255.255.0',
        'gateway_ipv4': '192.168.0.1'
    })
    assert response.status_code == 200
    # Add assertions for expected behavior with valid input

def test_user_input_invalid_ipv4(client):
    response = client.post('/', data={
        'ipv4': 'invalid_ipv4',
        'subnet': '255.255.255.0',
        'gateway_ipv4': '192.168.0.1'
    })
    assert response.status_code == 200
    # Add assertions for expected behavior with invalid IPv4 address

def test_user_input_invalid_subnet(client):
    response = client.post('/', data={
        'ipv4': '192.168.0.1/32',
        'subnet': 'invalid_subnet',
        'gateway_ipv4': '192.168.0.1'
    })
    assert response.status_code == 200
    # Add assertions for expected behavior with invalid subnet

def test_user_input_invalid_gateway(client):
    response = client.post('/', data={
        'ipv4': '192.168.0.1/32',
        'subnet': '255.255.255.0',
        'gateway_ipv4': 'invalid_gateway'
    })
    assert response.status_code == 200
    # Add assertions for expected behavior with invalid gateway
'''

def test_validate_ipv4():
    assert validate_ipv4('192.168.0.1/32') is True
    assert validate_ipv4('invalid_ipv4') is False
    # Add more test cases for validate_ipv4

def test_validate_subnet():
    assert validate_subnet('255.255.255.0') is True
    assert validate_subnet('invalid_subnet') is False
    # Add more test cases for validate_subnet

def test_validate_gateway():
    assert validate_gateway('192.168.0.1') is True
    assert validate_gateway('invalid_gateway') is False
    # Add more test cases for validate_gateway
