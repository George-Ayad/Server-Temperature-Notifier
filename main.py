#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Progressio Solutions - George Gabra Jr."
__version__ = "0.1.0"
__license__ = "GPL"

import os.path
import logzero
import logging
from logzero import logger
from hwmon import Hwmon
import json
import urllib.request
import smtplib
import ssl

threshold = 20


def main():
    # open Log file
    logzero.loglevel(logging.INFO)
    if not os.path.exists('./logfile.log'):
        file = open("logfile.log", "w")
        file.close()

    logzero.logfile("logfile.log")

    # Get current sensor data
    sensors = Hwmon.HW()

    # Log sensor data
    logger.info(sensors.data()["coretemp"])

    # Get average temperature
    temp = 0
    corecount = 0
    for i in sensors.data()["coretemp"]:
        if i.startswith("Core"):
            temp += float(sensors.data()["coretemp"][i].split()[0])
            corecount += 1
    temp = temp / corecount

    # Check temperature threshold
    if temp > threshold:
        logger.error("Temperature Average Higher Than Threshold !!")
        logger.error("average temperature = " + str(temp) + " > Threshold temperature (" + str(threshold) + ")")

        # Send notification to IOT remote
        logger.error("Sending notification to IOT remote")

        try:
            IOTUrl = urllib.request.urlopen("AC-REMOTE.local/ON")
            if IOTUrl.getcode() == 200:
                logger.info("Called IOT device successfully")
            else:
                logger.error("Could not send notification to IOT Device : Response code = " + str(IOTUrl.getcode()))
        except Exception as e:
            # If an error occurs, log it
            logger.error("Could not send notification to IOT Device :  " + str(e))

        # Send notification email to employees
        logger.error("Sending E-mail notification to employees")

        # Get mail server configuration
        with open('mail_setup.json') as f:
            data = json.load(f)

        smtp_server = data["smtp_server"]
        port = int(data["port"])  # For starttls
        sender_email = data["sender_email"]
        password = data["password"]
        receiver_email = data["receiver_email"]

        # Set message
        message = """
        WARNING !!
        Server core temperature Average Higher Than Threshold !!
        average temperature = """ + str(temp) + " > Threshold temperature (" + str(threshold) + ")"

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send email
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            try:
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
            except Exception as e:
                # If an error occurs, log it
                logger.error("Could not send email notification :  " + str(e))
            finally:
                server.quit()


if __name__ == "__main__":
    main()
