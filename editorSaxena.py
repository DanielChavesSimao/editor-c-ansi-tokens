from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tokenizer_c_ansi import tokenize, Token
import json
import logging


class TextEditor:

    def __init__(self, root: Tk):
        logging.basicConfig(level=logging.DEBUG)
        self.root = root
        self.root.title("ChurrasText")
        self.root.geometry("1200x700+200+150")
        self.filename = None
        self.title = StringVar()
        self.status = StringVar()
        # Inicializar a configuração de cores
        self.colorConfiguration = self.initialize_color_configuration()

        # Title bar
        self.titlebar = Label(self.root, textvariable=self.title, font=(
            "times new roman", 15, "bold"), bd=2, relief=GROOVE)
        self.titlebar.pack(side=TOP, fill=BOTH)
        self.settitle()

        # Status bar
        self.statusbar = Label(self.root, textvariable=self.status, font=(
            "times new roman", 15, "bold"), bd=2, relief=GROOVE)
        self.statusbar.pack(side=BOTTOM, fill=BOTH)
        self.status.set("Welcome To Text Editor")

        # Menu bar
        self.menubar = Menu(self.root, font=(
            "times new roman", 15, "bold"), activebackground="skyblue")
        self.root.config(menu=self.menubar)

        # File menu
        self.filemenu = Menu(self.menubar, font=(
            "times new roman", 12, "bold"), activebackground="skyblue", tearoff=0)
        self.filemenu.add_command(
            label="New", accelerator="Ctrl+N", command=self.newfile)
        self.filemenu.add_command(
            label="Open", accelerator="Ctrl+O", command=self.openfile)
        self.filemenu.add_command(
            label="Save", accelerator="Ctrl+S", command=self.savefile)
        self.filemenu.add_command(
            label="Save As", accelerator="Ctrl+A", command=self.saveasfile)
        self.filemenu.add_separator()
        self.filemenu.add_command(
            label="Exit", accelerator="Ctrl+E", command=self.exit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Edit Menu
        self.editmenu = Menu(self.menubar, font=(
            "times new roman", 12, "bold"), activebackground="skyblue", tearoff=0)
        self.editmenu.add_command(
            label="Cut", accelerator="Ctrl+X", command=self.cut)
        self.editmenu.add_command(
            label="Copy", accelerator="Ctrl+C", command=self.copy)
        self.editmenu.add_command(
            label="Paste", accelerator="Ctrl+V", command=self.paste)
        self.editmenu.add_separator()
        self.editmenu.add_command(
            label="Undo", accelerator="Ctrl+U", command=self.undo)
        self.editmenu.add_separator()
        self.editmenu.add_command(
            label="Check C Tokens", command=self.checkCTokens)
        self.editmenu.add_command(
            label="Update Color config", command=self.updateColorConfig)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        # Help menu
        self.helpmenu = Menu(self.menubar, font=(
            "times new roman", 12, "bold"), activebackground="skyblue", tearoff=0)
        self.helpmenu.add_command(label="About", command=self.infoabout)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        # Vertical scroll bar
        scrol_y = Scrollbar(self.root, orient=VERTICAL)
        
        # Text Area
        self.txtarea = Text(self.root, yscrollcommand=scrol_y.set, font=(
            "times new roman", 15, "bold"), background='grey25', foreground='white', state="normal", relief=GROOVE)
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.txtarea.yview)
        # Event binding for tokenization
        self.txtarea.bind("<KeyRelease>", self.checkCTokens)
        self.txtarea.pack(fill=BOTH, expand=1)

        # Shortcuts setup
        self.shortcuts()
        # Tags styles setup
        self.set_configs_for_tags()

    def get_color_configuration(self, type) -> str:
        """
        Retorna uma string com o valor da cor para o tipo do token type.
        """
        return self.colorConfiguration[type]["color"] if type in self.colorConfiguration else "white"

    def initialize_color_configuration(self) -> dict:
        """
        Abre o arquivo e retorna um dict {token_name_1: {color: color_value}, {token_name_2: {color: color_value}, ...}
        """
        with open('token_colors.json') as f:
            colorConfiguration = json.load(f)

        return colorConfiguration

    def setTagForToken(self, token: Token) -> None:
        """
        Adiciona a tag com o nome token.type em volta do token encontrado.
        """
        self.txtarea.tag_add(
            token.type, f'{token.line_start}.{token.column_start}', f'{token.line_end}.{token.column_end}')
        

    def set_configs_for_tags(self) -> None:
        """
        Configura as tags disponíveis na classe Token de acordo com as cores obtidas do arquivo.
        """
        for token in Token.available_types:
            self.txtarea.tag_configure(
                token, foreground=self.get_color_configuration(token))

    def updateColorConfig(self) -> None:
        """
        Le o arquivo de cores novamente e faz a checagem de tokens
        """
        self.colorConfiguration = self.initialize_color_configuration()
        self.set_configs_for_tags()
        self.checkCTokens()

    def clean_all_tags(self) -> None:
        """
        Pinta as tags de branco
        """
        self.txtarea.configure(foreground="white")
        for tag in self.txtarea.tag_names():
            self.txtarea.tag_remove(tag, '1.0', END)
        # logging.debug(self.txtarea.dump('1.0',END))

    def checkCTokens(self, e=None) -> None:
        if e:
            pass
        texto = self.txtarea.get("1.0", END)
        self.clean_all_tags()
        print('\n--Tokens update--')
        for token in tokenize(texto):
            logging.debug(token)
            self.setTagForToken(token)

    def settitle(self):
        if self.filename:
            self.title.set(self.filename)
        else:
            self.title.set("Untitled")

    def newfile(self, *args):
        self.txtarea.delete("1.0", END)
        self.filename = None
        self.settitle()
        self.status.set("New File Created")

    def openfile(self, *args):
        try:
            self.filename = filedialog.askopenfilename(title="Select file", filetypes=(
                ("All Files", "*.*"), ("Text Files", "*.txt"), ("C Files", "*.c")))
            if self.filename:
                infile = open(self.filename, "r")
                self.txtarea.delete("1.0", END)
                for line in infile:
                    self.txtarea.insert(END, line)
                infile.close()
                self.settitle()
                self.status.set("Opened Successfully")
                self.checkCTokens()
        except Exception as e:
            messagebox.showerror("Exception", e)

    def savefile(self, *args):
        try:
            if self.filename:
                data = self.txtarea.get("1.0", END)
                outfile = open(self.filename, "w")
                outfile.write(data)
                outfile.close()
                self.settitle()
                self.status.set("Saved Successfully")
            else:
                self.saveasfile()
        except Exception as e:
            messagebox.showerror("Exception", e)

    def saveasfile(self, *args):
        try:
            untitledfile = filedialog.asksaveasfilename(title="Save file As", defaultextension=".txt", initialfile="Untitled.txt", filetypes=(
                ("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py")))
            data = self.txtarea.get("1.0", END)
            outfile = open(untitledfile, "w")
            outfile.write(data)
            outfile.close()
            self.filename = untitledfile
            self.settitle()
            self.status.set("Saved Successfully")
        except Exception as e:
            messagebox.showerror("Exception", e)

    def exit(self, *args):
        op = messagebox.askyesno(
            "WARNING", "Your Unsaved Data May be Lost!!\nAre you sure you want to exit?")
        if op > 0:
            self.root.destroy()
        else:
            return

    def cut(self, *args):
        self.txtarea.event_generate("<<Cut>>")

    def copy(self, *args):
        self.txtarea.event_generate("<<Copy>>")

    def paste(self, *args):
        self.txtarea.event_generate("<<Paste>>")

    def undo(self, *args):
        try:
            if self.filename:
                self.txtarea.delete("1.0", END)
                infile = open(self.filename, "r")
                for line in infile:
                    self.txtarea.insert(END, line)
                infile.close()
                self.settitle()
                self.status.set("Undone Successfully")
            else:
                self.txtarea.delete("1.0", END)
                self.filename = None
                self.settitle()
                self.status.set("Undone Successfully")
        except Exception as e:
            messagebox.showerror("Exception", e)

    def infoabout(self):
        messagebox.showinfo("About Text Editor",
                            "A Simple Text Editor\nCreated using Python.")

    def shortcuts(self):
        self.txtarea.bind("<Control-n>", self.newfile)
        self.txtarea.bind("<Control-o>", self.openfile)
        self.txtarea.bind("<Control-s>", self.savefile)
        self.txtarea.bind("<Control-a>", self.saveasfile)
        self.txtarea.bind("<Control-e>", self.exit)
        self.txtarea.bind("<Control-x>", self.cut)
        self.txtarea.bind("<Control-c>", self.copy)
        self.txtarea.bind("<Control-v>", self.paste)
        self.txtarea.bind("<Control-u>", self.undo)
