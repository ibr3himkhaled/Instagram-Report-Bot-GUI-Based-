import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
import json
import logging
import random
import time
import threading
from selenium import webdriver
from selenium_stealth import stealth
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from datetime import datetime

class InstagramReportBot:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Instagram Report Bot")
        self.root.geometry("800x600")
        ctk.set_appearance_mode("dark")

        self.config = self.load_config()
        self.proxies = []
        self.accounts = []
        self.account_index = 0
        self.ua = UserAgent()

        logging.basicConfig(filename='log.txt', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        self.setup_gui()

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'delay_min': 2,
                'delay_max': 5,
                'max_reports': 100,
                'proxy_enabled': True
            }

    def setup_gui(self):
        self.input_frame = ctk.CTkFrame(self.root)
        self.input_frame.pack(pady=10, padx=10, fill="x")

        self.control_frame = ctk.CTkFrame(self.root)
        self.control_frame.pack(pady=10, padx=10, fill="x")

        self.log_frame = ctk.CTkFrame(self.root)
        self.log_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.target_label = ctk.CTkLabel(self.input_frame, text="Target Username/URL:")
        self.target_label.pack(pady=5)
        self.target_entry = ctk.CTkEntry(self.input_frame, width=300)
        self.target_entry.pack(pady=5)

        self.report_type = tk.StringVar(value="spam")
        report_options = ["spam", "harassment", "impersonation", "inappropriate"]
        self.report_label = ctk.CTkLabel(self.input_frame, text="Report Type:")
        self.report_label.pack(pady=5)
        for option in report_options:
            rb = ctk.CTkRadioButton(self.input_frame, text=option, variable=self.report_type, value=option)
            rb.pack(pady=2)

        self.proxy_var = tk.BooleanVar(value=True)
        self.proxy_check = ctk.CTkCheckBox(self.control_frame, text="Use Proxies", variable=self.proxy_var)
        self.proxy_check.pack(pady=5)

        self.load_proxy_btn = ctk.CTkButton(self.control_frame, text="Load Proxies", command=self.load_proxies)
        self.load_proxy_btn.pack(pady=5)

        self.load_accounts_btn = ctk.CTkButton(self.control_frame, text="Load Accounts", command=self.load_accounts_file)
        self.load_accounts_btn.pack(pady=5)

        self.start_btn = ctk.CTkButton(self.control_frame, text="Start Reporting", command=self.start_reporting)
        self.start_btn.pack(pady=5)

        self.progress = ttk.Progressbar(self.control_frame, length=300, mode='determinate')
        self.progress.pack(pady=10)

        self.log_text = ctk.CTkTextbox(self.log_frame, height=200)
        self.log_text.pack(fill="both", expand=True)

    def load_proxies(self):
        file_path = filedialog.askopenfilename(title="Select Proxy File",
                                               filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return
        try:
            with open(file_path, 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            self.log_message(f"Loaded {len(self.proxies)} proxies from {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load proxies: {str(e)}")

    def load_accounts_file(self):
        file_path = filedialog.askopenfilename(title="Select Accounts File",
                                               filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return
        try:
            with open(file_path, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
                self.accounts = []
                for line in lines:
                    if ":" in line:
                        username, password = line.split(":", 1)
                        self.accounts.append((username.strip(), password.strip()))
                self.account_index = 0
                self.log_message(f"Loaded {len(self.accounts)} accounts from {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load accounts: {str(e)}")

    def get_random_proxy(self):
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        logging.info(message)

    def report_target(self, target, report_type):
        try:
            if not self.accounts:
                self.log_message("No accounts loaded!")
                return False

            username, password = self.accounts[self.account_index]
            self.account_index = (self.account_index + 1) % len(self.accounts)

            proxy_dict = None
            proxy = None
            if self.proxy_var.get():
                proxy = self.get_random_proxy()
                if proxy:
                    proxy_dict = {
                        "http": f"http://{proxy}",
                        "https": f"http://{proxy}"
                    }

            options = webdriver.ChromeOptions()
            if proxy_dict:
                options.add_argument(f'--proxy-server={proxy_dict["http"]}')
            driver = uc.Chrome(options=options)

            stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True)

            # --- Instagram login and report logic goes here ---
            # Replace this with real login and report steps

            time.sleep(random.uniform(self.config['delay_min'], self.config['delay_max']))

            self.log_message(f"Reported {target} with {username} | Proxy: {proxy if proxy else 'None'}")
            return True

        except Exception as e:
            self.log_message(f"Error reporting {target}: {str(e)}")
            return False
        finally:
            try:
                driver.quit()
            except:
                pass

    def start_reporting(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Please enter a target!")
            return

        def report_thread():
            self.start_btn.configure(state="disabled")
            self.progress['value'] = 0
            success_count = 0

            for i in range(self.config['max_reports']):
                if self.report_target(target, self.report_type.get()):
                    success_count += 1
                self.progress['value'] = ((i + 1) / self.config['max_reports']) * 100
                self.root.update_idletasks()

            self.log_message(f"Reporting complete. Success: {success_count}/{self.config['max_reports']}")
            self.start_btn.configure(state="normal")

        thread = threading.Thread(target=report_thread)
        thread.daemon = True
        thread.start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    bot = InstagramReportBot()
    bot.run()
