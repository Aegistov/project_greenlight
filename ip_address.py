import subprocess

def display():
    if_result = str(subprocess.check_output(['ifconfig', 'wlan0']))
    if_sections = if_result.split(':')
    ip_address = if_sections[7].split(' ')[0]
    return(ip_address)
