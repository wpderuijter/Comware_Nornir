from nornir import InitNornir
from nornir_netmiko import netmiko_send_command

nr = InitNornir()

pad = 'e:/hpe/zenuity/'
fuit = open(pad + 'checkAndy.txt', 'w')

#############################################################
# Check if andyj auth failures in log
#############################################################

fuit.write("Check andy\n\n")

result = nr.run(
    task=netmiko_send_command,
    command_string="display log | i andyj"
)

for elem in result:
    logentries = result[elem][0].result.split('\n')
    if len(logentries)>0:

        for idx in range(0,len(logentries)-1):
            if "Authentication failed" in logentries[idx]:
                fuit.write(elem + ":\n")
                fuit.write('  ' + logentries[idx] + '\n')
                break

#######
fuit.close()
