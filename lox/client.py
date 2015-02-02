'''

Main module

Usage:

    import lox.client

    lox.client.main()

'''

import os
import sys
import time
import traceback
from getpass import getpass

import lox.config as config
from lox.api import LoxApi
from lox.daemon import Daemon, DaemonError
from lox.session import LoxSession
from lox.error import LoxError
import lox.gui as gui


__author__ = "imtal@yolt.nl"
__copyright__ = "(C) 2014, see LICENSE file"
__version__ = "0.2"


class Supervisor(Daemon):
    '''
    The daemon: start the sessions as threads and start the GUI
    '''
    sessions = dict()

    def started(self, restart=False):
        if restart:
            print "\nLocalbox daemon restarted\n"
        else:
            print "\nLocalbox daemon started\n"

    def run(self, interactive = False):
        for name in config.settings.iterkeys():
            self.add(name, interactive)
        if interactive:
            # console mainloop
            try:
                while True: time.sleep(2)
            except KeyboardInterrupt:
                for name in self.sessions.iterkeys():
                    self.sessions[name].stop()
                for name in self.sessions.iterkeys():
                    self.sessions[name].join()
        else:
            gui.mainloop()
            self.stop()


    def terminate(self):
        for name in self.sessions.iterkeys():
            self.remove(name)

    '''
    Use the following functoins only from within the daemon
    '''
    def add(self, name, interactive=False):
        self.sessions[name] = LoxSession(name, interactive)
        self.sessions[name].start()

    def remove(self, name):
        self.sessions[name].stop()
        while self.sessions[name].is_alive():
            time.sleep(1)
        del self.sessions[name]

    def restart(self,name):
        self.sessions[name].stop()
        while self.sessions[name].is_alive():
            time.sleep(1)
        self.sessions[name].start()


def need_sessions():
    '''
    Check if there are any sessions specified in config file
    '''
    if len(config.settings)==0:
        print "\nNo sessions configured, use command 'add'\n"
        sys.exit(1)


def cmd_start(daemon):
    '''
    Start the deamon
    '''
    need_sessions()
    passcode = getpass("Passcode: ")
    daemon.start()

def cmd_stop(daemon):
    '''
    Stop the daemon
    '''
    if not daemon.status() is None:
        daemon.stop()
        print "\nLocalbox daemon stopped\n"
    else:
        print "\nLocalbox daemon not running\n"

def cmd_run(daemon):
    '''
    Run the deamon interactive in the foreground
    '''
    console_msg("run in foreground")
    daemon.run(interactive = True)

def cmd_restart(daemon):
    '''
    Restart daemon
    '''
    daemon.restart()

def cmd_status(daemon):
    '''
    Show status of daemon
    '''
    s = daemon.status()
    if s is None:
        print "\nLocalbox daemon not running ...\n"
    else:
        print "\nLocalbox daemon running with pid {}\n".format(s)

def cmd_add(daemon):
    '''
    Add account
    '''
    if len(sys.argv)>2:
        name = sys.argv[2]
        if config.settings.has_key(name):
            print "Error: a session with name '{}' already exists".format(name)
        else:
            print "\nAdd Localbox session '{}'".format(name)
            for (setting,caption,default) in config.SETTINGS:
                value = raw_input("  {0} [{1}]: ".format(caption,default))
                config.settings[name][setting] = default if value=="" else value
            config.save()
            if not daemon.status() is None:
                y = raw_input("Start session [yes]: ")
                if y=="" or y=="yes":
                    daemon.restart()
        print ""
    else:
        cmd = os.path.basename(sys.argv[0])
        print "\nUsage: {0} add <name>\n".format(cmd,sys.argv[1])

def cmd_delete(daemon):
    '''
    Delete account
    '''
    if len(sys.argv)>2:
        name = sys.argv[2]
        if not config.settings.has_key(name):
            print "\nError: a session with name '{}' is not configured\n".format(name)
        else:
            config.settings.pop(name)
            config.save()
            if not daemon.status() is None:
                daemon.restart()
    else:
        cmd = os.path.basename(sys.argv[0])
        print "\nUsage: {0} delete <name>\n".format(cmd,sys.argv[1])

def cmd_edit(daemon):
    '''
    Edit configuration walking through accounts one by one
    '''
    if len(sys.argv)>2:
        name = sys.argv[2]
        if config.settings.has_key(name):
            print "Error: a session with name '{}' already exists".format(name)
        else:
            print "\nAdd a Localbox session with name '{}'".format(name)
            for (setting,caption,default) in config.SETTINGS:
                value = raw_input("  {0} [{1}]: ".format(caption,default))
                config.settings[name][setting] = default if value=="" else value
            config.save()
            if not daemon.status() is None:
                y = raw_input("Start this session [yes]: ")
                if y=="" or y=="yes":
                    daemon.restart()
        print ""
    else:
        cmd = os.path.basename(sys.argv[0])
        print "\nUsage: {0} edit <name>\n".format(cmd,sys.argv[1])

def cmd_list(daemon):
    '''
    List the configured sessions
    '''
    print "\nLocalbox sessions configured:\n"
    for name in config.settings.iterkeys():
        print "  {0:12} ({1})".format(name,config.settings[name]["lox_url"])
    print ""

def cmd_help(daemon):
    '''
    Show help
    '''
    cmd = os.path.basename(sys.argv[0])
    print "\nLocalbox desktop sync version {}\n".format(__version__)
    print "Usage: {} [command]".format(cmd)
    print ""
    for c in commands.iterkeys():
        (f,description) = commands[c]
        print "  {0:12} - {1}".format(c,description)
    print ""
    sys.exit(0)

def cmd_invitations(daemon):
    '''
    Show invirtations for each session
    '''
    need_sessions()
    print "\nLocalbox invitations:\n"
    for name in config.settings.iterkeys():
        print "Session '{}': ".format(name)
        try:
            api = LoxApi(name)
            invitations = api.invitations()
            for invite in invitations:
                share = invite[u'share']
                item = share[u'item']
                print "  [%s] %s (%s)" % (invite[u'id'],item[u'path'],invite[u'state'])
        except IOError as e:
            print "\nError: {}\n".format(str(e))
        else:
            print ""
    sys.exit(0)

def cmd_accept(daemon):
    pass

def cmd_revoke(daemon):
    pass

def cmd_usage():
    cmd = os.path.basename(sys.argv[0])
    print "\nUsage: {0} start|stop|run|status|help|... \n".format(cmd)
    sys.exit(1)

commands = {
                "start": (cmd_start,"starts the client"),
                "stop": (cmd_stop,"stops the client"),
                "run": (cmd_run, "run in foreground (interactive)"),
                "restart": (cmd_restart, "reloads the confguration"),
                "add": (cmd_add, "add an account"),
                "list": (cmd_list, "list configured sessions"),
                "edit": (cmd_edit, "edit configuration"),
                "delete": (cmd_delete, "delete session from configuration"),
                "status": (cmd_status,"show the status of the client"),
                "invitations": (cmd_invitations,"show invitations"),
                "accept": (cmd_accept,"accept invitation"),
                "revoke": (cmd_revoke,"revoke invitation"),
                "help": (cmd_help,"show this help")
           }

def main():
    '''
    Main routine: call routine from command
    '''
    cmd = sys.argv[1].lower() if len(sys.argv)>1 else cmd_usage()
    pidfile = os.environ['HOME']+'/.lox/lox-client.pid'
    logfile = os.environ['HOME']+'/.lox/lox-client.log'
    daemon = Supervisor(pidfile, path=os.environ['HOME'], umask=100, stdout=logfile, stderr=logfile)
    try:
        (func,description) = commands[cmd]
        func(daemon)
    except KeyError as e:
        print "\nError: invalid command\n"
        cmd_usage()
        sys.exit(1)
    except (DaemonError, LoxError) as e:
        print "\nError: {}\n".format(str(e))
        sys.exit(1)
    except KeyboardInterrupt as e:
        print "Error: interrupted"
        sys.exit(1)
    except Exception as e:
        print "Error: {}".format(str(e))
        traceback.print_exc()
        sys.exit(1)
