# -*- coding: utf-8 -*-

import smtplib
import pymongo
from scrapy.conf import settings
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from datetime import datetime, timedelta

class Utility(object):

    db = None
    client = None

    @staticmethod
    def init():
        print 'init Mongo Connection'
        Utility.client = pymongo.MongoClient(settings['MONGO_URI'])
        Utility.db = Utility.client[settings['MONGO_DATABASE']]

    @staticmethod
    def getDB():
        return Utility.db;

    @staticmethod
    def destruct():
        Utility.client.close()
       
    @staticmethod
    def sendMailToUser():
        querys = [
            {'$match': {
                'updated_time': {
                    '$gt': datetime.now() - timedelta(minutes=1)
                }
            }},
            {'$sort': { 'jpy': 1 }},
            { '$limit': 1 }
        ]
        cursor = Utility.db[settings['MONGO_COLLECTION']].aggregate(querys) 
        for doc in cursor:
            message = '%s:%s: JPY Currency %s' % (
                doc['name'], 
                doc['updated_time'].strftime("%Y-%m-%d %H:%M:%S"),
                doc['jpy']
            )
            Utility.send_mail(message, message)

    @staticmethod
    def send_mail(message, title):
        print message
        gmailUser = settings['GMAIL_USER']
        gmailPassword = settings['GMAIL_PASSWORD']

        msg = MIMEMultipart()
        msg['From'] = gmailUser
        msg['To'] = gmailUser
        msg['Subject'] = title
        msg.attach(MIMEText(message))

        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, gmailUser, msg.as_string())
        mailServer.close()
        print "Mail sent"
