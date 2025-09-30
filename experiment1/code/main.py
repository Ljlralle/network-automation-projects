import telnetlib
import time

host = '192.168.56.100'
Username = "python"
password = 'Huawei12#$'

tn = telnetlib.Telnet(host)
tn.read_until(b"Username:")
tn.write(Username.encode('ascii') + b"\n")
tn.read_until(b"Password:")
tn.write(password.encode('ascii') + b"\n") # 使用write()向设备输入命令
tn.write(b"n\n")
tn.write(b"screen-length 0 temporary\n")
tn.write(b'display cu int vlanif 1 \n')
time.sleep(1)
print(tn.read_very_eager().decode('ascii'))
tn.close()