import tkinter as tk
from tkinter import ttk, filedialog
from typing import Text
from Profile import *
import pathlib
from tkinter import messagebox as mb
import socket

class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20, command=self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.
        #self.password...
        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show='*')
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()


    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        res=mb.askquestion('Account Creation', "Do you already have an account and Local file on this computer?")
        if res == 'no':
            file_path = tk.simpledialog.askstring(title='File Creator', prompt='Please enter the File Path to the Directory for where you would like your file to be in (Do not include New file name).')
            if file_path == None:
                exit()
            file_name = tk.simpledialog.askstring(title='File Creator', prompt='Please enter the File Name')
            if file_name == None:
                exit()
            file_path = pathlib.Path(file_path)
            if file_path.exists():
                self.new_file = file_path / f"{file_name}.dsu"
                self.new_file.touch()
                exit_key = 1
                while exit_key != 0:
                    server = tk.simpledialog.askstring(title='Account Creator', prompt='Please enter a Server')
                    if server == None:
                        exit()
                    username = tk.simpledialog.askstring(title='Account Creator', prompt='Please enter a Username')
                    if username == None:
                        exit()
                    password = tk.simpledialog.askstring(title='Account Creator', prompt='Please enter a Password')
                    if password == None:
                        exit()
                    SERVER = server
                    PORT = 3021
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                            client.connect((SERVER, PORT))
                            send = client.makefile("w")
                            recv = client.makefile("r")
                            msg = json.dumps({"join": {"username": username, "password": password, "token": ""}})
                            send.write(msg + "\r\n")
                            send.flush()
                            srv_msg = recv.readline()
                            srv_msg_checker = json.loads(srv_msg)
                            if srv_msg_checker["response"]["type"] == "error":
                                tk.messagebox.showinfo(title="Username/Password/Server Error", message=f'Password/Username/Server Invalid Please Try again')
                            else:
                                self.profile = Profile(server, username, password)
                                self.username = self.profile.username
                                self.password = self.profile.password
                                self.server = self.profile.dsuserver
                                self.messages_sent = self.profile.messages_sent
                                self.messages_recieved = self.profile.messages_recieved
                                self.unread_messages = self.profile.unread_messages
                                self.list_of_contacts = self.profile.list_of_contacts
                                self.recipient = None
                                self.root = root
                                self._draw()
                                exit_key = 0
                    except socket.gaierror:
                        tk.messagebox.showinfo(title="Username/Password/Server Error", message=f'Password/Username/Server Invalid Please Try again')
                    except ConnectionRefusedError:
                        tk.messagebox.showinfo(title="Username/Password/Server Error", message=f'Password/Username/Server Invalid Please Try again')
            else:
                tk.messagebox.showerror(title="File Path Error", message='Entered An invalid Path, Please try again')
        else:
            exit_key1 = 1
            while exit_key1 != 0:
                file_path = tk.simpledialog.askstring(title='File Creator', prompt='Please enter a valid dsu file path.')
                if file_path == None:
                    exit()
                file_path = pathlib.Path(file_path)
                if file_path.exists():
                    self.new_file = pathlib.Path(file_path)
                    self.profile = Profile()
                    self.profile.load_profile(self.new_file)
                    self.username = self.profile.username
                    self.password = self.profile.password
                    self.server = self.profile.dsuserver
                    self.messages_sent = self.profile.messages_sent
                    self.messages_recieved = self.profile.messages_recieved
                    self.unread_messages = self.profile.unread_messages
                    self.list_of_contacts = self.profile.list_of_contacts
                    self.recipient = None
                    self.root = root
                    self._draw()
                    for name in self.list_of_contacts:
                        self.body.insert_contact(name)
                    tk.messagebox.showinfo(title="File Succesfully opened", message=f'Login Succesful, Welcome {self.username}')
                    exit_key1 = 0
                else:
                    tk.messagebox.showerror(title="File Path Error", message='Entered An invalid Path, Please try again')


    def send_message(self):
        text_message = self.body.get_text_entry()
        self.body.set_text_entry('')
        if text_message != '' and text_message != None:
            self.body.entry_editor.delete(1.0, tk.END)
            self.profile.send_messages(text_message, self.recipient)
            self.body.insert_user_message(text_message)
            self.recipient_selected(self.recipient)
    
    
    def add_contact(self):
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        contact_name = tk.simpledialog.askstring(title='Contact Adder', prompt='Add a Contact')
        self.body.insert_contact(contact_name)
        if contact_name not in self.list_of_contacts:
            self.list_of_contacts.append(contact_name)



    def recipient_selected(self, recipient):
        self.recipient = recipient
        self.body.set_text_entry('')
        self.body.entry_editor.delete(1.0, tk.END)
        self.profile.retrieve_all_messages()
        list_of_all_messages = []
        if self.recipient in self.profile.messages_recieved:
            messages_received = self.profile.messages_recieved[recipient]
            for index in range(len(messages_received)):
                list_of_all_messages.append(messages_received[index])
        
        if self.recipient in self.profile.messages_sent:
            messages_sent = self.messages_sent[recipient]
            for index1 in range(len(messages_sent)):
                list_of_all_messages.append(messages_sent[index1])

        newlist = sorted(list_of_all_messages, key=lambda d: d['timestamp'], reverse=True)
        for message in newlist:
            if message['from'] == 'me':
                self.body.insert_user_message(message['message'])
            else:
                self.body.insert_contact_message(message['message'])

    def configure_server(self):
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        SERVER = ud.server
        PORT = 3021
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((SERVER, PORT))
                send = client.makefile("w")
                recv = client.makefile("r")
                msg = json.dumps({"join": {"username": ud.user, "password": ud.pwd, "token": ""}})
                send.write(msg + "\r\n")
                send.flush()
                srv_msg = recv.readline()
                srv_msg_checker = json.loads(srv_msg)
                if srv_msg_checker["response"]["type"] == "error":
                    tk.messagebox.showinfo(title="Username/Password/Server Error", message=f'Password/Username/Server Invalid Please Try again')
                else:
                    self.username = ud.user
                    self.password = ud.pwd
                    self.server = ud.server
                    exit_key100 = 0
        except socket.gaierror:
            tk.messagebox.showinfo(title="Username/Password/Server Error", message=f'Password/Username/Server Invalid Please Try again')
        except ConnectionRefusedError:
            tk.messagebox.showinfo(title="Username/Password/Server Error", message=f'Password/Username/Server Invalid Please Try again')

        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.



    def check_new(self):
        self.after(1000, self.check_new)
        self.profile.retrieve_unread_messages()
        new_messages = self.profile.unread_messages
        for name in new_messages:
            for text in new_messages[name]:
                if name == self.recipient:
                    self.body.entry_editor.delete(1.0, tk.END)
                    self.body.insert_contact_message(text['message'])
                    self.recipient_selected(self.recipient)
                if name != None and name != self.recipient and name not in self.messages_recieved:
                    self.body.insert_contact(name)
        self.profile.unread_messages = {}
        self.profile.save_profile(self.new_file)





    def create_file(self):
        self.new_file = None
        file_path = tk.simpledialog.askstring(title='File Creator', prompt='Please enter the File Path to the Directory for where you would like your file to be in (Do not include New file name).')
        if file_path == None:
            exit()
        file_name = tk.simpledialog.askstring(title='File Creator', prompt='Please enter the File Name')
        if file_name == None:
            exit()
        file_path = pathlib.Path(file_path)
        if file_path.exists():
            self.new_file = file_path / f"{file_name}.dsu"
            self.new_file.touch()
            exit_key5 = 1
            while exit_key5 != 0:
                server = tk.simpledialog.askstring(title='Account Creator', prompt='Please enter a Server')
                if server == None:
                    exit()
                username = tk.simpledialog.askstring(title='Account Creator', prompt='Please enter a Username')
                if username == None:
                    exit()
                password = tk.simpledialog.askstring(title='Account Creator', prompt='Please enter a Password')
                if password == None:
                    exit()
                SERVER = server
                PORT = 3021
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                        client.connect((SERVER, PORT))
                        send = client.makefile("w")
                        recv = client.makefile("r")
                        msg = json.dumps({"join": {"username": username, "password": password, "token": ""}})
                        send.write(msg + "\r\n")
                        send.flush()
                        srv_msg = recv.readline()
                        srv_msg_checker = json.loads(srv_msg)
                        if srv_msg_checker["response"]["type"] == "error":
                            tk.messagebox.showinfo(title="Username/Password/Server Error", message=f'Password/Username/Server Invalid Please Try again')
                        else:
                            self.profile = Profile(server, username, password)
                            self.username = self.profile.username
                            self.password = self.profile.password
                            self.server = self.profile.dsuserver
                            self.messages_sent = self.profile.messages_sent
                            self.messages_recieved = self.profile.messages_recieved
                            self.unread_messages = self.profile.unread_messages
                            self.list_of_contacts = self.profile.list_of_contacts
                            self.recipient = None
                            self.root = self.root
                            self._draw()
                            exit_key5 = 0
                except socket.gaierror:
                    tk.messagebox.showinfo(title="Username/Password/Server Error", message=f'Password/Username/Server Invalid Please Try again')
                except ConnectionRefusedError:
                    tk.messagebox.showinfo(title="Username/Password/Server Error", message=f'Password/Username/Server Invalid Please Try again')
        else:
            tk.messagebox.showerror(title="File Path Error", message='Entered An invalid Path, Please try again')

    def load_file(self):
        exit_key3 = 1
        while exit_key3 != 0:
            profile = Profile()
            self.new_file = None
            file_path = tk.simpledialog.askstring(title='File Creator', prompt='Please enter a valid dsu file path.')
            file_path = pathlib.Path(file_path)
            if file_path.exists():
                self.new_file = file_path
                self.profile2 = Profile()
                self.profile2.load_profile(self.new_file)
                self.username = self.profile2.username
                self.password = self.profile2.password
                self.server = self.profile2.dsuserver
                self.messages_sent = self.profile2.messages_sent
                self.messages_recieved = self.profile2.messages_recieved
                self.unread_messages = self.profile2.unread_messages
                self.list_of_contacts = self.profile2.list_of_contacts
                self.recipient = None
                self.root = self.root
                for name in self.list_of_contacts:
                    self.body.insert_contact(name)
                tk.messagebox.showinfo(title="File Succesfully opened", message=f'Login Succesful, Welcome {self.username}')
                exit_key3 = 0
                self._draw()
            else:
                tk.messagebox.showerror(title="File Path Error", message='Entered An invalid Path, Please try again')
    

    def close_file(self):
        self.profile = Profile(self.server, self.username, self.password)
        self.profile.messages_sent = self.messages_sent
        self.profile.messages_recieved = self.messages_recieved
        self.profile.unread_messages = self.unread_messages
        self.profile.list_of_contacts = self.list_of_contacts
        self.profile.save_profile(self.new_file)
        tk.messagebox.showinfo(title="File Closure", message=f'File Succesfully Saved and Closed')
        exit()


    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.create_file)
        menu_file.add_command(label='Open...', command=self.load_file)
        menu_file.add_command(label='Close', command=self.close_file)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
