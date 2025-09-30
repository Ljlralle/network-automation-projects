from netmiko import ConnectHandler
from pysnmp.hlapi import *

# 设备连接参数
device_info = {
    'device_type': 'huawei',
    'host': '192.168.56.100',
    'username': 'python',
    'password': 'Huawei12#$',
    'port': 22,
    'timeout': 30,
    'session_timeout': 30,
    'global_delay_factor': 3,
}

try:
    # 建立连接
    print(f"正在连接设备 {device_info['host']}...")
    net_connect = ConnectHandler(**device_info)
    print(f"成功连接到设备 {device_info['host']}")

    # 先获取设备提示符
    prompt = net_connect.find_prompt()
    print(f"设备提示符: {prompt}")

    # 进入系统视图
    print("进入系统视图...")
    net_connect.send_command_timing('system-view immediately')

    # 读取SNMP配置文件
    print("读取SNMP配置...")
    with open('snmp.txt', 'r') as f:
        snmp_commands = [cmd.strip() for cmd in f.readlines() if cmd.strip()]

    # 使用send_command_timing逐条发送命令（不等待特定模式）
    print("执行SNMP配置...")
    for cmd in snmp_commands:
        print(f"执行: {cmd}")
        output = net_connect.send_command_timing(cmd, delay_factor=2)
        if "Error:" in output or "error" in output.lower():
            print(f"警告: 命令执行可能有问题 - {output}")

    # 返回用户视图
    net_connect.send_command_timing('return')

    # 保存配置
    print("保存配置...")
    save_output = net_connect.send_command_timing('save')
    if 'Are you sure' in save_output or 'continue' in save_output:
        net_connect.send_command_timing('y')
    print("配置已保存")

    # SNMP查询部分
    print("开始SNMP查询...")
    ip = '192.168.56.100'

    g = getCmd(
        SnmpEngine(),
        UsmUserData(
            'admin',
            'Huawei@123',
            'Huawei@123',
            authProtocol=usmHMACSHAAuthProtocol,
            privProtocol=usmAesCfb128Protocol
        ),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(g)

    print("\n=== SNMP查询结果 ===")
    if errorIndication:
        print(f"SNMP错误: {errorIndication}")
    elif errorStatus:
        print(f"SNMP错误状态: {errorStatus} at {errorIndex}")
    else:
        for varBind in varBinds:
            print(f"原始输出: {varBind}")
            hostname = str(varBind).split('=')[-1].strip().strip('"')
            print(f"设备主机名: {hostname}")

    # 关闭连接
    net_connect.disconnect()
    print("连接已关闭")

except Exception as e:
    print(f"错误: {str(e)}")