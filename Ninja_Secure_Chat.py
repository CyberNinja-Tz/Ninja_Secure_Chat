import os
import subprocess
import sys
import threading
import time

# --- AUTO-INSTALLER ---
try:
    import irc.client
except ImportError:
    print("\033[1;33m[*] Ina Install Vitu vya Muhimu... Subiri Kidogo.\033[0m")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "irc"])
    os.execv(sys.executable, ['python3'] + sys.argv)

import irc.client

# Rangi
RED, GREEN, CYAN, YELLOW, BLUE, WHITE, NC = '\033[0;31m', '\033[0;32m', '\033[0;36m', '\033[1;33m', '\033[0;34m', '\033[1;37m', '\033[0m'

# Kazi ya kuandika chati kwenye screen
def print_chat(text, nickname):
    terminal_width = os.get_terminal_size().columns
    left_width = int(terminal_width * 0.6)
    clean_text = text.ljust(left_width)[:left_width]
    sys.stdout.write(f"\r\033[K{clean_text} {WHITE}| {NC}\n")
    sys.stdout.write(f"{YELLOW}Mimi >> {NC}")
    sys.stdout.flush()

# Handlers za matukio ya IRC
def on_connect(connection, event):
    pass # Inasubiri 'welcome'

def on_welcome(connection, event, channel, password, nickname):
    print_chat(f"{GREEN}[V] Unaunganishwa! Inajoin {channel}...{NC}", nickname)
    if password:
        connection.join(channel, key=password)
    else:
        connection.join(channel)

def on_pubmsg(connection, event, nickname):
    user = event.source.split('!')[0]
    msg = event.arguments[0]
    if user != nickname:
        print_chat(f"{CYAN}[{user}]:{NC} {msg}", nickname)

def on_join(connection, event, nickname):
    user = event.source.split('!')[0]
    print_chat(f"{YELLOW}>>> {user} Ame Join.{NC}", nickname)

def on_quit(connection, event, nickname):
    user = event.source.split('!')[0]
    print_chat(f"{RED}<<< {user} Ametoka.{NC}", nickname)

def show_static_ui():
    os.system('clear')
    width = os.get_terminal_size().columns
    left_p = int(width * 0.6)
    header = f"{RED} NINJA SECURE CHAT {NC}".center(left_p) + f"{BLUE} SETTINGS & COMMANDS {NC}".center(width - left_p)
    print(f"{header}\n" + "=" * width)
    
    guide = [
        "COMMANDS:",
        "1. /quit   - Toka",
        "2. /nick   - Badili Jina",
        "3. /clear  - Safisha Chat",
        "",
        "STATUS: ONLINE (WAN)",
        "ENGINE: IRC.CLIENT.CORE"
    ]
    for i in range(7):
        print(" " * left_p + f"{WHITE}| {NC}" + (guide[i] if i < len(guide) else ""))

def start_ninja():
    os.system('clear')
    print(f"{RED}NINJA SECURE CHAT - SERVER LIST{NC}")
    servers = {"1": "Libera Chat", "2": "Freenode", "3": "Undernet", "4": "DALnet", "5": "Rizon"}
    server_ips = {"1": "irc.libera.chat", "2": "chat.freenode.net", "3": "irc.undernet.org", "4": "irc.dal.net", "5": "irc.rizon.net"}

    for k, v in servers.items(): print(f"[{k}] {v}")
    
    choice = input(f"\n{YELLOW}Chagua Server: {NC}")
    s_ip = server_ips.get(choice, "irc.libera.chat")
    nick = input(f"{CYAN}NickName: {NC}")
    chan = input(f"{CYAN}Channel: {NC}")
    if not chan.startswith("#"): chan = "#" + chan
    pwd = input(f"{CYAN}Password (Acha wazi): {NC}")
    if pwd == "": pwd = None

    
    irc_obj = irc.client.IRC()
    
    try:
        server = irc_obj.server()
        server.connect(s_ip, 6667, nick)
        
        # Kuunganisha Events
        irc_obj.add_global_handler("welcome", lambda c, e: on_welcome(c, e, chan, pwd, nick))
        irc_obj.add_global_handler("pubmsg", lambda c, e: on_pubmsg(c, e, nick))
        irc_obj.add_global_handler("join", lambda c, e: on_join(c, e, nick))
        irc_obj.add_global_handler("quit", lambda c, e: on_quit(c, e, nick))

        threading.Thread(target=irc_obj.process_forever, daemon=True).start()
        
    except Exception as e:
        print(f"{RED}Error: {e}{NC}")
        return

    show_static_ui()
    
    while True:
        try:
            msg = input(f"{YELLOW}Mimi >> {NC}")
            if not msg: continue
            
            if msg.startswith("/"):
                cmd = msg.split()
                if cmd[0] == "/quit": break
                elif cmd[0] == "/clear": show_static_ui()
                elif cmd[0] == "/nick" and len(cmd) > 1:
                    server.nick(cmd[1])
                    nick = cmd[1]
            else:
                if server.is_connected():
                    server.privmsg(chan, msg)
                else:
                    print(f"\n{RED}[!] Connection Imekata.{NC}")
                    break
        except (EOFError, KeyboardInterrupt):
            break

if __name__ == "__main__":
    start_ninja()
