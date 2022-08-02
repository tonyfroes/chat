import socket
import threading
import tkinter as tk
from tkinter import *
from random import randint
from tkinter import messagebox
from tkinter import font
from tkinter import ttk
import webbrowser

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
CONNECT = True

users = []
NAME = ''