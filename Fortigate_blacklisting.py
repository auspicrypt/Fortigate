# Importing modules
import paramiko
import datetime
import sys

#IP address validation check
def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

# input no of IP address and IP address from user

print '********************************************'
print'Only 5 IP addresses can be entered at a time'
print '********************************************'
no_of_ip = int(input('Enter No. of IP addresses: '))
num = 0
IP = []
if no_of_ip < 6:
    while num < no_of_ip:
        ip_element = str(raw_input('Enter IP address:'))
        if validate_ip(ip_element) == True:
            IP.append(ip_element)
            num += 1
        else:
            print("Enter valid IP address")
            pass
else:
    sys.exit("Enter a value less than 6")

blacklist_file = open("blacklisted_IP.txt", "ab+")
for ip_elem in IP:
    blacklist_file.write(str(ip_elem) + ' was added on ' + str(datetime.date.today()) + '\n')
blacklist_file.close()

# add string "_blacklist" to each IP address
string = '_SIEM_blacklist'
IP = [x + string for x in IP]

# setting parameters like host IP, username, passwd
HOST = "a.b.c.d" #Your IP address here
USER = "User" # Your Username here
PASS = "####" #Your password here

client1 = paramiko.SSHClient()
# Add missing client key
client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# connect to switch
client1.connect(HOST, username=USER, password=PASS)
print "SSH connection to firewall %s established" % HOST
# Gather commands and read the output from stdout
for bl_ip_name in IP:
    bl_ip = bl_ip_name.strip('_SIEM_blacklist')
    stdin, stdout, stderr = client1.exec_command(
        'config firewall address\nedit "' + str(bl_ip_name) +'_'+str(datetime.date.today())+ '"\nset subnet ' + str(bl_ip) + ' 255.255.255.255'+'\nnext\nend')
    print 'firewall Object %s created..!!' %bl_ip
for bl_ip_name_02 in IP:
    stdin, stdout, stderr = client1.exec_command('config firewall addrgrp\nedit "Blacklisted_ip"\nappend member ' + str(bl_ip_name_02)+'_'+str(datetime.date.today())+ '\nend')
    bl_ip_02 = bl_ip_name_02.strip('_SIEM_blacklist')
    print 'IP address %s has been blacklisted' %bl_ip_02
client1.close()
print "Logged out of firewall %s" % HOST

try:
    input ('PRESS ANY KEY TO CONTINUE...... .')
except SyntaxError:
    print 'Its done!!'
