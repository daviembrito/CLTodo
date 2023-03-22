import cmd
from rich.table import Table
from task import Task

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

    def do_lists(self, args):
        pass

    def do_select(self, arg):
        pass

    def do_show(self, arg):
        pass

    def do_add(self, args):
        pass

    def do_remove(self, arg):
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
