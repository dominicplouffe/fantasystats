"""
deploy.py

Usage:
    deploy.py --type=<type>

Example:
    trainer.py --type=general
    trainer.py --type=dev
"""

from fantasystats.tools import zip
from docopt import docopt
import paramiko
import boto3
import time
import os

BUILD_DIRS = [
    'fantasystats/scripts',
    'fantasystats/services',
    'fantasystats/api',
    'fantasystats/managers',
    'fantasystats/models',
    'fantasystats/tools',
    'fantasystats/database',
    'fantasystats/context.py',
    'fantasystats/__init__.py',
    'requirements.txt',

]
ZIP_FILENAME = 'fantasystats.zip'


def create_zip():
    if ZIP_FILENAME in os.listdir('.'):
        os.remove(ZIP_FILENAME)

    print('Packaging Files')
    utilities = zip.ZipUtilities()
    utilities.to_zip(BUILD_DIRS, ZIP_FILENAME)


def create_ssh_connection(public_ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        public_ip,
        username='ubuntu',
        key_filename='/Users/dplouffe/.ssh/admin-kp.pem'
    )

    return ssh


def copy_code(ssh):
    # print('Copying Code')
    # ssh.exec_command('./uz.sh')
    # time.sleep(5)
    # ssh.exec_command('sudo cp -r fantasystats /opt/fantasystats')
    # ssh.exec_command('sudo systemctl restart fantasystats')

    print('Copying Code')
    ssh.exec_command('unzip %s' % ZIP_FILENAME)
    ssh.exec_command('sudo cp -r fantasystats /opt/fantasystats')
    ssh.exec_command('sudo systemctl restart fantasystats')


def put_file(ssh):
    print('Uploading Zip File')
    ssh.exec_command('rm -r fantasystats')
    ssh.exec_command('rm %s' % ZIP_FILENAME)

    sftp = ssh.open_sftp()
    sftp.put('fantasystats.zip', 'fantasystats.zip')


def deploy(deploy_type):
    create_zip()

    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    for r in response['Reservations']:
        for i in r['Instances']:
            deploy_to_instance = False
            for t in i['Tags']:
                if t['Key'] == 'TYPE' and t['Value'].lower() == deploy_type.lower():
                    deploy_to_instance = True
                    break

            if deploy_to_instance:
                print('Deploying to %s' % i['PublicIpAddress'])
                ssh = create_ssh_connection(i['PublicIpAddress'])
                put_file(ssh)
                time.sleep(5.0)
                copy_code(ssh)


if __name__ == '__main__':
    args = docopt(__doc__)

    deploy_type = args['--type']

    deploy(deploy_type)
