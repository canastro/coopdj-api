# Set the path
import os, sys, unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server, Command
from app import app

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)

class RunTests(Command):

    def run(self):
        test_loader = unittest.defaultTestLoader
        test_runner = unittest.TextTestRunner()
        test_suite = test_loader.discover('./tests')
        test_runner.run(test_suite)

manager.add_command('test', RunTests())

if __name__ == "__main__":
    manager.run()
