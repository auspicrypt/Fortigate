# Importing modules
import paramiko
import datetime
import sys

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

print '*************************************'
print '     BLOCK IP ADDRESSES VIA LIST     '
print '*************************************'

while 1:
    try:
        path_of_file = raw_input('Enter filename with complete path:') #call for path of file to block IP addresses
        break
    except:
        print 'You have entered incorrect path or filename, please try again'
IP=[] #it will store valid IP addresses to block
with open(path_of_file) as f:
    content = f.readlines()
    content = [x.strip() for x in content]
    for value in content:
        if validate_ip(value) is True:
            IP.append(value)
        else:
            pass

#log the IP address just blocked
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

# Create address object
for bl_ip_name in IP:
    bl_ip = bl_ip_name.strip('_SIEM_blacklist')
    command1 = 'config firewall address \n edit "' + str(bl_ip_name) + '_' + str(datetime.date.today()) + '"\nset subnet ' + str(bl_ip) + ' 255.255.255.255' + '\nnext\nend'
    stdin, stdout, stderr = client1.exec_command(command1)
    print ('firewall Object %s created..!!' %bl_ip)

#Add addresses to address groups
for bl_ip_name_02 in IP:
    command2 = 'config firewall addrgrp \nedit "Blacklisted_ip" \nappend member ' + str(bl_ip_name_02) + '_' + str(datetime.date.today()) + '\nend'
    stdin, stdout, stderr = client1.exec_command(command2)
    # stdout = stdout.readlines()
    bl_ip_02 = bl_ip_name_02.strip('_SIEM_blacklist')
    print ('IP address %s has been added to blacklisted address group' %bl_ip_02)
    # print (str(stdout))
client1.close()
print "Logged out of firewall %s" % HOST
print 'Task completed'
raw_input('PRESS ANY KEY TO CONTINUE...... .')