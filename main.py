import re
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField
from flask import Flask, render_template, request, session
# from postgres.db import create_connection

app = Flask(__name__)
app.secret_key = 'AB'
# conn = create_connection()

invalid_counts = {
    'ipv4': 0,
    'subnet': 0,
    'gateway': 0
}


@app.route('/', methods=['GET', 'POST'])

def user_input():
    result = {}
    disable_submit = False
    remaining_time = 0

    # Check the invalid submission count for each input
    total_invalid_count = sum(invalid_counts.values())
    if total_invalid_count >= 5:
        disable_submit = True
        disable_time = session.get('disable_time')
        if disable_time:
            remaining_time = max(0, (disable_time - datetime.now()).seconds // 60)
        else:
            remaining_time = 0

    if request.method == 'POST':
        ipv4 = request.form.get('ipv4')
        subnet = request.form.get('subnet')
        gateway = request.form.get('gateway_ipv4')

        if not validate_ipv4(ipv4):
            invalid_counts['ipv4'] += 1
            if total_invalid_count >= 5:
                disable_submit = True
                disable_time = datetime.now() + timedelta(minutes=5)
                session['disable_time'] = disable_time
                remaining_time = 5
            return render_template('form.html', ipv4_error="Invalid IPv4 address", subnet=subnet, gateway=gateway, result=result,
                                disable_submit=disable_submit, remaining_time=remaining_time)

        if not validate_subnet(subnet):
            invalid_counts['subnet'] += 1
            if total_invalid_count >= 5:
                disable_submit = True
                disable_time = datetime.now() + timedelta(minutes=5)
                session['disable_time'] = disable_time
                remaining_time = 5
            return render_template('form.html', subnet_error="Invalid subnet", ipv4=ipv4, gateway=gateway, result=result,
                                disable_submit=disable_submit, remaining_time=remaining_time)

        if not validate_gateway(gateway):
            invalid_counts['gateway'] += 1
            if total_invalid_count >= 5:
                disable_submit = True
                disable_time = datetime.now() + timedelta(minutes=5)
                session['disable_time'] = disable_time
                remaining_time = 5
            return render_template('form.html', gateway_error="Invalid gateway", ipv4=ipv4, subnet=subnet, result=result,
                                disable_submit=disable_submit, remaining_time=remaining_time)

        # Reset the invalid submission counts and disable time if the input is valid
        invalid_counts['ipv4'] = 0
        invalid_counts['subnet'] = 0
        invalid_counts['gateway'] = 0
        session.pop('disable_time', None)

        # Rest of the code for processing valid input...
        result = {
            'ipv4': ipv4,
            'subnet': subnet,
            'gateway': gateway
        }

    return render_template('form.html', result=result, disable_submit=disable_submit, remaining_time=remaining_time)

def validate_ipv4(ipv4):
    # Regular expression pattern to match IPv4 address without white spaces
    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/32$'

    # Check if the input matches the pattern and has valid length
    if re.match(pattern, ipv4) and len(ipv4) <= 18:
        # Split the address and CIDR prefix
        address, cidr = ipv4.split('/')

        # Validate each octet
        octets = address.split('.')
        for octet in octets:
            if not octet.isdigit() or int(octet) < 0 or int(octet) > 255:
                return False

        # Validate the CIDR prefix
        if not cidr.isdigit() or int(cidr) != 32:
            return False

        # Passed all validations
        return True

    # Failed to match the pattern or exceeded max length
    return False

#255.255.255.255 15 max characters allowed
def validate_subnet(subnet):
    # Regular expression pattern to match subnet address
    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'

    # Check if the input matches the pattern and has valid length
    if re.match(pattern, subnet) and len(subnet) <= 15:
        # Validate each octet
        octets = subnet.split('.')
        for octet in octets:
            if not octet.isdigit() or int(octet) < 0 or int(octet) > 255:
                return False

        # Passed all validations
        return True

    # Failed to match the pattern or exceeded max length
    return False

#192.168.100.1 13 max characters allowed
def validate_gateway(gateway):
    # Regular expression pattern to match gateway address
    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.1$'

    # Check if the input matches the pattern and has valid length
    if re.match(pattern, gateway) and len(gateway) <= 13:
        # Validate each octet
        octets = gateway.split('.')
        for octet in octets:
            if not octet.isdigit() or int(octet) < 0 or int(octet) > 255:
                return False

        # Passed all validations
        return True

    # Failed to match the pattern or exceeded max length
    return False


#if __name__ == '__main__':
    #app.run(debug=False)
