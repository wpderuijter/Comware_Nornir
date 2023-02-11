from nornir import InitNornir
from nornir_netmiko import netmiko_send_command

nr = InitNornir()

invent = nr.inventory

nr.filter(functie='mgmt_acc').inventory.hosts.keys()

pad = 'e:/hpe/zenuity/'
fuit = open(pad + 'test.txt', 'w')

#############################################################
# Check Radius login
#############################################################

result = nr.run(
    task=netmiko_send_command,
    command_string="display log | i LOGIN:.wimr.logged.in"
)

for elem in result:
    logentries = result[elem][0].result.split('\n')
    fuit.write(elem + ":\n")
    fuit.write('  ' + logentries[-2] + '\n')
    fuit.write('  ' + logentries[-1] + '\n')
    fuit.write('#\n')

fuit.close()