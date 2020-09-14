import pysftp
import time
from win10toast import ToastNotifier
import urllib.request
from paramiko import SSHClient

def run():
    try:
        host = "example.com"
        username = "root"
        password = "root"
        toast = ToastNotifier()

        ip = urllib.request.urlopen("https://checkip.amazonaws.com/").read().decode('utf-8').strip()

        last = open("file/last-ip.txt", "r")
        last = last.read()

        if last != ip:
            lastUpdate = open("file/last-ip.txt", "w")
            lastUpdate.write(ip)
            lastUpdate.close()

            config = open("file/example-site-sample.conf")
            config = config.read().replace("{{ip}}", ip)

            newConfig = open("file/example-site.conf", "w")
            newConfig.write(config)
            newConfig.close()

            srv = pysftp.Connection(host=host, username=username, password=password)
            with srv.cd('/etc/nginx/sites-available/'): 
                srv.put('file/example-site.conf') 
            srv.close()
            ssh = SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(host, username=username, password=password)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('service nginx restart')
            toast.show_toast("IP Updated!","home.example.com new ip: " + ip, duration=10)
            time.sleep(10)
    except:
        time.sleep(10)

while True:
    run()
