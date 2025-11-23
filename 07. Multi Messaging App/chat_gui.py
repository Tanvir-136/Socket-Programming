import socket
import struct
import threading
import queue
import tkinter as tk
from tkinter import ttk, font
from datetime import datetime

# --- Network Configuration ---
# Multicast group and port that all clients will use to send/receive messages.
MCAST_GROUP = "224.1.1.1"
MCAST_PORT = 10000
BUFFER_SIZE = 1024

# --- Visual Theme (Dark Mode) ---
# Centralized color palette used throughout the UI for consistent styling.
COLORS = {
    "bg": "#1e1e1e",
    "sidebar": "#252526",
    "chat_bg": "#1e1e1e",
    "input_bg": "#3e3e42",
    "text": "#ffffff",
    "self_bubble": "#007acc",
    "other_bubble": "#333333",
    "system_text": "#4caf50",
    "accent": "#007acc",
}

class ChatClient:
    # Main class that encapsulates UI, networking, and message handling.
    def __init__(self, root):
        # Initialize application state and build the login UI.
        self.root = root
        self.root.title("LAN Messenger")
        self.root.geometry("700x500")
        self.root.configure(bg=COLORS["bg"])

        self.username = ""
        self.running = True
        self.sock = None
        self.msg_queue = queue.Queue()  # Thread-safe queue to pass messages from network thread to GUI.
        self.active_users = set()       # Track online users.

        self._setup_styles()
        self.build_login_ui()

    def _setup_styles(self):
        # Configure fonts and ttk styles used by the application.
        self.font_ui = font.Font(family="Segoe UI", size=10)
        self.font_msg = font.Font(family="Segoe UI", size=11)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Vertical.TScrollbar",
            background=COLORS["sidebar"],
            troughcolor=COLORS["bg"],
            borderwidth=0,
            arrowsize=0,
        )

    # --- UI BUILDERS ---
    def build_login_ui(self):
        # Create the initial login screen where user enters their display name.
        self.frame_login = tk.Frame(self.root, bg=COLORS["bg"])
        self.frame_login.pack(fill="both", expand=True)

        tk.Label(
            self.frame_login,
            text="Join Group",
            font=("Segoe UI", 20, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["text"],
        ).pack(pady=(120, 20))

        self.entry_user = tk.Entry(
            self.frame_login,
            font=("Segoe UI", 12),
            bg=COLORS["input_bg"],
            fg=COLORS["text"],
            bd=0,
            insertbackground="white",
            justify="center",
        )
        self.entry_user.pack(ipady=10, ipadx=20)
        self.entry_user.bind("<Return>", self.start_chat)
        self.entry_user.focus()

        tk.Button(
            self.frame_login,
            text="CONNECT",
            command=self.start_chat,
            bg=COLORS["accent"],
            fg="white",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            activebackground="#005f9e",
        ).pack(pady=20, ipadx=20, ipady=5)

    def build_main_ui(self):
        # Replace login UI with the main chat layout:
        # right sidebar for online users and left main pane for messages + input.
        self.frame_login.destroy()

        # 1. Sidebar (User List) - Right Side
        sidebar = tk.Frame(self.root, bg=COLORS["sidebar"], width=180)
        sidebar.pack(side="right", fill="y")
        sidebar.pack_propagate(False)  # Force width

        tk.Label(
            sidebar,
            text="ONLINE USERS",
            bg=COLORS["sidebar"],
            fg="#888888",
            font=("Segoe UI", 8, "bold"),
        ).pack(pady=(15, 10), anchor="w", padx=15)

        self.user_listbox = tk.Listbox(
            sidebar,
            bg=COLORS["sidebar"],
            fg=COLORS["text"],
            bd=0,
            font=("Segoe UI", 10),
            selectbackground=COLORS["sidebar"],
            activestyle="none",
            highlightthickness=0,
        )
        self.user_listbox.pack(fill="both", expand=True, padx=10)

        # 2. Chat Area - Left Side
        main_frame = tk.Frame(self.root, bg=COLORS["chat_bg"])
        main_frame.pack(side="left", fill="both", expand=True)

        # Chat Canvas and message frame inside to allow scrolling of message bubbles.
        self.canvas = tk.Canvas(main_frame, bg=COLORS["chat_bg"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(
            main_frame, orient="vertical", command=self.canvas.yview
        )
        self.msg_frame = tk.Frame(self.canvas, bg=COLORS["chat_bg"])

        # Ensure canvas scrollregion updates when new messages are added.
        self.msg_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window(
            (0, 0), window=self.msg_frame, anchor="nw", width=500
        )  # Initial width
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        # Input Bar at bottom for composing messages.
        input_container = tk.Frame(main_frame, bg=COLORS["bg"], pady=10)
        input_container.pack(side="bottom", fill="x")

        self.input_entry = tk.Entry(
            input_container,
            bg=COLORS["input_bg"],
            fg="white",
            bd=0,
            font=("Segoe UI", 11),
            insertbackground="white",
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=10, ipady=8)
        self.input_entry.bind("<Return>", self.send_chat_msg)
        self.input_entry.focus()

        send_btn = tk.Button(
            input_container,
            text="➤",
            command=self.send_chat_msg,
            bg=COLORS["accent"],
            fg="white",
            bd=0,
            font=("Segoe UI", 12),
        )
        send_btn.pack(side="right", padx=10, ipadx=10)

    # --- LOGIC ---
    def start_chat(self, event=None):
        # Triggered when user enters a name and joins: set username, build UI,
        # setup networking, announce presence, and begin processing queued messages.
        name = self.entry_user.get().strip()
        if not name:
            return
        self.username = name

        self.build_main_ui()
        self.setup_network()

        # Add self to local user list and announce join to the multicast group.
        self.update_user_list(self.username, add=True)
        self.send_packet(f"__JOIN__:{self.username}")

        # Start periodic processing of incoming messages from the queue.
        self.process_incoming()

    def setup_network(self):
        # Create UDP multicast socket, bind to port and join multicast group.
        # Start a background receiver thread to listen for incoming packets.
        try:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
            )
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("", MCAST_PORT))
            mreq = struct.pack("4sl", socket.inet_aton(MCAST_GROUP), socket.INADDR_ANY)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

            threading.Thread(target=self.receiver, daemon=True).start()
        except Exception as e:
            print(f"Net Error: {e}")

    def receiver(self):
        # Background thread: block on recvfrom and parse received protocol messages.
        # Put parsed events into the thread-safe msg_queue for the main thread to handle.
        while self.running:
            try:
                data, _ = self.sock.recvfrom(BUFFER_SIZE)
                msg = data.decode()

                # --- PROTOCOL HANDLING ---
                # Handle join notifications, presence replies, leaves, and normal chat lines.
                if msg.startswith("__JOIN__:"):
                    # Someone announced they joined; inform UI and reply with presence.
                    new_user = msg.split(":")[1]
                    self.msg_queue.put(("system", f"{new_user} joined"))
                    self.msg_queue.put(("user_add", new_user))

                    # Reply to the joining peer so they see me in their list as well.
                    if new_user != self.username:
                        self.send_packet(f"__PRESENCE__:{self.username}")

                elif msg.startswith("__PRESENCE__:"):
                    # Received presence reply from an existing user.
                    existing_user = msg.split(":")[1]
                    self.msg_queue.put(("user_add", existing_user))

                elif msg.startswith("__LEAVE__:"):
                    # A user is leaving; update UI accordingly.
                    leaving_user = msg.split(":")[1]
                    self.msg_queue.put(("system", f"{leaving_user} left"))
                    self.msg_queue.put(("user_remove", leaving_user))

                elif ": " in msg:
                    # Normal chat message in format "sender: message".
                    sender, content = msg.split(": ", 1)
                    tag = "self" if sender == self.username else "other"
                    self.msg_queue.put(("chat", sender, content, tag))

            except OSError:
                # Socket closed or other fatal error — exit receiver loop.
                break

    def process_incoming(self):
        # Periodically called on the main thread to process events queued by the receiver.
        while not self.msg_queue.empty():
            type_, *data = self.msg_queue.get()

            if type_ == "chat":
                # data: sender, content, tag
                self.render_bubble(data[0], data[1], data[2])
            elif type_ == "system":
                # Render system notifications (joins/leaves).
                self.render_system(data[0])
            elif type_ == "user_add":
                # Add a username to the online set and refresh the list.
                self.update_user_list(data[0], add=True)
            elif type_ == "user_remove":
                # Remove a username from the online set and refresh the list.
                self.update_user_list(data[0], add=False)

        # Continue scheduling updates while the app is running.
        if self.running:
            self.root.after(100, self.process_incoming)

    def update_user_list(self, user, add=True):
        # Manage the active_users set and refresh the Listbox to reflect current users.
        if add:
            self.active_users.add(user)
        else:
            self.active_users.discard(user)

        # Refresh Listbox contents in sorted order for predictability.
        self.user_listbox.delete(0, "end")
        for u in sorted(self.active_users):
            prefix = "🟢 " if u != self.username else "👤 "
            self.user_listbox.insert("end", f" {prefix}{u}")

    def send_chat_msg(self, event=None):
        # Get the typed message, send it over multicast and clear the input.
        txt = self.input_entry.get().strip()
        if not txt:
            return
        self.send_packet(f"{self.username}: {txt}")
        self.input_entry.delete(0, "end")

    def send_packet(self, txt):
        # Encode and send a UDP packet to the multicast group.
        if self.sock:
            self.sock.sendto(txt.encode(), (MCAST_GROUP, MCAST_PORT))

    def render_bubble(self, sender, message, tag):
        # Create a visually distinct "bubble" for each message in the chat area.
        row = tk.Frame(self.msg_frame, bg=COLORS["chat_bg"])
        row.pack(fill="x", pady=5)

        bg = COLORS["self_bubble"] if tag == "self" else COLORS["other_bubble"]
        anchor = "e" if tag == "self" else "w"

        # Show sender name above messages from others.
        if tag == "other":
            tk.Label(
                row,
                text=sender,
                font=("Segoe UI", 7, "bold"),
                bg=COLORS["chat_bg"],
                fg="#888",
            ).pack(anchor="w", padx=5)

        # The message label acts as the bubble itself.
        bubble = tk.Label(
            row,
            text=message,
            bg=bg,
            fg="white",
            font=("Segoe UI", 10),
            padx=12,
            pady=8,
            wraplength=350,
            justify="left",
        )
        bubble.pack(anchor=anchor, padx=5)

        # Auto-scroll to the latest message.
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def render_system(self, text):
        # Render small, colored system notifications in the chat area.
        tk.Label(
            self.msg_frame,
            text=text,
            bg=COLORS["chat_bg"],
            fg=COLORS["system_text"],
            font=("Segoe UI", 8),
        ).pack(pady=5)
        self.canvas.yview_moveto(1.0)

    def on_close(self):
        # Clean shutdown: announce leaving, close socket and destroy the GUI.
        self.running = False
        try:
            self.send_packet(f"__LEAVE__:{self.username}")
            self.sock.close()
        except:
            pass
        self.root.destroy()


if __name__ == "__main__":
    # Application entry point: create Tk root, instantiate client and run mainloop.
    root = tk.Tk()
    app = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()