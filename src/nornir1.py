from nornir import InitNornir
from nornir_netmiko import netmiko_send_command

nr = InitNornir()

pad = 'e:/hpe/zenuity/'
fuit = open(pad + 'uitvoer.txt', 'w')

#################################################################################
#  Check IRF only for MDS, use that info to also display a list of all switches
#################################################################################

result = nr.run(
    task=netmiko_send_command,
    command_string="display irf"
)

fuit.write("This test script involves the following switches:\n\n")

for elem in result:
    swName = elem.lower()
    fuit.write(' o  ' + swName + '\n')

fuit.write("\n\n")

fuit.write("IRF\n\n")

for elem in result:
    logentries = result[elem][0].result.split('\n')
    if "MDS" in elem.upper():
        fuit.write(elem + ":\n")
        for entry in logentries:
            fuit.write('  ' + entry + '\n')
        fuit.write('#\n')

#############################################################
# Check Radius login
#############################################################

fuit.write("Radius\n\n")

result = nr.run(
    task=netmiko_send_command,
    command_string="display log | i LOGIN:.wimr.logged.in"
)

for elem in result:
    logentries = result[elem][0].result.split('\n')
    fuit.write(elem + ":\n")
    fuit.write('  ' + logentries[-1] + '\n')
    fuit.write('#\n')

#############################################################
# Check Clock
#############################################################

fuit.write("Time\n\n")

result = nr.run(
    task=netmiko_send_command,
    command_string="display clock"
)

for elem in result:
    logentries = result[elem][0].result.split('\n')
    fuit.write(elem + ":\n")
    for regel in logentries:
        fuit.write('  ' + regel + "\n")
    fuit.write('#\n')

#############################################################
# Check NTP sessions
#############################################################

fuit.write("NTP\n\n")

result = nr.run(
    task=netmiko_send_command,
    command_string="display ntp session"
)

for elem in result:
    logentries = result[elem][0].result.split('\n')
    fuit.write(elem + ":\n")
    for regel in logentries:
        fuit.write('  ' + regel + "\n")
    fuit.write('#\n')

#############################################################
# Check interfaces
#############################################################

fuit.write("Interfaces\n\n")

result = nr.run(
    task=netmiko_send_command,
    command_string="display interface brief"
)

for elem in result:
    logentries = result[elem][0].result.split('\n')
    fuit.write(elem + ":\n")
    fsw = open(pad + elem + '.txt', 'w')
    for regel in logentries:
        woorden = regel.split()
        if 'DOWN' in woorden and 'unused' in woorden:
            fsw.write('interface ' + woorden[0] + '\n')
            fsw.write('  shutdown\n')
            fsw.write('#\n')
        elif 'DOWN' in woorden and len(woorden) == 6:
            fsw.write('interface ' + woorden[0] + '\n')
            fsw.write('  descr unused\n')
            fsw.write('  shutdown\n')
            fsw.write('#\n')
        fuit.write('  ' + regel + "\n")
    fuit.write('#\n')
    fsw.close()

#############################################################
# Check snmp
#############################################################

fuit.write("SNMP\n\n")

result = nr.run(
    task=netmiko_send_command,
    command_string="display cur | i snmp"
)

for elem in result:
    logentries = result[elem][0].result.split('\n')
    fuit.write(elem + ":\n")
    for regel in logentries:
        woorden = regel.split()
        if 'DOWN' in woorden and 'unused' in woorden:
            print('interface ' + woorden[0])
            print('  shutdown')
            print('#')
        fuit.write('  ' + regel + "\n")
    fuit.write('#\n')

#############################################################
# Check info-center
#############################################################

fuit.write("Logging\n\n")

result = nr.run(
    task=netmiko_send_command,
    command_string="display cur | i info-center"
)

for elem in result:
    logentries = result[elem][0].result.split('\n')
    fuit.write(elem + ":\n")
    for regel in logentries:
        woorden = regel.split()
        if 'DOWN' in woorden and 'unused' in woorden:
            print('interface ' + woorden[0])
            print('  shutdown')
            print('#')
        fuit.write('  ' + regel + "\n")
    fuit.write('#\n')

#############################################################
# Check routing
#############################################################

fuit.write("Routing\n\n")

result = nr.run(
    task=netmiko_send_command,
    command_string="display cur | i route-static"
)

for elem in result:
    logentries = result[elem][0].result.split('\n')
    fuit.write(elem + ":\n")
    for regel in logentries:
        woorden = regel.split()
        if 'DOWN' in woorden and 'unused' in woorden:
            print('interface ' + woorden[0])
            print('  shutdown')
            print('#')
        fuit.write('  ' + regel + "\n")
    fuit.write('#\n')

#############################################################
# Check lldp
#############################################################

fuit.write("LLDP\n\n")

result = nr.run(
    task=netmiko_send_command,
    command_string="display lldp neigh list"
)

#############################################################
# Create a command file with interface descriptions based on LLDP
# and shutdown unused ports
#############################################################

for elem in result:
    logentries = result[elem][0].result.split('\n')
    fuit.write(elem + ":\n")
    fsw = open(pad + "/descriptions/" + elem + '.txt', 'a')
    for regel in logentries:
        woorden = regel.split()
        if len(woorden) == 4:
            intf = woorden[2].replace('GigabitEthernet', 'gi')
            intf = intf.replace('FortyGigE', 'for')
            intf = intf.replace('M-gi', 'mge')
            intf = intf.replace('Ten-gi', 'ten')
            fsw.write("interface " + woorden[0] + '\n')
            fsw.write("  descr " + woorden[3] + ":" + intf + '\n')
            fsw.write('#\n')
        fuit.write('  ' + regel + "\n")
    fuit.write('#\n')
    fsw.close()

#############################################################
# Create a list of the software versions installed
#############################################################

fuit.write("Software versions\n\n")

result = nr.run(
    task=netmiko_send_command,
    command_string='display version | i "System image version:"'
)

for elem in result:
    logentries = result[elem][0].result.split('\n')
    fuit.write(elem + ": " + logentries[-1] + '\n')

fuit.close()
