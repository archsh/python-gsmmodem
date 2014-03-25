#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""\
Demo: handle incoming SMS messages by replying to them

Simple demo app that listens for incoming SMS messages, displays the sender's number
and the messages, then replies to the SMS by saying "thank you"
"""

from __future__ import print_function
import sys, datetime
import logging
sys.path.append('..')

PORT = 'COM4'
BAUDRATE = 9600
PIN = None  # SIM card PIN (if any)

from gsmmodem.modem import GsmModem


def handleSms(sms):
    print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(sms.number, sms.time, sms.text))
    print('Replying to SMS...')
    sms.reply(u'SMS received: "{0}{1}"'.format(sms.text[:20], '...' if len(sms.text) > 20 else ''))
    print('SMS sent.\n')


def main():
    print('[%s] Initializing modem...' % datetime.datetime.now())
    # Uncomment the following line to see what the modem is doing:
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.smsTextMode = False
    modem.connect(PIN)
    print('[%s] Initialized modem!' % datetime.datetime.now())
    print('[%s] Sending Message...' % datetime.datetime.now())
    modem.sendSms('18926025825', u'尊敬的用户，您好！欢饮使用KKBEAR！%s ' % datetime.datetime.now())
    print('[%s] Waiting for SMS message...' % datetime.datetime.now())
    try:
        modem.rxThread.join(2 ** 31)
        # Specify a (huge) timeout so that it essentially blocks indefinitely,
        # but still receives CTRL+C interrupt signal
    finally:
        modem.close()


if __name__ == '__main__':
    main()
