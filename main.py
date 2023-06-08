#!/usr/bin/env python3

import platform
import os
import distro
import subprocess
import re
import psutil

import colorama
from colorama import init, Fore, Back, Style
from getpass import getuser

init(autoreset=True)

def ln(part1, part2):
    return f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}{part1}{Style.RESET_ALL} {part2}"

def get_host_and_user():
    return f"{getuser()}@{platform.node()}"

def get_memoryinfo():
    # Get the memory usage information
    memory = psutil.virtual_memory()

    # Convert memory values to gigabytes (GB)
    used_memory_gb = memory.used / (1024 ** 3)
    total_memory_gb = memory.total / (1024 ** 3)

    # Calculate the memory usage percentage
    memory_usage_percent = (used_memory_gb / total_memory_gb) * 100

    # Format the memory information
    memory_info_formatted = f"{used_memory_gb:.2f}/{total_memory_gb:.2f}GB • {memory_usage_percent:.2f}%"

    return memory_info_formatted

def get_gpu_name() -> str:
    info = _get_linux_gpu_name()
    if "processor graphics controller" in info.lower():
        info = "Intergrated Graphics"
    return info

def _get_linux_gpu_name():
    try:
        command = 'lspci -vnn | grep VGA -A 1'
        output = subprocess.check_output(command, shell=True).decode().strip()
        pattern = r'\b(?<=: ).*?(?= \[)'
        match = re.search(pattern, output)

        if match:
            gpu_name = match.group()
            return gpu_name
        else:
            return "GPU name not found."
    except Exception as e:
        return str(e)

def get_cpuinfo():
    with open("/proc/cpuinfo", "r") as f:
        for line in f:
            if re.search("model name", line):
                return line.replace("model name	: ", "").strip()
                
        return "couldn't find cpuinfo"

def get_distro() -> str:
    info = f"{distro.name()} {distro.version()}"
    if "arch" in info.lower():
        info = f"{info} (arch btw)"
    return info

def get_architecture() -> str:
    return str(platform.architecture()).strip(")(").replace("'", "").replace(", ", " - ")

def get_ascii() -> str: 
    ascii_art = f"""
       {Style.DIM}.---.{Style.RESET_ALL}            {Style.BRIGHT}\033[4m{get_host_and_user()}\033[0m
      {Style.DIM}/     \\{Style.RESET_ALL}       {ln('os.', get_distro())}
      {Style.DIM}\\.{Style.RESET_ALL}{Fore.WHITE}@{Style.RESET_ALL}{Style.DIM}-{Style.RESET_ALL}{Fore.WHITE}@{Style.DIM}./{Style.RESET_ALL}     {ln('krnl.', platform.release())}
      {Style.DIM}/`{Style.RESET_ALL}{Fore.YELLOW}\\_/{Fore.RESET}{Style.DIM}`\\{Style.RESET_ALL}     {ln('arch.', get_architecture())}
     {Style.DIM}//  {Style.RESET_ALL}{Style.BRIGHT}_{Style.DIM}  \\\\{Style.RESET_ALL}     {ln('cpu.', get_cpuinfo())}
    {Style.DIM}| \\     )|{Style.RESET_ALL}{Fore.YELLOW}_{Style.RESET_ALL}    {ln('gpu.', get_gpu_name())}
   {Fore.YELLOW}/`\\_{Fore.RESET}{Style.DIM}`>  <{Style.RESET_ALL}{Fore.YELLOW}_/ \\{Fore.RESET}   {ln('mem.', get_memoryinfo())}
{Style.DIM}jgs{Style.RESET_ALL}{Fore.YELLOW}\\__/{Fore.RESET}{Style.DIM}'---'{Style.RESET_ALL}{Fore.YELLOW}\\__/{Fore.RESET}        {Fore.RED}🂠  {Fore.GREEN}🂠  {Fore.YELLOW}🂠  {Fore.BLUE}🂠  {Fore.MAGENTA}🂠  {Fore.CYAN}🂠  {Style.RESET_ALL}🂠
    """
    return ascii_art

os.system("clear")
print(get_ascii())
