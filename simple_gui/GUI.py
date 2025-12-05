#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
import json


# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 400,
                             height = 300)
        # create a Label
        self.pls = Label(self.login, 
                       text = "Please login to continue",
                       justify = CENTER, 
                       font = "Helvetica 14 bold")
          
        self.pls.place(relheight = 0.15,
                       relx = 0.2, 
                       rely = 0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Helvetica 12")
          
        self.labelName.place(relheight = 0.2,
                             relx = 0.1, 
                             rely = 0.2)
          
        # create a entry box for 
        # tyoing the message
        self.entryName = Entry(self.login, 
                             font = "Helvetica 14")
          
        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
          
        # set the focus of the curser
        self.entryName.focus()
          
        # create a Continue Button 
        # along with action
        self.go = Button(self.login,
                         text = "CONTINUE", 
                         font = "Helvetica 14 bold", 
                         command = lambda: self.goAhead(self.entryName.get()))
          
        self.go.place(relx = 0.4,
                      rely = 0.55)
        self.Window.mainloop()
  
    def goAhead(self, name):
        def goAhead(self, name):
    if len(name) > 0:
        msg = json.dumps({"action": "login", "name": name})
        self.send(msg)
        response = json.loads(self.recv())

        #Login success
        if response["status"] == 'ok':
            
            self.login.destroy()
            self.sm.set_state(S_LOGGEDIN)
            self.sm.set_myname(name)
            self.layout(name)

           
            self.textCons.config(state=NORMAL)
            self.textCons.insert(END, "✅ Welcome to the chat, " + name + "!\n\n")
            self.textCons.insert(END, menu + "\n\n")
            self.textCons.config(state=DISABLED)
            self.textCons.see(END)

            
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()

        #Login failed
        else:
            # Show a popup window
            from tkinter import messagebox
            messagebox.showerror("Login failed", "❌ Username already taken or invalid.\nPlease try again.")

        
  
    # The main layout of the chat
    def layout(self,name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A", 
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
          
        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#B05EA8",
                             fg = "#EAECEE",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
          
        self.textCons.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
          
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
          
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
          
        self.entryMsg.focus()
          
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
        self.emojiButton = Button(self.bottomFrame,
                                text="😊",
                                font=("Segoe UI Emoji", 14),
                                command=self.open_emoji_picker)
        self.emojiButton.pack(side=RIGHT, padx=5)

        

          
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06, 
                             relwidth = 0.22)
          
        self.textCons.config(cursor = "arrow")
          
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)
    def open_emoji_picker(self):
        picker = Toplevel(self.window)
        picker.title("Emoji Picker")
        picker.geometry("300x200")
        picker.resizable(False, False)

        emojis = ["😊", "😂", "🤣", "❤️", "💕", "🥺",
                    "👍", "😎", "😭", "😡", "😱", "🤔",
                    "🎉", "🔥", "💀", "✨", "🤯", "👀" ]


        row = 0
        col = 0
        for emoji in emojis:
            b = Button(picker, text=emoji, font=("Segoe UI Emoji", 18),
                        command=lambda e=emoji: (self.insert_emoji(e), picker.destroy()))
            b.grid(row=row, column=col, padx=5, pady=5)

            col += 1
            if col > 5:   
                col = 0
                row += 1
    def insert_emoji(self, emoji):
        self.entryMsg.insert(END, emoji)


  
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)


    def proc(self):
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = ""

        # receive message from peer
        if self.socket in read:
            peer_msg = self.recv()

        # if user typed a message or received a message
        if len(self.my_msg) > 0 or len(peer_msg) > 0:
            new_msg = self.sm.proc(self.my_msg, peer_msg)
            self.my_msg = ""  # clear the outgoing message buffer

            self.textCons.config(state=NORMAL)
            self.textCons.insert(END, new_msg + "\n\n")  # print only new msg
            self.textCons.config(state=DISABLED)
            self.textCons.see(END)

            # IMPORTANT FIX: reset system_msg
            self.system_msg = ""


    def run(self):
        self.login()
# create a GUI class object
if __name__ == "__main__": 
    g = GUI()