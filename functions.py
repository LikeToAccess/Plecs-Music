# -*- coding: utf-8 -*-
# filename          : functions.py
# description       : Helper functions for Plex Bot
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 12-13-2020
# version           : v1.0
# usage             : python functions.py
# notes             : This should not be run directly
# license           : MIT
# py version        : 3.7.9 (must run on 3.6 or higher)
#==============================================================================
from datetime import datetime
from random import randint
import os


def kill_token(chars=4):
	token = []
	for char in range(chars):
		token.append(str(randint(0,9)))
	return "".join(token)

def read_file(filename, directory=None):
	if directory:
		os.chdir(f"{os.getcwd()}/{directory}")
	with open(filename, "r") as f:
		lines = f.read().split("\n")
	return lines

def write_file(filename, msg):
	with open(filename, "w") as f:
		f.write(msg)

def append_file(filename, msg):
	with open(filename, "a") as f:
		f.write(msg)

def filter_file(lines, filename=False):
	if filename:
		lines = read_file(filename)
	data = []
	for line in lines:
		if line[:1] != "#" and line != "":
			data.append(line)
	return data

def status(args=""):
	os.system(f"python status.py {args}")

def log(ctx, filename="log.txt"):
	data = ctx.message.content
	data = f"[{datetime.now()}]{ctx.message.author} :: {data}\n"
	append_file("log.txt", data)


if __name__ == "__main__":
	print("Wrong module, switchihng to \"main.py\"...")
	os.system("python main.py")