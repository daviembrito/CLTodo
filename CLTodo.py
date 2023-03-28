import cmd
from rich.table import Table
from rich.console import Console
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
        for list in lists:
            print(list)

    def do_select(self, list_name):
        """Selects a list to interact with"""
        if not db.tableExists(list_name):
            print("Invalid list name!")
            return 
        
        self.selected_list = list_name
        print(f"Selected list {list_name}!")

    def do_show(self, category):
        if not self.hasSelectedList():
            self.printSelectError()
            return
        
        if category:
            category = split(category)[0]
            todos = db.getRowsFromCategory(category[0], self.selected_list)
        else:
            todos = db.getAllRows(self.selected_list)

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("#", style="dim", width=4, justify="center")
        table.add_column("Todo", min_width=20, justify="center")
        table.add_column("Category", min_width=12, justify="center")
        table.add_column("Created At", min_width=12, justify="center")
        table.add_column("Done At", min_width=12, justify="center")
        table.add_column("Done", min_width=6, justify="center")

        for todo in todos:
            is_done_str = '✅' if todo.done == True else '❌'
            done_date_str = "-" if todo.done_date == None else todo.done_date[:-7]
            created_date_str = todo.created_date[:-7]

            table.add_row(str(todo.position),
                        todo.name, 
                        todo.category, 
                        created_date_str,
                        done_date_str, 
                        is_done_str)
        self.console.print(table)
        
    def do_create(self, list_name):
        """Add a new TODO list"""
        list_name = split(list_name)[0]

        if db.tableExists(list_name):
            print("List already exists!")
            return

        db.createTable(list_name)
        self.do_lists(list_name)   

    def do_delete(self, list_name):
        """Deletes a TODO list"""
        list_name = split(list_name)[0]

        if not db.tableExists(list_name):
            print("List does not exists!")
            return
        
        db.deleteTable(list_name)

        if db.getTablesNames()[0] == "No list found!":
            return
        
        self.do_lists(list_name) 

    def do_add(self, args):
        """Adds a TODO to the list"""
        if not self.hasSelectedList():
            self.printSelectError()
            return

        args = split(args)
        todo, category = args[0], args[1]

        todo = Todo.create(todo, category)
        db.addTaskToTable(todo, self.selected_list)

        self.do_show(None)

    def do_remove(self, position):
        """Removes a TODO from the list"""
        if not self.hasSelectedList():
            self.printSelectError()
            return
        
        position = split(position)[0]
        db.removeTaskFromTable(position, self.selected_list)

        self.do_show(None)

    def do_done(self, position):
        if not self.hasSelectedList():
            self.printSelectError()
            return

        done_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S.%f")
        db.invertTaskStatus(position, done_date, self.selected_list)

        self.do_show(None)

    def do_change(self, args):
        if not self.hasSelectedList():
            self.printSelectError()
            return

        args = split(args)
        old_position, new_position = args[0], args[1]

        db.changeTaskPosition(old_position, new_position, self.selected_list)
        self.do_show(None)

    
    def do_quit(self, arg):
        """Quit the program"""
        return True
    
    def do_help(self, arg):
        """Available commands"""
        print("teste")        
        """
        if arg:
            doc = getattr(self, "do_" + arg).__doc__
            return doc + '\n\nDescrição:\n\tAdiciona uma saudação ao nome especificado'
        else:
            cmd.Cmd.do_help(self, arg)
        """
        
    def default(self, line):
        cmd, arg, line = self.parseline(line)

        if cmd in self.aliases:
            return self.aliases[cmd](arg)
        else:
            self.do_help(arg)

    def hasSelectedList(self):
        if self.selected_list:
            return True
        
        return False
    
    def printSelectError(self):
        print("[ERROR] You must select a list before!")
    
if __name__ == '__main__':
    TodoCLI().cmdloop()
