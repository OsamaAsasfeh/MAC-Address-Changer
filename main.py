import optparse
import re
import subprocess

def the_signature():
    print('''
                                     ______                                                                 __                                                    
                                   /      \                                                               |  \\                                                   
                                  |  $$$$$$\\ _______        ______ ____   ______   _______         _______| $$____   ______  _______   ______   ______   ______  
                                  | $$  | $$/'       \\      |      \\    \\ |      \\ /       \\       /       | $$    \\ |      \\|       \\ /      \\ /      \\ /      \\ 
                                  | $$  | $|  $$$$$$$      | $$$$$$\\$$$$\\ \\$$$$$$|  $$$$$$$      |  $$$$$$| $$$$$$$\\ \\$$$$$$| $$$$$$$|  $$$$$$|  $$$$$$|  $$$$$$\\
                                  | $$  | $$\\$$    \\       | $$ | $$ | $$/      $| $$            | $$     | $$  | $$/$/      $| $$  | $| $$  | $| $$    $| $$   \\$$
                                  | $$__/ $$_\\$$$$$$\\      | $$ | $$ | $|  $$$$$$| $$_____       | $$_____| $$  | $|  $$$$$$| $$  | $| $$__| $| $$$$$$$| $$      
                                   \\$$    $|       $$      | $$ | $$ | $$\\$$    $$\\$$     \\       \\$$     | $$  | $$\\$$    $| $$  | $$\\$$    $$\\$$     | $$      
                                    \\$$$$$$ \\$$$$$$$        \\$$  \\$$  \\$$ \\$$$$$$$ \\$$$$$$$        \\$$$$$$$\\$$   \\$$ \\$$$$$$$\\$$   \\$$_\\$$$$$$$ \\$$$$$$$\\$$      
                                                                                                                                     |  \\__| $$                  
                                                                                                                                      \\$$    $$                  
                                                                                                                                       \\$$$$$$                   
    ''')
    print('''
     __       __                __                 __                                                                                                                    ______          __       
    |  \     /  \              |  \               |  \                                                                                                                  /      \        |  \      
    | $$\   /  $$ ______   ____| $$ ______        | $$____  __    __         ______   _______  ______  ______ ____   ______          ______   _______  ______   _______|  $$$$$$\______ | $$____  
    | $$$\ /  $$$|      \ /      $$/      \       | $$    \|  \  |  \       /      \ /       \|      \|      \    \ |      \        |      \ /       \|      \ /       | $$_  \$/      \| $$    \ 
    | $$$$\  $$$$ \$$$$$$|  $$$$$$|  $$$$$$\      | $$$$$$$| $$  | $$      |  $$$$$$|  $$$$$$$ \$$$$$$| $$$$$$\$$$$\ \$$$$$$\        \$$$$$$|  $$$$$$$ \$$$$$$|  $$$$$$| $$ \  |  $$$$$$| $$$$$$$\\
    | $$\$$ $$ $$/      $| $$  | $| $$    $$      | $$  | $| $$  | $$      | $$  | $$\$$    \ /      $| $$ | $$ | $$/      $$       /      $$\$$    \ /      $$\$$    \| $$$$  | $$    $| $$  | $$\\
    | $$ \$$$| $|  $$$$$$| $$__| $| $$$$$$$$      | $$__/ $| $$__/ $$      | $$__/ $$_\$$$$$$|  $$$$$$| $$ | $$ | $|  $$$$$$$      |  $$$$$$$_\$$$$$$|  $$$$$$$_\$$$$$$| $$    | $$$$$$$| $$  | $$ \\
    | $$  \$ | $$\$$    $$\$$    $$\$$     \      |$$$$$$$$|$$$$$$$$       \$$$$$$$\ |       $$\$$    $| $$ | $$ | $$\$$    $$      \$$      \ |       $$\$$      \ | $$    | $$  | $$    $$\$$   $$\\
     \$$   \$$\__|$$$$$$$$ \$$$$$$$ \$$$$$$$       \_______|\_______|       \_______| \$$$$$$$  \$$$$$$ \$$  \$$  \$$ \$$$$$$$       \$$$$$$$  \$$$$$$$  \$$$$$$$  \$$     \$$   \$$$$$$$ \$$$$$$ 
    ''')


def change_mac_linux(interface, new_mac):
    print("[+] Changing Mac Address for ", interface, "to ", new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC Address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Interface to change its MAC Address")
    (option, arguments) = parser.parse_args()
    if not option.interface:
        parser.error("[-] Please specify an Interface , use --help for more info.")
    elif not option.new_mac:
        parser.error("[-] Please specify an Mac Address , use --help for more info.")
    return option


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_reslut = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_reslut:
        return mac_address_search_reslut.group(0)
    else:
        print("[-] No mac address found in this interface : " + str(interface))


def main():
    the_signature()
    mac_address_regex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')

    options = get_arguments()

    match = mac_address_regex.match(str(options.new_mac))

    if match:
        # The MAC address string is valid
        current_mac = get_current_mac(options.interface)
        print("[+] Current Mac :" + current_mac)
        change_mac_linux(options.interface, options.new_mac)
        current_mac = get_current_mac(options.interface)

        if current_mac == options.new_mac.lower():
            print("[+] Mac address was successfully changed to  :" + current_mac)
        else:
            print("[-] Mac address did not get changed .")
    else:
        # The MAC address string is invalid
        print("Invalid MAC address")


main()