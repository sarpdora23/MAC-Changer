import subprocess
import optparse
import re
import random
import time

def get_arguments():
    parse = optparse.OptionParser()
    parse.add_option("-i","--interface",dest ="interface",help = "Which interface do you want to change")
    parse.add_option("-m","--mac",dest = "mac",help = "New MAC Adresses")
    parse.add_option("-r","--random_mode",dest = "random_mode",help = "Changing mode random or basic")
    (options,arguments) = parse.parse_args()
    if not options.interface:
        parse.error("[-]Please enter interface which do you want to change mac more info --help")
    elif not options.mac:
        if options.random_mode == "basic":
            parse.error("[-]Please enter mac address more info --help")
    elif not options.random_mode:
        parse.error("[-]Please enter random mode more info --help")
    return options
def change_mac_normal(interface,new_mac):
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
    subprocess.call(["ifconfig",interface,"up"])
def change_mac_random(interface):
    while True:
        new_mac = "00:"+str(random.randint(10,99))+":"+str(random.randint(10,99))+":"+ str(random.randint(10,99))+":"+ str(random.randint(10,99))+":"+str(random.randint(10,99))
        subprocess.call(["ifconfig",interface,"down"])
        subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
        subprocess.call(["ifconfig",interface,"up"])
        current_mac =get_current_mac(interface)
        if current_mac:
            if current_mac == new_mac:
                print("[+] MAC address changed succesfully")
                print("[+] New MAC address: " + current_mac)
            else:
                print("[-] MAC address couldn't changed")
        time.sleep(15)
def get_current_mac(interface):
    ifconfig_output = str(subprocess.check_output(["ifconfig",interface]))
    mac_output =re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_output)
    if mac_output:
        return mac_output.group(0)
    else:
        print("[-] Sorry the interface doesn't have any mac address")
def check_mode(random_mode,interface,mac):
    if random_mode == "basic":
        change_mac_normal(interface,mac)
        change_mac_normal(options.interface,options.mac)
        current_mac =get_current_mac(options.interface)
        if current_mac:
            if current_mac == options.mac:
                print("[+] MAC address changed succesfully")
                print("[+] New MAC address: " + current_mac)
            else:
                print("[-] MAC address couldn't changed")
    elif random_mode == "random":
        change_mac_random(interface)
    else:
        print("[-] Invalid value info --help")
options = get_arguments()
check_mode(options.random_mode,options.interface,options.mac)
