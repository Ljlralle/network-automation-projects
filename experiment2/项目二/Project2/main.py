import paramiko
import time
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.56.100',port=22,username='python',password='Huawei12#$')
cli = ssh.invoke_shell()
cli.send('N\n')
time.sleep(1)
cli.send('system-view\n')
time.sleep(1)
cli.send('vlan 10\n')
time.sleep(2)
cli.send('quit\n')
time.sleep(1)
cli.send('int g1/0/1\n')
time.sleep(1)
cli.send('port link-type access\n')
time.sleep(1)
cli.send('port default vlan 10\n')
time.sleep(1)
cli.send('undo shutdown\n')
time.sleep(1)
cli.send('quit\n')
time.sleep(1)

cli.send('display vlan\n')
time.sleep(2)
dis_vlan = cli.recv(999999).decode()
print(dis_vlan)

time.sleep(3)

cli.send('display current-configuration interface g1/0/1\n')
time.sleep(2)

dis_g101 = cli.recv(999999).decode()
time.sleep(2)
print(dis_g101)

# 8、关闭 SSH 连接
ssh.close()