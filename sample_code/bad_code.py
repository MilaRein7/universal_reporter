# sample_code/bad_code.py

import os

user_input = "print('Hello from eval')"
eval(user_input)  # специально небезопасно, чтобы Bandit ругался

password = "super_secret_password"
print("Password is:", password)