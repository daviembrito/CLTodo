import cmd
from rich.table import Table
from task import Task
from database import getTablesNames, createTable, tableExists, deleteTable

class MyCLI(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '
        self.doc_header = 'Comandos disponíveis:'
        self.undoc_header = 'Comandos não documentados:'
        self.aliases = {
            "exit" : self.do_quit,
            "q" : self.do_quit,
            "h" : self.do_help
        }
        self.actual_list = None

    def do_lists(self, args):
        """Lists all available TODO lists"""
        lists = getTablesNames()
        for list in lists:
            print(list)

    def do_select(self, list_name):
        """Selects a list to interact with"""
        if not tableExists(list_name):
            print("Invalid list name!")
            return 
        
        self.actual_list = list_name
        print(f"Selected list {list_name}")

    def do_show(self, arg):
        pass

    def do_create(self, list_name):
        """Add a new TODO list"""
        list_name = list_name.split()[0]

        if tableExists(list_name):
            print("List already exists!")
            return

        createTable(list_name)
        self.do_lists(list_name)   

    def do_delete(self, list_name):
        """Deletes a TODO list"""
        list_name = list_name.split()[0]

        if not tableExists(list_name):
            print("List does not exists!")
            return
        
        deleteTable(list_name)

        self.do_lists(list_name) 

    def do_add(self, args):
        """Adds a TODO to the list"""
        pass

    def do_remove(self, arg):
        """Removes a TODO from the list"""
        pass

    def do_done(self, arg):
        pass

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
    
if __name__ == '__main__':
    MyCLI().cmdloop()
