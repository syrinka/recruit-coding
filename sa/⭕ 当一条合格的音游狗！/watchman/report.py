import smtplib
from urllib import request
from email.mime.text import MIMEText
from email.header import Header

from .config import config
from .log import logger


def report(msg: str):
    conf = config['report']

    if conf['email'].get('enable'):
        report_email(msg)
    if conf['webhook'].get('enable'):
        report_webhook(msg)


def report_email(msg: str):
    conf = config['report']['email']

    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header('server', 'utf-8')
    message['To'] =  Header('maint', 'utf-8')
    message['Subject'] = Header('服务器告警', 'utf-8')

    try:
        smtp = smtplib.SMTP()
        smtp.connect(conf['host'], 25)
        smtp.login(conf['user'], conf['pass'])
    except smtplib.SMTPException:
        logger.warning('Failed to connect SMTP, abort email report')
        return

    for target in conf['targets']:
        try:
            smtp.sendmail(
                conf['sender'],
                target['receiver'],
                message.as_string()
            )
        except Exception:
            logger.warning(f'Error sending email to {target["receiver"]}')


def report_webhook(msg: str):
    conf = config['report']['webhook']
    
    for target in conf['targets']:
        body = target['template'].replace(
            target['placeholder'], msg
        )
        try:
            req = request.request(
                target['endpoint'],
                body,
                target['headers']
            )
            request.urlopen(req)
        except Exception:
            logger.warning(f'Error triggering webhook to {target["endpoint"]}')
