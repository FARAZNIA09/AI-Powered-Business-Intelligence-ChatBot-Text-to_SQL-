import customtkinter as ctk
import json
import os
import requests
from tkinter import ttk

# =========================================================
# APP GLOBAL CONFIGURATION & SETTINGS
# =========================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Fastapi local server connection endpoint
API_URL = "http://127.0.0.1:8000/query"

# User registry & chat history file persistent storage definitions
USER_DB_FILE = "users_auth.json"
HISTORY_DB_FILE = "chat_history.json"

# Dynamic UI palette combinations
BG_COLOR = "#0B1120"
SIDEBAR_COLOR = "#0F172A"
CARD_COLOR = "#111827"
ACCENT = "#2563EB"
ACCENT_HOVER = "#1D4ED8"
TEXT = "#F9FAFB"
SECONDARY = "#94A3B8"
BORDER = "#1E3A8A"
VAL_COLOR = ACCENT  # Fixed chart vector text data label color variable

# Verify localized credential database configuration profiles
if not os.path.exists(USER_DB_FILE):
    with open(USER_DB_FILE, "w") as f:
        json.dump({"admin": "admin123"}, f)

# =========================================================
# PERSISTENT SESSION CHAT HISTORY STORAGE UTILITIES
# =========================================================
def load_user_history_from_disk(username):
    if not os.path.exists(HISTORY_DB_FILE):
        return []
    try:
        with open(HISTORY_DB_FILE, "r") as f:
            data = json.load(f)
            return data.get(username, [])
    except Exception:
        return []

def save_user_query_to_disk(username, query_string):
    try:
        data = {}
        if os.path.exists(HISTORY_DB_FILE):
            with open(HISTORY_DB_FILE, "r") as f:
                data = json.load(f)
        if username not in data:
            data[username] = []
        if query_string not in data[username]:
            data[username].append(query_string)
        with open(HISTORY_DB_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Failed to persist sync profile log: {e}")

# =========================================================
# SYSTEM STAGE ROOT APPLICATION CLASS
# =========================================================
class DataChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AI-Powered Business Intelligence Chatbot")
        self.geometry("1550x900")
        self.minsize(1400, 800)
        self.configure(fg_color=BG_COLOR)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.current_user = None
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_current_frame()
        self.auth_frame = LoginFrame(self, self.on_login_success, self.show_register_screen)
        self.auth_frame.grid(row=0, column=0, sticky="nsew")

    def show_register_screen(self):
        self.clear_current_frame()
        self.auth_frame = RegisterFrame(self, self.show_login_screen)
        self.auth_frame.grid(row=0, column=0, sticky="nsew")

    def on_login_success(self, username):
        self.current_user = username
        self.clear_current_frame()
        self.dashboard_frame = MainDashboardFrame(self, self.current_user, self.handle_logout)
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")

    def handle_logout(self):
        self.current_user = None
        self.show_login_screen()

    def clear_current_frame(self):
        for widget in self.winfo_children():
            widget.grid_forget()

# =========================================================
# SECURITY SYSTEM SIGN IN ACCESS CONTROLLER
# =========================================================
class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, login_callback, register_switch_callback):
        super().__init__(parent, fg_color=BG_COLOR)
        self.login_callback = login_callback
        self.register_switch_callback = register_switch_callback
        
        box = ctk.CTkFrame(self, width=420, height=480, fg_color=SIDEBAR_COLOR, corner_radius=20, border_width=1, border_color=BORDER)
        box.place(relx=0.5, rely=0.5, anchor="center")
        box.pack_propagate(False)
        
        ctk.CTkLabel(box, text="Sign In", font=("Segoe UI", 28, "bold"), text_color=TEXT).pack(pady=(40, 5))
        ctk.CTkLabel(box, text="Access your Data Analytics Dashboard", font=("Segoe UI", 14), text_color=SECONDARY).pack(pady=(0, 30))
        
        self.username_input = ctk.CTkEntry(box, width=320, height=48, corner_radius=10, placeholder_text="Username", fg_color=BG_COLOR, border_color=BORDER)
        self.username_input.pack(pady=10)
        
        self.password_input = ctk.CTkEntry(box, width=320, height=48, corner_radius=10, placeholder_text="Password", show="*", fg_color=BG_COLOR, border_color=BORDER)
        self.password_input.pack(pady=10)
        
        self.error_lbl = ctk.CTkLabel(box, text="", font=("Segoe UI", 12), text_color="#EF4444")
        self.error_lbl.pack(pady=5)
        
        ctk.CTkButton(box, text="Login", width=320, height=48, corner_radius=10, fg_color=ACCENT, hover_color=ACCENT_HOVER, font=("Segoe UI", 15, "bold"), command=self.verify_credentials).pack(pady=15)
        ctk.CTkButton(box, text="Create an Account", width=320, height=30, fg_color="transparent", text_color=ACCENT, font=("Segoe UI", 13), hover=False, command=self.register_switch_callback).pack(pady=5)

    def verify_credentials(self):
        user = self.username_input.get().strip()
        pwd = self.password_input.get()
        
        with open(USER_DB_FILE, "r") as f:
            users = json.load(f)
            
        if user in users and users[user] == pwd:
            self.login_callback(user)
        else:
            self.error_lbl.configure(text="Invalid Username or Password")

# =========================================================
# NEW USER ACCOUNT SECURITY REGISTRY PROVIDER
# =========================================================
class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent, login_switch_callback):
        super().__init__(parent, fg_color=BG_COLOR)
        self.login_switch_callback = login_switch_callback
        
        box = ctk.CTkFrame(self, width=420, height=520, fg_color=SIDEBAR_COLOR, corner_radius=20, border_width=1, border_color=BORDER)
        box.place(relx=0.5, rely=0.5, anchor="center")
        box.pack_propagate(False)
        
        ctk.CTkLabel(box, text="Register Account", font=("Segoe UI", 28, "bold"), text_color=TEXT).pack(pady=(35, 5))
        ctk.CTkLabel(box, text="Set up credentials for secure database querying", font=("Segoe UI", 13), text_color=SECONDARY).pack(pady=(0, 25))
        
        self.username_input = ctk.CTkEntry(box, width=320, height=48, corner_radius=10, placeholder_text="Choose Username", fg_color=BG_COLOR, border_color=BORDER)
        self.username_input.pack(pady=10)
        
        self.password_input = ctk.CTkEntry(box, width=320, height=48, corner_radius=10, placeholder_text="Create Password", show="*", fg_color=BG_COLOR, border_color=BORDER)
        self.password_input.pack(pady=10)
        
        self.confirm_input = ctk.CTkEntry(box, width=320, height=48, corner_radius=10, placeholder_text="Confirm Password", show="*", fg_color=BG_COLOR, border_color=BORDER)
        self.confirm_input.pack(pady=10)
        
        self.error_lbl = ctk.CTkLabel(box, text="", font=("Segoe UI", 12), text_color="#EF4444")
        self.error_lbl.pack(pady=5)
        
        ctk.CTkButton(box, text="Register Now", width=320, height=48, corner_radius=10, fg_color="#10B981", hover_color="#059669", font=("Segoe UI", 15, "bold"), command=self.register_user).pack(pady=15)
        ctk.CTkButton(box, text="Back to Login", width=320, height=30, fg_color="transparent", text_color=ACCENT, font=("Segoe UI", 13), hover=False, command=self.login_switch_callback).pack(pady=5)

    def register_user(self):
        user = self.username_input.get().strip()
        pwd = self.password_input.get()
        conf = self.confirm_input.get()
        
        if not user or not pwd:
            self.error_lbl.configure(text="Fields cannot be left blank.")
            return
        if pwd != conf:
            self.error_lbl.configure(text="Passwords do not match!")
            return
            
        with open(USER_DB_FILE, "r") as f:
            users = json.load(f)
            
        if user in users:
            self.error_lbl.configure(text="Username already active.")
            return
            
        users[user] = pwd
        with open(USER_DB_FILE, "w") as f:
            json.dump(users, f)
            
        self.login_switch_callback()

# =========================================================
# CENTRAL ENTERPRISE APPLICATION GRID WORKSPACE CONTAINER
# =========================================================
class MainDashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, user_session, logout_command):
        super().__init__(parent, fg_color=BG_COLOR)
        self.user_session = user_session
        self.logout_command = logout_command
        self.sidebar_buttons = {}
        
        # Pull history records assigned specifically tracking this logged-in individual
        self.chat_history_records = [{"query": q} for q in load_user_history_from_disk(self.user_session)]
        
        # Grid layout management architecture setup properties
        self.sidebar_visible = True
        self.grid_columnconfigure(0, weight=0, minsize=260) 
        self.grid_columnconfigure(1, weight=1)              
        self.grid_rowconfigure(0, weight=1)
        
        # Left Main Side Menu Navigation Canvas Window
        self.sidebar_frame = ctk.CTkFrame(self, width=260, fg_color=SIDEBAR_COLOR, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        self.build_sidebar()
        
        # Right Dynamic Container Workspace Panel Block
        self.main_content_area = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.main_content_area.grid(row=0, column=1, sticky="nsew")
        self.main_content_area.grid_columnconfigure(0, weight=1)
        self.main_content_area.grid_rowconfigure(1, weight=1)
        
        self.build_topbar()
        self.switch_view("Chatbot") 
        self.build_statusbar()

    def build_sidebar(self):
        ctk.CTkLabel(self.sidebar_frame, text="AI Database Chatbot", font=("Segoe UI", 22, "bold"), text_color=TEXT).pack(pady=(35, 30), padx=20, anchor="w")
        
        menu_items = [
            ("💬  Chatbot", "Chatbot"),
            ("🗄️  Data Sources", "Data Sources"),
            ("⚙️  Admin Panel", "Admin Panel")
        ]
        
        for display_text, view_key in menu_items:
            btn = ctk.CTkButton(
                self.sidebar_frame, text=display_text, width=220, height=46, corner_radius=12,
                fg_color="transparent", hover_color=ACCENT_HOVER, text_color=TEXT,
                font=("Segoe UI", 14), anchor="w",
                command=lambda k=view_key: self.switch_view(k)
            )
            btn.pack(pady=5, padx=15)
            self.sidebar_buttons[view_key] = btn
            
        ctk.CTkLabel(self.sidebar_frame, text="📜 CHAT HISTORY", font=("Segoe UI", 12, "bold"), text_color=SECONDARY).pack(pady=(30, 8), padx=25, anchor="w")
        
        self.history_scroll_area = ctk.CTkScrollableFrame(self.sidebar_frame, fg_color="#0A0F1D", height=320, corner_radius=10, border_width=1, border_color="#1E293B")
        self.history_scroll_area.pack(fill="x", padx=15, pady=5)
        
        self.render_history_sidebar_logs()
        
        ctk.CTkLabel(self.sidebar_frame, text=f"User: {self.user_session}", font=("Segoe UI", 12), text_color=SECONDARY).pack(side="bottom", pady=(0, 15))

    def render_history_sidebar_logs(self):
        for w in self.history_scroll_area.winfo_children():
            w.destroy()
            
        if not self.chat_history_records:
            lbl = ctk.CTkLabel(self.history_scroll_area, text="No queries logged yet.", font=("Segoe UI", 12, "italic"), text_color=SECONDARY)
            lbl.pack(pady=15)
            return
            
        for item in reversed(self.chat_history_records):
            truncated_text = item["query"][:24] + "..." if len(item["query"]) > 24 else item["query"]
            hist_btn = ctk.CTkButton(
                self.history_scroll_area, text=f"• {truncated_text}", 
                font=("Segoe UI", 11), text_color=TEXT, fg_color="transparent", 
                anchor="w", height=28, hover_color="#1E293B",
                command=lambda q=item["query"]: self.trigger_historical_replay(q)
            )
            hist_btn.pack(fill="x", pady=2)

    def trigger_historical_replay(self, query_string):
        self.switch_view("Chatbot")
        self.chatbot_view_frame.prompt_entry.delete(0, "end")
        self.chatbot_view_frame.prompt_entry.insert(0, query_string)
        self.chatbot_view_frame.dispatch_query()

    def build_topbar(self):
        self.topbar = ctk.CTkFrame(self.main_content_area, height=80, fg_color=SIDEBAR_COLOR, corner_radius=18)
        self.topbar.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        self.topbar.pack_propagate(False)
        
        # Dynamic side panel folding visibility utility button controller
        self.toggle_btn = ctk.CTkButton(
            self.topbar, text="◀ Hide Menu", width=110, height=38, corner_radius=10,
            fg_color="#1E293B", hover_color="#334155", font=("Segoe UI", 12, "bold"),
            command=self.toggle_sidebar_visibility
        )
        self.toggle_btn.pack(side="left", padx=20)
        
        self.topbar_title = ctk.CTkLabel(self.topbar, text="AI-Powered Workspace Engine", font=("Segoe UI", 22, "bold"), text_color=TEXT)
        self.topbar_title.pack(side="left", padx=10)
        
        profile_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        profile_frame.pack(side="right", padx=20)
        
        ctk.CTkLabel(profile_frame, text=f"👤 {self.user_session.title()}", font=("Segoe UI", 14, "bold")).pack(side="left", padx=10)
        ctk.CTkButton(profile_frame, text="Logout", width=85, height=32, corner_radius=10, fg_color="#EF4444", hover_color="#DC2626", font=("Segoe UI", 12, "bold"), command=self.logout_command).pack(side="left")

    def toggle_sidebar_visibility(self):
        if self.sidebar_visible:
            self.sidebar_frame.grid_forget()
            self.grid_columnconfigure(0, weight=0, minsize=0)
            self.toggle_btn.configure(text="▶ Show Menu")
            self.sidebar_visible = False
        else:
            self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
            self.grid_columnconfigure(0, weight=0, minsize=260)
            self.toggle_btn.configure(text="◀ Hide Menu")
            self.sidebar_visible = True

    def build_statusbar(self):
        status_bar = ctk.CTkFrame(self, height=35, fg_color="#020617", corner_radius=0)
        status_bar.place(relx=0, rely=1, relwidth=1, anchor="sw")
        ctk.CTkLabel(status_bar, text="Status: Connected to local MS SQL Server Instance & FastAPI API Service Node", font=("Segoe UI", 12), text_color=SECONDARY).pack(side="left", padx=20)
        ctk.CTkLabel(status_bar, text="System Production Build: v1.5.0", font=("Segoe UI", 12), text_color=SECONDARY).pack(side="right", padx=20)

    def switch_view(self, target_key):
        for key, btn in self.sidebar_buttons.items():
            if key == target_key:
                btn.configure(fg_color=ACCENT, font=("Segoe UI", 14, "bold"))
            else:
                btn.configure(fg_color="transparent", font=("Segoe UI", 14, "normal"))
                
        for w in self.main_content_area.winfo_children():
            if w != self.topbar:
                w.grid_forget()
                
        if target_key == "Chatbot":
            self.topbar_title.configure(text="AI-Powered Business Intelligence Assistant Chatbot")
            self.chatbot_view_frame = ChatbotWorkspaceView(self.main_content_area, self)
            self.chatbot_view_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
            
        elif target_key == "Data Sources":
            self.topbar_title.configure(text="Relational Database Connection Strings Management Data Source")
            frame = DataSourcesWorkspaceView(self.main_content_area)
            frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
            
        elif target_key == "Admin Panel":
            self.topbar_title.configure(text="Central Admin Security Privileges Account Registry Control")
            frame = AdminWorkspaceView(self.main_content_area)
            frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

    def log_query_to_history(self, raw_query_string):
        if not any(h["query"] == raw_query_string for h in self.chat_history_records):
            self.chat_history_records.append({"query": raw_query_string})
            save_user_query_to_disk(self.user_session, raw_query_string)
            self.render_history_sidebar_logs()


# =========================================================
# SUB-VIEW: CHAT INTERFACE & RESIZABLE LOGIC CANVAS
# =========================================================
class ChatbotWorkspaceView(ctk.CTkFrame):
    def __init__(self, parent, main_dashboard_ref):
        super().__init__(parent, fg_color="transparent")
        self.dashboard_ref = main_dashboard_ref
        
        # Track left/right column weight scaling ratios
        self.left_weight = 3.0
        self.right_weight = 2.0
        self.apply_flexible_workspace_proportions()
        self.grid_rowconfigure(0, weight=1)
        
        # -------------------------------------------------------------
        # LEFT PANEL CONTENT ASSEMBLY MOUNTING
        # -------------------------------------------------------------
        self.chat_panel = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=16, border_width=1, border_color=BORDER)
        self.chat_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.chat_panel.grid_rowconfigure(1, weight=1)
        self.chat_panel.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.chat_panel, text="Enterprise Chat Data Engine Pipeline", font=("Segoe UI", 18, "bold"), text_color=TEXT).grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        self.dialog_scroll = ctk.CTkScrollableFrame(self.chat_panel, fg_color="#0B1220", corner_radius=12, border_width=1, border_color=BORDER)
        self.dialog_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 15))
        
        input_wrapper = ctk.CTkFrame(self.chat_panel, fg_color="transparent")
        input_wrapper.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        input_wrapper.grid_columnconfigure(0, weight=1)
        
        self.prompt_entry = ctk.CTkEntry(input_wrapper, height=52, corner_radius=10, border_width=1, border_color=BORDER, fg_color="#0B1220", placeholder_text="Ask business questions like: 'Top 5 product by sales'...", font=("Segoe UI", 14))
        self.prompt_entry.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        self.prompt_entry.bind("<Return>", lambda e: self.dispatch_query())
        
        ctk.CTkButton(input_wrapper, text="Run Analysis", width=130, height=52, corner_radius=10, fg_color=ACCENT, hover_color=ACCENT_HOVER, font=("Segoe UI", 14, "bold"), command=self.dispatch_query).grid(row=0, column=1)

        # -------------------------------------------------------------
        # ADJUSTABLE SEPARATOR GRIP SLIDER SPLIT AXIS
        # -------------------------------------------------------------
        slider_axis = ctk.CTkFrame(self, fg_color="transparent", width=20)
        slider_axis.grid(row=0, column=1, sticky="ns")
        
        ctk.CTkLabel(slider_axis, text="⬌", font=("Segoe UI", 16, "bold"), text_color=SECONDARY).pack(expand=True)
        self.panel_slider = ctk.CTkSlider(
            slider_axis, from_=1.0, to=5.0, number_of_steps=100, orientation="vertical", width=16,
            command=self.on_workspace_slider_move
        )
        self.panel_slider.pack(fill="y", expand=True, pady=10)
        self.panel_slider.set(2.0) 

        # -------------------------------------------------------------
        # RIGHT PANEL CONTENT ASSEMBLY MOUNTING
        # -------------------------------------------------------------
        self.right_chart_panel = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=16, border_width=1, border_color=BORDER)
        self.right_chart_panel.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        
        ctk.CTkLabel(self.right_chart_panel, text="📊 Dynamic Query Visualization", font=("Segoe UI", 18, "bold"), text_color=TEXT).pack(anchor="w", padx=20, pady=(20, 5))
        self.chart_subtitle = ctk.CTkLabel(self.right_chart_panel, text="No query data processed yet.", font=("Segoe UI", 12), text_color=SECONDARY)
        self.chart_subtitle.pack(anchor="w", padx=20, pady=(0, 10))

        self.tabs_bar = ctk.CTkFrame(self.right_chart_panel, fg_color="transparent")
        self.tabs_bar.pack(fill="x", padx=20, pady=5)
        
        self.selected_chart_type = "Bar Chart"
        self.latest_dataset_columns = []
        self.latest_dataset_matrix = []

        self.tab_btns = {}
        for view_name in ["Bar Chart", "Line Chart", "Histogram"]:
            btn = ctk.CTkButton(
                self.tabs_bar, text=view_name, width=90, height=28, corner_radius=6,
                fg_color=ACCENT if view_name == self.selected_chart_type else "transparent", 
                hover_color="#1E293B", text_color=TEXT, font=("Segoe UI", 11),
                command=lambda v=view_name: self.change_chart_type(v)
            )
            btn.pack(side="left", padx=4)
            self.tab_btns[view_name] = btn

        self.chart_canvas = ctk.CTkCanvas(self.right_chart_panel, bg="#0B1220", highlightthickness=0, bd=0)
        self.chart_canvas.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        self.append_bubble("System Engine", "API Connection Established. Run numerical queries to map real-time data onto graphs.")

    def apply_flexible_workspace_proportions(self):
        self.grid_columnconfigure(0, weight=int(self.left_weight * 10))
        self.grid_columnconfigure(1, weight=0) 
        self.grid_columnconfigure(2, weight=int(self.right_weight * 10))

    def on_workspace_slider_move(self, value):
        self.right_weight = float(value)
        self.left_weight = 6.0 - float(value)
        self.apply_flexible_workspace_proportions()

    def select_best_chart_by_query_context(self, query_string):
        q = query_string.lower()
        if "trend" in q or "month" in q or "year" in q or "date" in q or "time" in q or "over" in q:
            best_match = "Line Chart"  
        elif "distribution" in q or "spread" in q or "range" in q or "frequency" in q or "bins" in q:
            best_match = "Histogram"   
        else:
            best_match = "Bar Chart"   
        self.change_chart_type(best_match)

    def change_chart_type(self, chart_type):
        self.selected_chart_type = chart_type
        for name, button in self.tab_btns.items():
            if name == chart_type:
                button.configure(fg_color=ACCENT, font=("Segoe UI", 11, "bold"))
            else:
                button.configure(fg_color="transparent", font=("Segoe UI", 11))
        self.draw_live_query_chart()

    def append_bubble(self, sender, message):
        bubble_bg = "#1E293B" if sender == "User" else "#1E3A8A"
        align = "e" if sender == "User" else "w"
        wrapper = ctk.CTkFrame(self.dialog_scroll, fg_color="transparent")
        wrapper.pack(fill="x", pady=6, padx=10)
        
        bubble = ctk.CTkFrame(wrapper, fg_color=bubble_bg, corner_radius=12)
        bubble.pack(side="right" if align == "e" else "left", padx=5)
        
        lbl = ctk.CTkLabel(bubble, text=f"{sender}:\n{message}", font=("Segoe UI", 13), text_color=TEXT, justify="left", wraplength=450)
        lbl.pack(padx=14, pady=8)
        self.dialog_scroll._parent_canvas.yview_moveto(1.0)

    def copy_to_clipboard(self, text_to_copy, button_widget):
        self.clipboard_clear()
        self.clipboard_append(text_to_copy)
        self.update()
        original_text = button_widget.cget("text")
        button_widget.configure(text="✔ Copied!", fg_color="#10B981")
        self.after(1400, lambda: button_widget.configure(text=original_text, fg_color="#1E293B"))

    def display_structured_grid(self, sql_string, headers, data_matrix):
        wrapper = ctk.CTkFrame(self.dialog_scroll, fg_color=CARD_COLOR, corner_radius=12, border_width=1, border_color=BORDER)
        wrapper.pack(fill="x", pady=10, padx=10)
        
        action_bar = ctk.CTkFrame(wrapper, fg_color="transparent", height=32)
        action_bar.pack(fill="x", padx=15, pady=(10, 0))
        
        ctk.CTkLabel(action_bar, text="🧾 Result Data Table Mapping", font=("Segoe UI", 12, "bold"), text_color=SECONDARY).pack(side="left")

        copy_table_btn = ctk.CTkButton(action_bar, text="📋 Copy Grid Data", width=110, height=26, corner_radius=6, fg_color="#1E293B", text_color=TEXT, font=("Segoe UI", 11, "bold"))
        copy_table_btn.pack(side="right", padx=5)
        formatted_table_string = "\t".join(headers) + "\n" + "\n".join(["\t".join(map(str, row)) for row in data_matrix])
        copy_table_btn.configure(command=lambda: self.copy_to_clipboard(formatted_table_string, copy_table_btn))

        copy_sql_btn = ctk.CTkButton(action_bar, text="📄 Copy SQL", width=90, height=26, corner_radius=6, fg_color="#1E293B", text_color=TEXT, font=("Segoe UI", 11, "bold"))
        copy_sql_btn.pack(side="right", padx=5)
        copy_sql_btn.configure(command=lambda: self.copy_to_clipboard(sql_string, copy_sql_btn))
        
        ctk.CTkLabel(wrapper, text=sql_string, font=("Consolas", 11), text_color="#6EE7B7", justify="left", anchor="w").pack(fill="x", padx=15, pady=(8, 10))
        
        table_container = ctk.CTkFrame(wrapper, fg_color="#0B1220", corner_radius=8)
        table_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#111827", fieldbackground="#111827", foreground=TEXT, borderwidth=0, font=("Segoe UI", 10), rowheight=26)
        style.configure("Treeview.Heading", background=BORDER, foreground=TEXT, font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[('selected', ACCENT)])
        
        tree = ttk.Treeview(table_container, columns=headers, show="headings", height=min(len(data_matrix), 5))
        for col in headers:
            tree.heading(col, text=str(col).upper())
            tree.column(col, width=120, minwidth=90, anchor="center")
        for row in data_matrix:
            tree.insert("", "end", values=row)
            
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        scrollbar.pack(side="right", fill="y", padx=(0, 5), pady=5)
        
        self.dialog_scroll._parent_canvas.yview_moveto(1.0)

    # -------------------------------------------------------------
    # CUSTOM COORDINATE GRAPH RENDERING ROUTINES ENGINE
    # -------------------------------------------------------------
    def draw_live_query_chart(self):
        self.chart_canvas.delete("all")
        self.update_idletasks()

        if not self.latest_dataset_matrix or len(self.latest_dataset_columns) < 2:
            return

        cols = self.latest_dataset_columns
        matrix = self.latest_dataset_matrix

        label_col_idx = 0
        value_col_idx = 1
        
        for idx, item in enumerate(matrix[0]):
            if isinstance(item, (int, float)):
                value_col_idx = idx
                label_col_idx = 0 if idx != 0 else 1
                break

        chart_data = []
        for row in matrix:
            try:
                lbl = str(row[label_col_idx])
                val = float(row[value_col_idx])
                chart_data.append((lbl, val))
            except (ValueError, TypeError, IndexError):
                continue

        if not chart_data:
            return

        self.chart_subtitle.configure(text=f"Plotting Metric attributes values mapping based on columns: '{cols[label_col_idx]}' vs '{cols[value_col_idx]}'")

        w = self.chart_canvas.winfo_width() if self.chart_canvas.winfo_width() > 100 else 500
        h = self.chart_canvas.winfo_height() if self.chart_canvas.winfo_height() > 100 else 400
        
        pad_l, pad_b, pad_r, pad_t = 65, 45, 30, 30
        graph_w = w - pad_l - pad_r
        graph_h = h - pad_b - pad_t

        max_val = max([item[1] for item in chart_data]) if max([item[1] for item in chart_data]) > 0 else 100
        max_val *= 1.15 

        self.chart_canvas.create_line(pad_l, h - pad_b, w - pad_r, h - pad_b, fill="#334155", width=2)
        self.chart_canvas.create_line(pad_l, pad_t, pad_l, h - pad_b, fill="#334155", width=2)

        for tier in [0.25, 0.5, 0.75, 1.0]:
            tier_val = max_val * tier
            ty = h - pad_b - (tier_val / max_val * graph_h)
            self.chart_canvas.create_line(pad_l, ty, w - pad_r, ty, fill="#1E293B", dash=(4, 4))
            self.chart_canvas.create_text(pad_l - 8, ty, text=f"{int(tier_val)}", fill=SECONDARY, font=("Segoe UI", 9), anchor="e")

        # 1. GRAPH RENDERING: BAR CHART
        if self.selected_chart_type == "Bar Chart":
            gap = 18
            num_elements = len(chart_data)
            bar_w = (graph_w - (gap * (num_elements + 1))) / num_elements
            
            for idx, (label, val) in enumerate(chart_data):
                x0 = pad_l + gap + idx * (bar_w + gap)
                y0 = h - pad_b - (val / max_val * graph_h)
                x1 = x0 + bar_w
                y1 = h - pad_b
                
                self.chart_canvas.create_rectangle(x0, y0, x1, y1, fill=VAL_COLOR, outline="")
                self.chart_canvas.create_text(x0 + bar_w/2, y0 - 10, text=f"{int(val)}", fill=TEXT, font=("Segoe UI", 9, "bold"))
                trunc_lbl = label[:10] + ".." if len(label) > 10 else label
                self.chart_canvas.create_text(x0 + bar_w/2, y1 + 15, text=trunc_lbl, fill=SECONDARY, font=("Segoe UI", 10))

        # 2. GRAPH RENDERING: LINE CHART
        elif self.selected_chart_type == "Line Chart":
            num_elements = len(chart_data)
            step_x = graph_w / (num_elements - 1) if num_elements > 1 else graph_w
            
            coords = []
            for idx, (label, val) in enumerate(chart_data):
                cx = pad_l + (idx * step_x)
                cy = h - pad_b - (val / max_val * graph_h)
                coords.append((cx, cy, label, val))
                
            for i in range(len(coords) - 1):
                self.chart_canvas.create_line(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1], fill="#10B981", width=3)
                
            for cx, cy, label, val in coords:
                self.chart_canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill="#34D399", outline=TEXT, width=1)
                self.chart_canvas.create_text(cx, cy - 14, text=f"{int(val)}", fill=TEXT, font=("Segoe UI", 9, "bold"))
                trunc_lbl = label[:10] + ".." if len(label) > 10 else label
                self.chart_canvas.create_text(cx, h - pad_b + 15, text=trunc_lbl, fill=SECONDARY, font=("Segoe UI", 10))

        # 3. GRAPH RENDERING: HISTOGRAM 
        elif self.selected_chart_type == "Histogram":
            num_elements = len(chart_data)
            bin_w = graph_w / num_elements
            
            for idx, (label, val) in enumerate(chart_data):
                x0 = pad_l + (idx * bin_w)
                y0 = h - pad_b - (val / max_val * graph_h)
                x1 = x0 + bin_w
                y1 = h - pad_b
                
                self.chart_canvas.create_rectangle(x0, y0, x1, y1, fill="#F59E0B", outline="#78350F", width=1)
                self.chart_canvas.create_text(x0 + bin_w/2, y0 - 10, text=f"{int(val)}", fill=TEXT, font=("Segoe UI", 9))
                trunc_lbl = label[:10] + ".." if len(label) > 10 else label
                self.chart_canvas.create_text(x0 + bin_w/2, y1 + 15, text=trunc_lbl, fill=SECONDARY, font=("Segoe UI", 10))

    def dispatch_query(self):
        query = self.prompt_entry.get().strip()
        if not query:
            return
            
        self.append_bubble("User", query)
        self.dashboard_ref.log_query_to_history(query) 
        self.prompt_entry.delete(0, "end")
        
        try:
            response = requests.post(API_URL, json={"user_query": query}, timeout=8)
            if response.status_code == 200:
                data = response.json()
                sql_output = data.get("generated_sql", "---")
                
                if data.get("is_df", False):
                    self.latest_dataset_columns = data.get("columns", [])
                    self.latest_dataset_matrix = data.get("data", [])
                    
                    self.append_bubble("AI Engine Assistant", "Query data resolved successfully from database records parameters matrix:")
                    self.display_structured_grid(sql_output, self.latest_dataset_columns, self.latest_dataset_matrix)
                    
                    self.select_best_chart_by_query_context(query)
                    self.draw_live_query_chart()
                else:
                    self.append_bubble("AI Engine Assistant", data.get("result", "No response description returned."))
            else:
                self.append_bubble("AI Engine Assistant", f"HTTP Error Node Response: {response.status_code}")
        except Exception as ex:
            self.append_bubble("AI Engine Assistant", f"Handshake Interrupted. Confirm FastAPI server terminal connection. Details: {str(ex)}")


# =========================================================
# SUB-VIEW: INFRASTRUCTURE MAPPING DASHBOARD PANEL
# =========================================================
class DataSourcesWorkspaceView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=CARD_COLOR, corner_radius=16, border_width=1, border_color=BORDER)
        
        ctk.CTkLabel(self, text="🗄️ Relational Data Infrastructure Connectivity Mapping", font=("Segoe UI", 20, "bold"), text_color=TEXT).pack(anchor="w", padx=30, pady=(25, 5))
        ctk.CTkLabel(self, text="Current environment driver configuration profile pointers mapped out of localized configuration scripts.", font=("Segoe UI", 13), text_color=SECONDARY).pack(anchor="w", padx=30, pady=(0, 20))
        
        wrapper = ctk.CTkFrame(self, fg_color="#0B1220", corner_radius=14, border_width=1, border_color=BORDER)
        wrapper.pack(fill="both", expand=True, padx=35, pady=(10, 30))
        
        ctk.CTkLabel(wrapper, text="Active Environment Target Configuration Profile", font=("Segoe UI", 16, "bold"), text_color=TEXT).pack(anchor="w", padx=25, pady=(20, 15))
        
        config_labels = [
            ("SQL Server Relational Hardware Host IP Instance Name:", "FARAZ-PC\\SQLEXPRESS03"),
            ("Target Database Logical Entity Space Name Mapping:", "chatbot_db"),
            ("Active User Credential Profile Handshake Profile Identity:", "faraz_user"),
            ("Windows OS Native Driver Client Interface Subsystem Version:", "ODBC Driver 17 for SQL Server"),
            ("Handshake Connection Verification Validation Runtime Status Layer:", "ACTIVE (Listening directly on PyODBC Pipeline threads channels)")
        ]
        
        for lbl_title, value_string in config_labels:
            row_frame = ctk.CTkFrame(wrapper, fg_color="transparent")
            row_frame.pack(fill="x", padx=25, pady=8)
            
            ctk.CTkLabel(row_frame, text=lbl_title, font=("Segoe UI", 13, "bold"), text_color=SECONDARY, width=380, anchor="w").pack(side="left")
            ctk.CTkLabel(row_frame, text=value_string, font=("Consolas", 13), text_color="#34D399" if "ACTIVE" in value_string else TEXT, anchor="w").pack(side="left", padx=10)


# =========================================================
# SUB-VIEW: SECURITY MANAGEMENT USER PRIVILEGES REGISTRY
# =========================================================
class AdminWorkspaceView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=CARD_COLOR, corner_radius=16, border_width=1, border_color=BORDER)
        self.app_root = parent.master
        
        ctk.CTkLabel(self, text="⚙️ Security System Administrative Privileges Dashboard", font=("Segoe UI", 20, "bold"), text_color=TEXT).pack(anchor="w", padx=30, pady=(25, 5))
        ctk.CTkLabel(self, text="Monitors localized user identity authentication credentials profiles and active system status data rules configurations.", font=("Segoe UI", 13), text_color=SECONDARY).pack(anchor="w", padx=30, pady=(0, 20))
        
        list_wrapper = ctk.CTkFrame(self, fg_color="#0B1220", corner_radius=14, border_width=1, border_color=BORDER)
        list_wrapper.pack(fill="both", expand=True, padx=35, pady=(10, 15))
        
        ctk.CTkLabel(list_wrapper, text="Authenticated Profiles Stored Inside 'users_auth.json' Registry Storage File", font=("Segoe UI", 14, "bold"), text_color=TEXT).pack(anchor="w", padx=25, pady=(20, 10))
        
        try:
            with open(USER_DB_FILE, "r") as f:
                user_profiles_dict = json.load(f)
                
            for username, obfuscated_pwd in user_profiles_dict.items():
                row = ctk.CTkFrame(list_wrapper, fg_color=CARD_COLOR, corner_radius=8, height=40, border_width=1, border_color="#1E293B")
                row.pack(fill="x", padx=25, pady=5)
                row.pack_propagate(False)
                
                ctk.CTkLabel(row, text=f"👤 User Account Handle ID: {username}", font=("Segoe UI", 13, "bold"), text_color=TEXT).pack(side="left", padx=15)
                ctk.CTkLabel(row, text=f"🔒 Encrypted Key Profile: {'*' * len(obfuscated_pwd)} (Stored safely locally)", font=("Segoe UI", 12), text_color=SECONDARY).pack(side="right", padx=15)
        except Exception as e:
            ctk.CTkLabel(list_wrapper, text=f"Failed to pull active session registry records. Reason: {str(e)}", text_color="#EF4444").pack(pady=20)

        danger_zone_box = ctk.CTkFrame(self, fg_color="#1E1B1B", corner_radius=14, border_width=1, border_color="#991B1B")
        danger_zone_box.pack(fill="x", padx=35, pady=(10, 25))
        
        info_frame = ctk.CTkFrame(danger_zone_box, fg_color="transparent")
        info_frame.pack(side="left", padx=25, pady=15)
        
        ctk.CTkLabel(info_frame, text="⚠ Account Data Management Security Warning Actions", font=("Segoe UI", 14, "bold"), text_color="#FCA5A5").pack(anchor="w")
        ctk.CTkLabel(info_frame, text="Deleting your user profile immediately purges all credentials data locally. This action cannot be reversed.", font=("Segoe UI", 12), text_color="#F87171").pack(anchor="w")
        
        delete_account_btn = ctk.CTkButton(
            danger_zone_box, text="Delete My Account", width=150, height=38, corner_radius=8,
            fg_color="#DC2626", hover_color="#991B1B", text_color=TEXT, font=("Segoe UI", 13, "bold"),
            command=self.execute_profile_wipeout_sequence
        )
        delete_account_btn.pack(side="right", padx=25, pady=15)

    def execute_profile_wipeout_sequence(self):
        target_username = self.app_root.current_user
        if not target_username:
            return
            
        try:
            with open(USER_DB_FILE, "r") as f:
                current_profiles = json.load(f)
                
            if target_username in current_profiles:
                del current_profiles[target_username]
                
            with open(USER_DB_FILE, "w") as f:
                json.dump(current_profiles, f)
                
            self.app_root.handle_logout()
            
        except Exception as err:
            print(f"Error handling administrative data profile removal cleanup operation: {str(err)}")


if __name__ == "__main__":
    app = DataChatbotApp()
    app.mainloop()