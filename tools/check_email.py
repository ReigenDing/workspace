#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Vin on 2017/10/25
import os
import email
import imaplib

IMAP = 'imap.163.com'
ACCOUNT = 'a54959@163.com'
PASSWORD = '45Qq6y9zwB3G487j'


def save_file(file_name, data, save_path=''):
    file_path = os.path.join(save_path, file_name)
    with open(file_path, 'wb') as fp:
        fp.write(data)
    return file_path


class Message(dict):
    """邮件内容存储格式"""


class Email(object):
    All, Unseen, Seen, Recent, Answered, Flagged = "All,Unseen,Seen,Recent,Answered,Flagged".split(',')

    def __init__(self, imap, account, password, file_save_path=''):
        if imap and account and password:
            self.host = imap
            self.account = account
            self.password = password
            self.save_path = file_save_path
            self.imap_server = self.login()

    def login(self):
        imap_server = imaplib.IMAP4_SSL(self.host)
        imap_server.login(self.account, self.password)
        return imap_server

    def get_newest(self):
        for msg_data in self.check_email(message_type=self.Unseen):
            print(u"邮件主题：{subject}\n邮件日期：{date}\n附件列表：{files}\n邮件正文：{content}".format(
                subject=msg_data.get('subject'),
                date=msg_data.get('date'),
                files=msg_data.get('files'),
                content=msg_data.get('content')
            ))

    def get_messages(self, message_type='Unseen', count=1):
        for msg_data in self.check_email(last_message=False, message_type=message_type, count=count):
            print(u"邮件主题：{subject}\n邮件日期：{date}\n附件列表：{files}\n邮件正文：{content}".format(
                subject=msg_data.get('subject'),
                date=msg_data.get('date'),
                files=msg_data.get('files'),
                content=msg_data.get('content')
            ))
            print '\n'

    def check_email(self, last_message=True, message_type="Unseen", count=1):
        """Message statues in ['All', 'Unseen', 'Seen', 'Recent', 'Answered', 'Flagged']
        :param last_message 返回收信箱最新的（最后一封）邮件， 默认为 True,
        :param message_type 检索邮件类型，默认为 Unseen（未读）邮件,
        :param count        检出的邮件消息数目 默认为 1
        :return Iteration
        """
        # 选中收信箱
        select_status, info = self.imap_server.select(mailbox='INBOX')
        if select_status != 'OK':
            print(info)
            raise StopIteration
        # 选择邮件类型
        search_status, items = self.imap_server.search(None, message_type)
        if search_status != 'OK':
            print(items)
            raise StopIteration
        message_list = items[0].split()[-1:] if last_message else items[0].split()[:count]
        print(u"读取 {0} 类型邮件，共有 {1} 封邮件, 读取 {2} 封".format(message_type, len(items[0].split()), len(message_list)))
        for message_index in message_list:
            msg_data = Message()
            fetch_status, message = self.imap_server.fetch(message_index, "(RFC822)")
            msg = email.message_from_string(message[0][1])
            # 消息日期
            msg_data['date'] = msg["Date"]
            # 消息主题
            message_subject = email.Header.decode_header(msg["Subject"])
            msg_data['subject'] = self.str_to_unicode(message_subject[0][0], message_subject[0][1])
            # 消息正文, 正文类型, 消息附件
            msg_data.update(self.parse_message(msg, save_path=self.save_path))
            yield msg_data

    @staticmethod
    def str_to_unicode(s, encoding=None):
        return unicode(s, encoding) if encoding else unicode(s)

    @staticmethod
    def parse_message(msg, save_path=''):
        message_content, content_type, suffix = None, None, None
        files = []
        for part in msg.walk():
            if not part.is_multipart():
                content_type = part.get_content_type()
                filename = part.get_filename()
                # 是否有附件
                if filename:
                    file_header = email.Header.Header(filename)
                    decode_header = email.Header.decode_header(file_header)
                    file_name = decode_header[0][0]
                    data = part.get_payload(decode=True)
                    print('Attachment : ' + file_name)
                    # 保存附件
                    if file_name:
                        save_file(file_name, data, save_path)
                        files.append(file_name)
                else:
                    if content_type in ['text/plain']:
                        suffix = '.txt'
                    if content_type in ['text/html']:
                        suffix = '.htm'
                    if part.get_charsets() is None:
                        message_content = part.get_payload(decode=True)
                    else:
                        message_content = part.get_payload(decode=True).decode(part.get_charsets()[0])
        msg_data = {
            'content': message_content,
            'type': suffix,
            'files': files
        }
        return msg_data


if __name__ == '__main__':
    email_163 = Email(imap=IMAP, account=ACCOUNT, password=PASSWORD)
    email_163.get_messages(message_type="Unseen", count=2)
