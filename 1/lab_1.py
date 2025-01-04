import os
import subprocess
import paramiko

import paramiko

# Укажите данные для подключения
hostname = '192.168.111.132'
port = 22  # стандартный порт SSH
username = 'vagrant'
password = 'vagrant'

# Создание SSH-клиента
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, port, username, password)

# Чтение файла с удаленного компьютер
sftp = client.open_sftp()
remote_file_path = '/homer/vagrant/config.txt'
with sftp.file(remote_file_path, 'r') as remote_file:
    file_content = remote_file.read().decode()
    doc_dir_path = file_content.split("\n")[0]
    sftp.open



sftp.close()
client.close()

print(file_content)