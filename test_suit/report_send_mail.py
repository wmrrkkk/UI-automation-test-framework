import os
import time
import zipfile
import configparser
import unittest
from email.header import Header
from base_page.HTMLTestRunner import HTMLTestRunner
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys

sys.path.append("..\\")


# 从config.ini配置文件中读取相应配置信息
config_path = os.path.abspath(os.path.dirname(
    os.path.dirname(__file__))) + '/config.ini'
config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')
projectName = config.get('projectInfo', 'projectName')
tester = config.get('testInfo', 'tester')
smtpServer = config.get('testInfo', 'smtpServer')
mail_sender = config.get('testInfo', 'sender')
userName = config.get('testInfo', 'userName')
passWord = config.get('testInfo', 'passWord')
mail_receiver = config.get('testInfo', 'receiver')


# 邮件发送自动化测试报告
# file_new为生成的chtml测试报告文件，zip_report为包含测试报告及错误截图的zip文件
def send_mail(file_new, zip_report):

    # 将测试报告添加为邮件正文
    f = open(file_new, 'rb')
    mail_body = f.read()
    f.close()

    # 邮件服务器等信息配置
    smtpserver = 'mail.atwasoft.net'
    sender = mail_sender
    receivers = mail_receiver.split(',')
    username = userName
    password = passWord

    # 邮件主题设置
    msg = MIMEMultipart()
    text = MIMEText(mail_body, 'html', 'utf-8')
    text['Subject'] = Header(projectName + '自动化测试报告', 'utf-8')
    msg.attach(text)
    msg['Subject'] = Header(projectName + '自动化测试报告', 'utf-8')

    # 添加zip包到邮件附件
    report = MIMEApplication(open(zip_report, 'rb').read())
    report.add_header('Content-Disposition', 'attachment',
                      filename='自动化测试报告.zip')
    msg.attach(report)

    # 发件人、收件人信息配置
    msg['from'] = sender
    msg['to'] = ','.join(receivers)

    # 发送邮件
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(msg['from'], receivers, msg.as_string())
    smtp.quit()
    print('Send mail success!')


# 获取最新的测试报告
def new_report(testreport):
    dirs = os.listdir(testreport)
    dirs.sort()
    newReportName = dirs[-1]
    print('Newest report name {0}'.format(newReportName))
    file_new = os.path.join(testreport, newReportName)
    return file_new


if __name__ == '__main__':

    # 测试用例路径、测试报告路径、测试报告路径下文件目录
    test_dir = os.path.abspath(os.path.dirname(
        os.path.dirname(__file__))) + '\\testcase\\'
    report_dir = os.path.abspath(os.path.dirname(
        os.path.dirname(__file__))) + '\\test_report\\'
    file_list = os.listdir(report_dir)

    # 清空测试报告目录
    for filename in file_list:
        file_path = os.path.join(report_dir, filename)
        os.remove(file_path)

    # 执行测试，生成html测试报告文件
    discover = unittest.defaultTestLoader.discover(
        test_dir, pattern='test*.py')
    now = time.strftime("%Y%m%d-%H%M%S")
    fileName = 'test_report' + now + '.html'
    fp = open('../test_report/' + fileName, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title=projectName + u'自动化测试报告',
                            description=u'自动化测试用例执行情况，错误截图等详细信息请下载附件解压后查看。',
                            tester=tester)
    runner.run(discover)
    fp.close()

    # 生成zip文件
    zip_name = os.path.abspath(os.path.dirname(
        os.path.dirname(__file__))) + '\\report_backup\\' + now + '.zip'
    zip_file = zipfile.ZipFile(zip_name, 'w')
    file_list = os.listdir(report_dir)
    for filename in file_list:
        zip_file.write(report_dir + filename, filename)
    zip_file.close()

    # 获取最新html测试报告文件名，发送测试报告
    new_report = new_report(report_dir)
    send_mail(new_report, zip_name)
