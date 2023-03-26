import cmd
from rich.table import Table
from rich.console import Console
from task import Task
#from database import getTablesNames, createTable, tableExists, deleteTable, addTaskToTable, getAllRows, removeTaskFromTable, 
import database as db
from shlex import split

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

    def do_show(self, arg):
        if not self.hasSelectedList():
            self.printSelectError()
            return
        
        todos = db.getAllRows(self.selected_list)
        for todo in todos:
            print(todo.position, todo.name)
        
    def do_create(self, list_name):
        """Add a new TODO list"""
        list_name = list_name.split()[0]

        if db.tableExists(list_name):
            print("List already exists!")
            return

        db.createTable(list_name)
        self.do_lists(list_name)   

    def do_delete(self, list_position):
        """Deletes a TODO list"""
        if not self.hasSelectedList():
            self.printSelectError()

        list_name = list_name.split()[0]

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

        task = Task.create(todo, category)
        db.addTaskToTable(task, self.selected_list)

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

        db.invertTaskStatus(position, self.selected_list)
        
        self.do_show(None)

    def do_update(self, args):
        pass
    
    def do_quit(self, arg):
        """Quit the program"""
        return True
    
    def do_help(self, arg):
        """Available commands"""
        if arg:
            # Obter a mensagem de ajuda padrão para o comando
            doc = getattr(self, "do_" + arg).__doc__
            return doc + '\n\nDescrição:\n\tAdiciona uma saudação ao nome especificado'
        else:
            cmd.Cmd.do_help(self, arg)
        
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
    
    def printSelectError():
        print("[ERROR] You must select a list before!")
    
if __name__ == '__main__':
    TodoCLI().cmdloop()
