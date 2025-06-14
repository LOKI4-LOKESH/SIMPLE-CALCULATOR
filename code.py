import tkinter as tk
from tkinter import font

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Calculator - Professional")
        self.configure(bg="#f6f8fa")  # Light background (GitHub light)
        self.resizable(False, False)
        self._build_ui()
        self._bind_keys()
        self.expression = ""

    def _build_ui(self):
        self.display_font = font.Font(family="Consolas", size=24, weight="bold")
        self.button_font = font.Font(family="Segoe UI", size=14)
        self.button_active_bg = "#d0d7de"  
        self.button_bg = "#ffffff"          
        self.button_fg = "#24292e"           
        self.accent_fg = "#0366d6"         
        self.display_var = tk.StringVar()
        self.display = tk.Entry(self, textvariable=self.display_var, font=self.display_font,
                                bg="#ffffff", fg="#24292e", bd=2, relief="sunken",
                                justify="right", state="readonly", readonlybackground="#ffffff",
                                highlightthickness=0, insertbackground="#24292e")
        self.display.grid(row=0, column=0, columnspan=4, ipadx=10, ipady=15, padx=16, pady=(16,8), sticky="ew")
        buttons = [
            ("C", 1, 0, self._clear), 
            ("±", 1, 1, self._toggle_sign), 
            ("%", 1, 2, self._percent), 
            ("/", 1, 3, lambda: self._append_operator("/")),
            ("7", 2, 0, lambda: self._append_char("7")),
            ("8", 2, 1, lambda: self._append_char("8")),
            ("9", 2, 2, lambda: self._append_char("9")),
            ("*", 2, 3, lambda: self._append_operator("*")),
            ("4", 3, 0, lambda: self._append_char("4")),
            ("5", 3, 1, lambda: self._append_char("5")),
            ("6", 3, 2, lambda: self._append_char("6")),
            ("-", 3, 3, lambda: self._append_operator("-")),
            ("1", 4, 0, lambda: self._append_char("1")),
            ("2", 4, 1, lambda: self._append_char("2")),
            ("3", 4, 2, lambda: self._append_char("3")),
            ("+", 4, 3, lambda: self._append_operator("+")),
            ("0", 5, 0, lambda: self._append_char("0")),
            (".", 5, 1, lambda: self._append_decimal()),
            ("←", 5, 2, self._backspace),
            ("=", 5, 3, self._calculate),
        ]

        for (text, r, c, cmd) in buttons:
            btn = tk.Button(self, text=text, command=cmd,
                            font=self.button_font, fg=self.button_fg,
                            bg=self.button_bg, bd=1, relief="raised",
                            activebackground=self.button_active_bg,
                            activeforeground=self.accent_fg,
                            highlightthickness=0, padx=12, pady=10)
            btn.grid(row=r, column=c, sticky="nsew", padx=8, pady=8)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.button_active_bg))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.button_bg))

        for i in range(6):
            self.rowconfigure(i, weight=1)
        for j in range(4):
            self.columnconfigure(j, weight=1)

    def _bind_keys(self):
  
        for key in "0123456789":
            self.bind(key, self._key_append)
        for key in "+-*/":
            self.bind(key, self._key_append)
        self.bind(".", self._key_append)
        self.bind("<Return>", lambda e: self._calculate())
        self.bind("<BackSpace>", lambda e: self._backspace())
        self.bind("<Escape>", lambda e: self._clear())

    def _key_append(self, event):
        char = event.char
        if char in "0123456789":
            self._append_char(char)
        elif char in "+-*/":
            self._append_operator(char)
        elif char == ".":
            self._append_decimal()

    def _append_char(self, char):
 
        self.expression += char
        self._update_display()

    def _append_operator(self, operator):
        if not self.expression:
            
            if operator == "-":
                self.expression += operator
                self._update_display()
            return

        
        if self.expression[-1] in "+-*/":
            self.expression = self.expression[:-1] + operator
        else:
            self.expression += operator
        self._update_display()

    def _append_decimal(self):
        
        parts = self._split_expression()
        if "." in parts[-1]:
            return  # Ignore if current number already has decimal
        self.expression += "."
        self._update_display()

    def _split_expression(self):
        
        import re
        parts = re.split(r"[+\-*/]", self.expression)
        return parts

    def _clear(self):
        self.expression = ""
        self._update_display()

    def _backspace(self):
        self.expression = self.expression[:-1]
        self._update_display()

    def _toggle_sign(self):
       
        import re
        parts = list(re.finditer(r"(\d*\.?\d+)", self.expression))
        if not parts:
            return
        last = parts[-1]
        start, end = last.span()
        number_text = self.expression[start:end]
        try:
            number_value = float(number_text)
            toggled = -number_value
           
            self.expression = self.expression[:start] + str(toggled) + self.expression[end:]
            self._update_display()
        except ValueError:
            pass

    def _percent(self):
        
        import re
        parts = list(re.finditer(r"(\d*\.?\d+)", self.expression))
        if not parts:
            return
        last = parts[-1]
        start, end = last.span()
        number_text = self.expression[start:end]
        try:
            number_value = float(number_text)
            percent_value = number_value / 100
            self.expression = self.expression[:start] + str(percent_value) + self.expression[end:]
            self._update_display()
        except ValueError:
            pass

    def _calculate(self):
        try:
            
            expression_eval = self.expression.replace("÷", "/").replace("×", "*")
            
            if not all(c in "0123456789+-*/.() " for c in expression_eval):
                raise ValueError("Invalid character")
            result = eval(expression_eval, {"__builtins__": {}}, {}) 
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            self.expression = str(result)
            self._update_display()
        except Exception:
            self.expression = ""
            self.display_var.set("Error")

    def _update_display(self):
        self.display_var.set(self.expression)


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()

