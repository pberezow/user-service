import os, subprocess, argparse, sys
from server.config import FLASK_APP, DEFAULT_IP


class Command:
    def __init__(self, name, descr, runcmd, env={}):
        self.name = name
        self.descr = descr
        self.runcmd = runcmd
        self.env = env

    def run(self, conf):
        cmd = self.runcmd(conf)
        env = os.environ
        env.update(self.env)
        env.update(conf)
        subprocess.call(cmd, env=env, shell=True)


class CommandManager:
    def __init__(self):
        self.commands = {}

    def add(self, command):
        self.commands[command.name] = command

    def configure(self, conf):
        self.conf = conf

    def run(self, command):
        if command in self.commands:
            self.commands[command].run(self.conf)
        else:
            print("Unknown command.")
            print(self.available_commands())

    def available_commands(self):
        commands = sorted(self.commands.values(), key=lambda c: c.name)
        space = max([len(c.name) for c in commands]) + 2
        description = 'Available commands:\n'
        for c in commands:
            description += '  ' + c.name + ' ' * (space - len(c.name)) + c.descr + '\n'
        return description


cm = CommandManager()

cm.add(Command(
    "build",
    "compiles python files in project into .pyc binaries",
    lambda c: 'python3 -m compileall .'))

cm.add(Command(
    "start",
    "runs server with gunicorn in a production setting",
    lambda c: 'gunicorn -b {0}:{1} server:app'.format(c['host'], c['port']),
    {
        'FLASK_APP': FLASK_APP,
        'FLASK_DEBUG': 'false'
    }))

cm.add(Command(
    "run",
    "runs dev server using Flask's native debugger & backend reloader",
    lambda c: 'python3 -m flask run --host={0} --port={1} --debugger --reload'.format(c['host'], c['port']),
    {
        'FLASK_APP': FLASK_APP,
        'FLASK_DEBUG': 'true'
    }))

cm.add(Command(
    "debug",
    "runs dev server in debug mode; use with an IDE's remote debugger",
    lambda c: 'python3 -m flask run --host={0} --port={1} --no-debugger --no-reload'.format(c['host'], c['port']),
    {
        'FLASK_APP': FLASK_APP,
        'FLASK_DEBUG': 'true'
    }))

cm.add(Command(
    "test",
    "runs all tests inside of `tests` directory",
    lambda c: 'python3 -m unittest discover -s tests -p "*.py"'))

# Create and format argument parser for CLI
parser = argparse.ArgumentParser(description=cm.available_commands(),
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("command", help="command to run (see list above)")
parser.add_argument("ipaddress", nargs='?', default=DEFAULT_IP,
                    help="address and port to run on (i.e. {0})".format(DEFAULT_IP))

# Take in command line input for configuration
try:
    args = parser.parse_args()
    cmd = args.command
    addr = args.ipaddress.split(':')
    cm.configure({
        'host': addr[0],
        'port': addr[1],
    })
    cm.run(cmd)
except:
    if len(sys.argv) == 1:
        print(cm.available_commands())
    sys.exit(0)
