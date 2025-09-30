# 1、导⼊模块
import paramiko
import time
from pysnmp.hlapi import *

# 2、定义交换机信息
ip = '192.168.56.100'
username = 'python'
password = 'Huawei12#$'

# 3、SSH登陆设备
ssh = paramiko.client.SSHClient()
ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
ssh.connect(hostname=ip, port=22, username=username, password=password)
print(ip + ' login succesfully')

# 4、打开⼀个channel，输⼊配置
cli = ssh.invoke_shell()
cli.send('N\n')
time.sleep(0.5)
cli.send('screen-length 0 temporary\n')
time.sleep(0.5)

# 5、进⼊系统视图
cli.send('system-view immediately\n')
time.sleep(0.5)

# 6、逐⾏读取本地同⼀个⽂件夹⾥的snmp.txt，写⼊SSH通道
with open('snmp.txt', 'r') as f:  # 使用with自动管理文件资源
    snmp_config_list = f.readlines()
    for i in snmp_config_list:
        cli.send(i.strip() + '\n')  # 去除行尾换行并显式添加换行符
        time.sleep(0.5)

# 7、建立SNMP的通道
transport = UdpTransportTarget((ip, 161))  # 修正变量命名，避免无效代码行

# 8、通过pySNP获取设备的主机名
g = getCmd(
    SnmpEngine(),
    UsmUserData(
        'admin',
        'Huawei@123',
        'Huawei@123',
        authProtocol=usmHMACSHAAuthProtocol,
        privProtocol=usmAesCfb128Protocol
    ),
    transport,  # 引用已创建的transport对象
    ContextData(),
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0))
)

errorIndication, errorStatus, errorIndex, varBinds = next(g)
for i in varBinds:
    print(i)
    # 改进值提取逻辑，兼容不同OID格式
    print(str(i).split('=')[-1].strip().strip('"'))

# 9、最大接收返回信息
dis_this = cli.recv(999999).decode()
print(dis_this)

# 关闭会话
ssh.close()
