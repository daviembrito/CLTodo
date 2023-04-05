'''
CLTodo - Command Line Todos
Coded by: github.com/daviembrito
Version: 0.1.2
'''

import cmd
from rich.table import Table
from rich.console import Console
from rich.text import Text
from todo import Todo
import database as db
from shlex import split
from datetime import datetime

class TodoCLI(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.selected_list = None
        
        self.console = Console()
        self.prompt = '> '
        self.doc_header = 'Comandos disponíveis:'
        self.undoc_header = 'Comandos não documentados:'
        self.aliases = {
            "exit" : self.do_quit,
            "q" : self.do_quit,
            "h" : self.do_help,
            "list" : self.do_lists,
            "tables" : self.do_lists
        }

    def do_lists(self, args):
        """Lists all available TODO lists"""
        lists = db.getTablesNames()

        if lists == ["No list found!"]:
            self.printError(lists[0])
            return

        for list in lists:
            print(list)

    def do_select(self, list_name):
        """Selects a list to interact with"""
        if not db.tableExists(list_name):
            self.printError("Invalid list name!")
            return 
        
        self.selected_list = list_name
        self.prompt = f"{list_name}> "

        self.printMessage(f'Selected list "{list_name}"!')

    def do_show(self, arg):
        """Shows the list"""
        if not self.hasSelectedList():
            return
        
        if arg:
            arg = split(arg)[0]
            if arg in ["done", "undone"]:
                todos = db.getRowsFromStatus(arg, self.selected_list)
            else:
                todos = db.getRowsFromCategory(arg, self.selected_list)
        else:
            todos = db.getAllRows(self.selected_list)

        table = self.createTable(todos)
        self.console.print(table)
        
    def do_create(self, list_name):
        """Add a new TODO list"""
        if self.notEnoughArgs(list_name, 1):
            self.printError("You must provide a name!")
            return

        list_name = split(list_name)[0]

        if db.tableExists(list_name):
            self.printError("List already exists!")
            return

        db.createTable(list_name)
        self.do_lists(list_name)   

    def do_delete(self, list_name):
        """Deletes a TODO list"""
        if self.notEnoughArgs(list_name, 1):
            self.printError("You must provide a list name!")
            return
        
        list_name = split(list_name)[0]

        if not db.tableExists(list_name):
            self.printError("List does not exists!")
            return
        
        db.deleteTable(list_name)

        if db.getTablesNames()[0] == "No list found!":
            return
        
        self.do_lists(list_name) 

    def do_add(self, args):
        """Adds a TODO to the list"""
        if not self.hasSelectedList():
            return
        
        if self.notEnoughArgs(args, 2):
            self.printError("You must provide a name and category!")

        args = split(args)
        todo, category = args[0], args[1]

        todo = Todo.create(todo, category)
        db.addTaskToTable(todo, self.selected_list)

        self.do_show(None)

    def do_remove(self, position):
        """Removes a TODO from the list"""
        if not self.hasSelectedList():
            return
        
        if self.notEnoughArgs(position, 1):
            self.printError("You must provide a position!")
        
        position = split(position)[0]
        db.removeTaskFromTable(position, self.selected_list)

        self.do_show(None)

    def do_done(self, position):
        """Turns a TODO to done"""
        if not self.hasSelectedList():
            return
        
        if self.notEnoughArgs(position, 1):
            self.printError("You must provide a position!")
            return

        done_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
        db.invertTaskStatus(position, done_date, self.selected_list)

        self.do_show(None)

    def do_change(self, args):
        """Change a todo position"""
        if not self.hasSelectedList():
            return
        
        if self.notEnoughArgs(args, 2):
            self.printError("You must provide a old and new positions")
            return

        args = split(args)
        old_position, new_position = args[0], args[1]

        if int(new_position) > db.getMaxPosition(self.selected_list):
            self.printError("New position is out of range!")
            return

        db.changeTaskPosition(old_position, new_position, self.selected_list)
        self.do_show(None)

    
    def do_quit(self, arg):
        return True
    
    def do_help(self, arg):
        self.console.print("COMMANDS:", style="bold yellow")
        hello = """
        lists                   List all Todo lists
        create <name>           Create a new list
        delete <list>           Delete a list
        select <list>           Select a list to interact with
        show [category]         Show the whole list (or a specific category)
        add <todo> <category>   Add a new Todo to the list
        remove <position>       Remove a todo with the specified position
        done <position>         Change the status of the todo to done or undone
        change <pos> <new_pos>  Change a todo's position
        quit                    Quit the program"""

        print(hello)
        
    def default(self, line):
        cmd, arg, line = self.parseline(line)

        if cmd in self.aliases:
            return self.aliases[cmd](arg)
        else:
            self.do_help(arg)

    def hasSelectedList(self):
        if self.selected_list:
            return True
        
        self.printError("You must select a list before!")
        return False
    
    def createTable(self, todos):
        table = Table(show_header=True, header_style="bold cyan")

        table.add_column("#", style="dim", width=4, justify="center")
        table.add_column("Todo", min_width=20, justify="center")
        table.add_column("Category", min_width=12, justify="center")
        table.add_column("Created At", min_width=12, justify="center")
        table.add_column("Done At", min_width=12, justify="center")
        table.add_column("Done", width=5, justify="center")

        for todo in todos:
            self.createRow(todo, table)

        return table
    
    def createRow(self, todo, table):
        is_done_str = Text("√", style="bold green") if todo.done == True else Text("X", style="bold red")
        done_date_str = "-" if todo.done_date == None else todo.done_date[:-7]
        created_date_str = todo.created_date[:-7]

        table.add_row(str(todo.position),
                    todo.name, 
                    todo.category, 
                    created_date_str,
                    done_date_str, 
                    is_done_str)
        
    def notEnoughArgs(self, args, numberOfArgs):
        if len(args) < numberOfArgs:
            return True
        
        return False
    
    def printMessage(self, msg):
        self.console.print(f'[OK] {msg}', style="bold cyan")

    def printError(self, msg):
        self.console.print(f'[ERROR] {msg}', style="bold red")
    
if __name__ == '__main__':
    Console().print("CLTodo", style="bold cyan")
    TodoCLI().cmdloop()