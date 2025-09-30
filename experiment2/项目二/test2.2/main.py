import paramiko
import time


def send_dis_cmd(ip, username, password, commands):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username=username, password=password, look_for_keys=False)
        print(f"SSH 已经登录 {ip}")
        cli = ssh.invoke_shell()
        cli.send('screen-length 0 temporary\n')
        for cmd in commands_S:
            cli.send(cmd + "\n")
            time.sleep(1)
        dis_cu = cli.recv(999999).decode()
        print(dis_cu)
        ssh.close()
    except paramiko.ssh_exception.AuthenticationException:
        print(f"\n\tUser authentication failed for {ip}.\n")


if __name__ == "__main__":
    commands_R = ['display version', 'display patch-information', 'display clock', 'display device', 'display health',
                  'display memory-usage', 'display logbuffer']
    commands_S = ['display version', 'display patch-information', 'display clock', 'display device',
                  'display cpu-usage configuration', 'display memory-usage', 'display logbuffer summary']
    devices = {
        'R, SZ1': '10.2.12.1',
        'R, SZ2': '10.2.12.2',
        'S, S4': '10.3.1.254',
        'S, S1': '10.1.4.252',
        'S, S2': '10.1.4.253'
    }
    username = "python"
    password = "Huawei12#$"

    for key in devices.keys():
        ip = devices[key]
        if key.startswith('R'):
            send_dis_cmd(ip, username, password, commands_R)
        else:
            send_dis_cmd(ip, username, password, commands_S)