
import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import pyperclip


class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("560x720")
        self.root.resizable(False, False)
        self.root.configure(bg="#101827")

        self.history = []
        self.password_var = tk.StringVar()
        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.number_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)
        self.exclude_var = tk.BooleanVar(value=False)

        self.bg = "#101827"
        self.panel = "#1d293b"
        self.fg = "#f1f5f9"
        self.accent = "#818cf8"

        self.build_gui()

    def build_gui(self):
        tk.Label(
            self.root,
            text="SECURE PASSWORD GENERATOR",
            font=("Arial", 19, "bold"),
            bg=self.bg,
            fg=self.accent
        ).pack(pady=(20, 5))

        tk.Label(
            self.root,
            text="Create a strong, random password",
            font=("Arial", 10),
            bg=self.bg,
            fg="#cbd5e1"
        ).pack(pady=(0, 15))

        options = tk.Frame(self.root, bg=self.panel)
        options.pack(fill="x", padx=25, pady=5)

        tk.Label(
            options,
            text="Password length",
            font=("Arial", 11, "bold"),
            bg=self.panel,
            fg=self.fg
        ).grid(row=0, column=0, sticky="w", padx=15, pady=12)

        self.length_spin = tk.Spinbox(
            options,
            from_=8,
            to=64,
            textvariable=self.length_var,
            width=6,
            font=("Arial", 11)
        )
        self.length_spin.grid(row=0, column=1, padx=10, pady=12)

        tk.Label(
            options,
            text="Character types",
            font=("Arial", 11, "bold"),
            bg=self.panel,
            fg=self.fg
        ).grid(row=1, column=0, sticky="w", padx=15, pady=5)

        checkbox_frame = tk.Frame(options, bg=self.panel)
        checkbox_frame.grid(
            row=2, column=0, columnspan=2,
            sticky="w", padx=15, pady=5
        )

        checkbox_style = {
            "bg": self.panel,
            "fg": self.fg,
            "selectcolor": self.bg,
            "activebackground": self.panel,
            "activeforeground": self.fg,
            "font": ("Arial", 10)
        }

        tk.Checkbutton(
            checkbox_frame, text="Uppercase (A-Z)",
            variable=self.upper_var, **checkbox_style
        ).pack(anchor="w", pady=2)

        tk.Checkbutton(
            checkbox_frame, text="Lowercase (a-z)",
            variable=self.lower_var, **checkbox_style
        ).pack(anchor="w", pady=2)

        tk.Checkbutton(
            checkbox_frame, text="Numbers (0-9)",
            variable=self.number_var, **checkbox_style
        ).pack(anchor="w", pady=2)

        tk.Checkbutton(
            checkbox_frame, text="Symbols (!@#...)",
            variable=self.symbol_var, **checkbox_style
        ).pack(anchor="w", pady=2)

        tk.Checkbutton(
            options,
            text="Exclude ambiguous characters (0, O, l, 1)",
            variable=self.exclude_var,
            **checkbox_style
        ).grid(row=3, column=0, columnspan=2,
               sticky="w", padx=15, pady=10)

        tk.Button(
            self.root,
            text="Generate Password",
            command=self.generate_password,
            font=("Arial", 12, "bold"),
            bg=self.accent,
            fg="#101827",
            activebackground="#a5b4fc",
            relief="flat",
            cursor="hand2"
        ).pack(fill="x", padx=25, pady=12, ipady=7)

        result_frame = tk.Frame(self.root, bg=self.panel)
        result_frame.pack(fill="x", padx=25, pady=5)

        tk.Label(
            result_frame,
            text="YOUR PASSWORD",
            font=("Arial", 9, "bold"),
            bg=self.panel,
            fg="#cbd5e1"
        ).pack(pady=(12, 5))

        self.password_entry = tk.Entry(
            result_frame,
            textvariable=self.password_var,
            font=("Consolas", 14),
            justify="center",
            state="readonly",
            readonlybackground="#263449",
            fg="#a5f3fc",
            relief="flat"
        )
        self.password_entry.pack(fill="x", padx=12, ipady=9)

        tk.Button(
            result_frame,
            text="Copy to Clipboard",
            command=self.copy_password,
            font=("Arial", 10, "bold"),
            bg="#334155",
            fg=self.fg,
            activebackground="#475569",
            relief="flat",
            cursor="hand2"
        ).pack(pady=10, ipadx=10, ipady=3)

        self.status_label = tk.Label(
            result_frame,
            text="Generate a password to get started.",
            bg=self.panel,
            fg="#cbd5e1",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=(0, 10))

        strength_frame = tk.Frame(self.root, bg=self.bg)
        strength_frame.pack(fill="x", padx=30, pady=8)

        self.strength_label = tk.Label(
            strength_frame,
            text="Password strength: Not generated",
            bg=self.bg,
            fg=self.fg,
            font=("Arial", 10, "bold")
        )
        self.strength_label.pack(anchor="w")

        self.strength_bar = ttk.Progressbar(
            strength_frame,
            length=490,
            maximum=100,
            mode="determinate"
        )
        self.strength_bar.pack(fill="x", pady=7)

        tk.Label(
            self.root,
            text="Recent passwords (current session only)",
            font=("Arial", 10, "bold"),
            bg=self.bg,
            fg=self.fg
        ).pack(anchor="w", padx=30, pady=(8, 4))

        self.history_list = tk.Listbox(
            self.root,
            height=5,
            font=("Consolas", 10),
            bg=self.panel,
            fg=self.fg,
            selectbackground=self.accent,
            relief="flat"
        )
        self.history_list.pack(fill="x", padx=25, pady=(0, 10))

        tk.Label(
            self.root,
            text="Passwords are not saved to a file.",
            font=("Arial", 9),
            bg=self.bg,
            fg="#94a3b8"
        ).pack(pady=(0, 10))

    def generate_password(self):
        try:
            length = self.length_var.get()

            if not 8 <= length <= 64:
                messagebox.showerror(
                    "Invalid length",
                    "Choose a password length from 8 to 64."
                )
                return

        except (ValueError, tk.TclError):
            messagebox.showerror(
                "Invalid length",
                "Enter a valid whole number."
            )
            return

        selected_groups = []

        if self.upper_var.get():
            selected_groups.append(string.ascii_uppercase)

        if self.lower_var.get():
            selected_groups.append(string.ascii_lowercase)

        if self.number_var.get():
            selected_groups.append(string.digits)

        if self.symbol_var.get():
            selected_groups.append(string.punctuation)

        if len(selected_groups) < 2:
            messagebox.showerror(
                "Select character types",
                "Choose at least two character types."
            )
            return

        if length < len(selected_groups):
            messagebox.showerror(
                "Invalid length",
                "Password length is too short for your selections."
            )
            return

        if self.exclude_var.get():
            ambiguous = "0Ol1"
            selected_groups = [
                "".join(
                    char for char in group
                    if char not in ambiguous
                )
                for group in selected_groups
            ]

        if any(not group for group in selected_groups):
            messagebox.showerror(
                "Character selection",
                "One selected character group is empty."
            )
            return

        all_characters = "".join(selected_groups)

        # Guarantee one character from every selected group.
        password_chars = [
            secrets.choice(group) for group in selected_groups
        ]

        # Fill the remaining positions securely.
        while len(password_chars) < length:
            password_chars.append(
                secrets.choice(all_characters)
            )

        # Securely shuffle the password characters.
        secrets.SystemRandom().shuffle(password_chars)

        password = "".join(password_chars)
        self.password_var.set(password)

        self.update_strength(password, len(selected_groups))
        self.update_history(password)

        # Automatically copy the new password.
        try:
            pyperclip.copy(password)
            self.status_label.config(
                text="Password generated and copied!"
            )
        except pyperclip.PyperclipException:
            self.status_label.config(
                text="Password generated. Use Copy to Clipboard."
            )
        except Exception:
            self.status_label.config(
                text="Password generated. Clipboard unavailable."
            )

    def update_strength(self, password, diversity):
        length = len(password)

        if length >= 16 and diversity >= 3:
            strength = "Strong"
            score = 100
        elif length >= 12 and diversity >= 2:
            strength = "Medium"
            score = 65
        else:
            strength = "Weak"
            score = 30

        self.strength_bar["value"] = score
        self.strength_label.config(
            text=f"Password strength: {strength} ({score}%)"
        )

    def copy_password(self):
        password = self.password_var.get()

        if not password:
            messagebox.showinfo(
                "No password",
                "Generate a password first."
            )
            return

        try:
            pyperclip.copy(password)
            self.status_label.config(
                text="Password copied to clipboard!"
            )
        except Exception:
            messagebox.showerror(
                "Clipboard error",
                "Could not copy. Please try again."
            )

    def update_history(self, password):
        self.history.insert(0, password)
        self.history = self.history[:5]

        self.history_list.delete(0, tk.END)

        for item in self.history:
            self.history_list.insert(tk.END, item)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

