def send_email(matches, addresses, subject):
    a = open(addresses, 'r')
    add = a.readlines()
    for address in add:
        body = generate_body(matches)
        service = create_service()
        test = CreateMessage('erickmartins@gmail.com', address,
            subject, '', body)
        # print(test)
        ret = SendMessage(service, 'me', test)
    return

def generate_body(matches):
    body = ''
    counter = 1
    for match in matches:
        match_list = match[0].split(',')
        body = body + str(counter) + ') '
        body = body + match_list[1]+' x '
        body = body + match_list[2]+' ('
        body = body + match_list[3]+'), '
        body = body + match_list[4]+' - '
        body = body + match_list[5] + '<br>\n'
        counter = counter + 1
    return body
"""Send an email message from the user's account.
"""

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors


def SendMessage(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        print(message)
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        # print('Message Id: %s' % message['id'])
        return message
    except(errors.HttpError):
        print('An error occurred: %s' % error)


def CreateMessage(sender, to, subject, message_text, message_html):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(message_text, 'plain'))
    msg.attach(MIMEText(message_html, 'html'))

    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body

   


def CreateMessageWithAttachment(sender, to, subject, message_text, file_dir,
                                filename):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.
      file_dir: The directory containing the file to be attached.
      filename: The name of the file to be attached.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    path = os.path.join(file_dir, filename)
    content_type, encoding = mimetypes.guess_type(path)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(path, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(path, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(path, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(path, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()

    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def create_service():
    from oauth2client import file, client, tools
    from googleapiclient.discovery import build
    from httplib2 import Http


    SCOPES = 'https://www.googleapis.com/auth/gmail.send'

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service


if __name__ == '__main__':
    service = create_service()
    test = CreateMessage('erickmartins@gmail.com', 'erickmartins@gmail.com',
        'test', '','this is a test')
    print(test)
    ret = SendMessage(service, 'me', test)
    print(ret)