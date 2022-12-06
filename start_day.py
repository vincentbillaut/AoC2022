import browser_cookie3
import os
import re
import requests
import shutil
import sys

from datetime import date


def get_browser_cookies():
    cj = browser_cookie3.brave()
    return cj


class AdventOfCodeDay:
    def __init__(self, day: int = None, overwrite: bool = False):
        # initialize_day
        if day is None:
            day = int(date.today().strftime("%d").lstrip("0"))
            print(f"Initializing day {day} (today's date)")
        else:
            print(f"Initializing day {day}")
        self.day: int = day
        # get cookies
        print("... getting browser cookies")
        cj = get_browser_cookies()
        # get inputs
        print("... getting input")
        dir_path, file_path = f"day{day}", f"input{day}"
        if not os.path.exists(dir_path) or overwrite:
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            os.chdir(dir_path)
            r = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cj)
            with open(file_path, "w") as f:
                f.write(r.text)
            print("Done.")
            os.chdir("..")
        else:
            print("Input folder already existed (nothing done).")
        self.input_path = os.path.join(dir_path, file_path)
        self._display_head()

    def _display_head(self, n=5):
        print("\n", "-" * 40)
        with open(self.input_path, "r") as f:
            for i, l in enumerate(f):
                if i < n:
                    print(l, end="")
        print(f"length {i+1}".center(40, "-"), "\n")

    def _load_all_lines(self, proc_f):
        data = []
        with open(self.input_path, "r") as f:
            for l in f:
                data.append(proc_f(l))
        return data

    def load_regex(self, pattern, n, strip=False):
        data = []
        with open(self.input_path, "r") as f:
            for l in f:
                match = re.match(pattern, l.strip() if strip else l)
                if match:
                    data.append(tuple([match.group(i + 1) for i in range(n)]))
        return data

    def load_integers(self):
        func = lambda l: int(l.strip())
        return self._load_all_lines(func)

    def load_strings(self, strip=True):
        func = (lambda l: l.strip()) if strip else (lambda l: l)
        return self._load_all_lines(func)
