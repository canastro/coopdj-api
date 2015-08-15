# Set the path
import os, sys, unittest, app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server, Command
from coverage import coverage

manager = Manager(app.app)


class RunServer(Command):
    def run(self):
        app.init()

        app.app.run(
            use_debugger = True,
            use_reloader = True,
            host = '0.0.0.0'
        )

manager.add_command('runserver', RunServer)

class RunTests(Command):

    def run(self):

        cov = coverage(branch=True, include=['app/*'])
        cov.start()

        app.init(
            MONGODB_SETTINGS={'DB': 'testing'},
            TESTING=True,
            CSRF_ENABLED=False
        )

        test_loader = unittest.defaultTestLoader
        test_runner = unittest.TextTestRunner()
        test_suite = test_loader.discover('./tests')


        try:
            test_runner.run(test_suite)
        except:
            pass

        cov.stop()
        cov.save()

        print("\n\nCoverage Report:\n")
        cov.report()
        print("HTML version: " + os.path.join("tmp/coverage/index.html"))

        cov.html_report(directory='tmp/coverage')
        cov.erase()


manager.add_command(
    'test',
    RunTests()
)

if __name__ == "__main__":
    manager.run()
