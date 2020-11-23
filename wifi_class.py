import paramiko
import pandas
import time

APRouter="192.168.101."
wifi_card="Wi-Fi"

class Window:
    
    ssh1=paramiko.SSHClient()
    ssh2=paramiko.SSHClient()

#### Instance attribute ######
    def __init__(self,hostname,ipaddress,password):
        self.ipaddress=ipaddress
        self.hostname=hostname
        self.password=password

##### Sshconnect method ######    
    def Sshconnect(self,sshserver,ssh):
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname="{}".format(sshserver.ipaddress), username="{}".format(sshserver.hostname), password="{}".format(sshserver.password))

####### PC Sendcommand method ####        
    def Sendcommand2remote(self,command,ssh):
        (stdin, stdout, stderr) = ssh.exec_command("{}".format(command)) ##### neu dat cac bien cung ten trong cac method khac nhau thi neu minh can truy cap tu object thi phan biet nhu the nao 
        time.sleep(3)
        self.lines = stdout.readlines()
        for line in self.lines:
            line=line.replace("\n","")
            line=line.strip()
            print(line)       
######## PC check Wifi-Connection method ### 
    def Check_connection(self,wirless_card,ssh):
        #(stdin ,stdout, stderr) = ssh.exec_command("netsh wlan disconnect interface=\"{}\"".format(wifi_card))
        (stdin, stdout, stderr) = ssh.exec_command("netsh interface ipv4 show addresses \"{}\"".format(wirless_card))
        lines = stdout.readlines()
        for line in lines:
            line=line.replace("\n","")
            line=line.strip()
            print(line)
            if APRouter in line:
                check_ip=True
            else:
                pass                
        try: 
            if check_ip==True:
                print("Connect successfully")
        except:
            print("Connect unsuccessfully")
            print("Try to connect again")

    def get_remote_info(self,cmd,ssh):
        self.Sendcommand2remote(cmd,ssh)
        for i in self.lines:
            if APRouter in i:
                i=i.replace("Address ","")
                i=i.replace(" Parameters","")
                remote_ip=i.strip()
        return remote_ip

###############################################        
    def ping_test(self,ping_cmd,ssh):
        self.Sendcommand2remote(ping_cmd,ssh)
        for ele in self.lines:
            if "Approximate" in ele:
                print("ping successful")
                rs="Fail"
            else:
                pass
        if rs!="Fail":
            rs="OK"
        else:
            pass
        return rs
print("SSH to local PC1: ")
PC1= Window("Kieu.nguyen","192.168.101.102","290294")

PC1.Sshconnect(PC1,PC1.ssh1)

print("Check Wi-Fi connection of PC1: ")
PC1.Check_connection(wifi_card,PC1.ssh1)

print("IP address of Wi-Fi PC1 is: ")

a=PC1.get_remote_info("netsh interface ipv4 show ipaddresses \"{}\"".format(wifi_card),PC1.ssh1)

print("dia chi: ")

print(a)

print("Ping to remote: ")

ping=PC1.ping_test("ping {}".format(a),PC1.ssh1)

print(ping)