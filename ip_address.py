import subprocess

def display():
    if_result = subprocess.check_output(['ifconfig', 'wlan0']).decode('utf-8')
    if_sections = if_result.split(':')
    ip_address = if_sections[7].split(' ')[0]
    print(ip_address)
    return(ip_address)
