"""
Database implementation class
"""

from sqlite3 import Binary

from logging import getLogger
from os.path import exists
from os.path import expandvars
from os.path import join
try:
    from ConfigParser import ConfigParser
    from ConfigParser import NoSectionError
except ImportError:
    from configparser import ConfigParser  # pylint: disable=F0401,W0611
    from configparser import NoSectionError  # pylint: disable=F0401

try:
    from MySQLdb import connect as mysql_connect
    from MySQLdb import Error as MySQLError
except ImportError:
    mysql_connect = None

from sqlite3 import Error as SQLiteError

from sqlite3 import connect as sqlite_connect

class DatabaseError(Exception):
    pass

def get_sql_log_dict():
    parser = ConfigParser()
    parser.read(join(expandvars("%APPDATA%"), 'localbox', 'sync.ini'))
    try:
        dbtype = parser.get('database', 'type')
    except NoSectionError:
        dbtype = "sqlite"
    if dbtype in ['sqlite', 'sqlite3']:
        try:
            ip_address = parser.get('database', 'filename')
        except NoSectionError:
            ip_address = join(expandvars("%APPDATA%"), 'localbox', 'database.sqlite')
    else:
        ip_address = parser.get('database', 'hostname')
    return {'ip': ip_address, 'user': '', 'path': 'database/'}

def database_execute(command, params=None):
    """
    Function to execute a sql statement on the database. Executes the right
    backend and makes sure '?' is replaced for the local substitution variable
    if needed.
    @param command the sql command to execute
    @param params a list of tuple of values to substitute in command
    @returns a list of dictionaries representing the sql result
    """
    getLogger("database").info("database_execute(" + command + ", " +
                               str(params) + ")", extra=get_sql_log_dict())
    parser = ConfigParser()
    parser.read(join(expandvars("%APPDATA%"), 'localbox', 'sync.ini'))
    try:
        dbtype = parser.get('database', 'type')
    except NoSectionError:
        dbtype = 'sqlite'

    if dbtype == "mysql":
        if mysql_execute is None:
            exit("Trying to use a MySQL database without python-MySQL module.")
        command = command.replace('?', '%s')
        return mysql_execute(command, params)

    elif (dbtype in ["sqlite3", "sqlite"]):
        return sqlite_execute(command, params)
    else:
        raise DatabaseError("Unknown database type, cannot continue")


def sqlite_execute(command, params=None):
    """
    Function to execute a sql statement on the mysql database. This function is
    called by the database_execute function when the sqlite backend is set in
    the configuration file
    @param command the sql command to execute
    @param params a list of tuple of values to substitute in command
    @returns a list of dictionaries representing the sql result
    """
    # NOTE mostly copypasta'd from mysql_execute, may be a better way
    getLogger("database").debug("sqlite_execute(" + command + ", " +
                                str(params) + ")", extra=get_sql_log_dict())
    try:
        parser = ConfigParser()
        parser.read(join(expandvars("%APPDATA%"), 'localbox', 'sync.ini'))
 
        try:
            filename = parser.get('database', 'filename')
        except NoSectionError:
            filename = join(expandvars("%APPDATA%"), 'localbox', 'database.sqlite')

        init_db = not exists(expandvars(filename))
        connection = sqlite_connect(filename)
        connection.text_factory = Binary
        cursor = connection.cursor()
        if init_db:
            for sql in ('CREATE TABLE sites (site char(255), client_id'
                        ' char(255), client_secret char(255));',
                        'CREATE TABLE keys (site char(255), user char(255),'
                        ' fingerprint char(40));'):
                if sql != "" and sql is not None:
                    cursor.execute(sql)
                    connection.commit()
        if params:
            cursor.execute(command, params)
        else:
            cursor.execute(command)
        connection.commit()
        return cursor.fetchall()
    except SQLiteError as sqlerror:
        raise DatabaseError("SQLite Error: %d: %s" % (sqlerror.args[0],
                                                      sqlerror.args[1]))
    except NoSectionError:
        raise DatabaseError("Please configure the database section"
                            " in the ini file")
    except TypeError:
        raise DatabaseError("Please configure the 'filename' parameter"
                            " in the [database] section in the ini file")
    finally:
        try:
            if connection:
                connection.close()
        except UnboundLocalError:
            pass


def mysql_execute(command, params=None):
    """
    Function to execute a sql statement on the mysql database. This function is
    called by the database_execute function when the mysql backend is set in
    the configuration file.
    @param command the sql command to execute
    @param params a list of tuple of values to substitute in command
    @returns a list of dictionaries representing the sql result
    """
    getLogger("database").debug("mysql_execute(" + command + ", " + str(params)
                                + ")", extra=get_sql_log_dict())
    parser = ConfigParser()
    parser.read(join(expandvars("%APPDATA%"), 'localbox', 'sync.ini'))
    try:
        host = parser.get('database', 'hostname')
        user = parser.get('database', 'username')
        pawd = parser.get('database', 'password')
        dbse = parser.get('database', 'database')
        port = parser.getint('database', 'port')
        connection = mysql_connect(host=host, port=port, user=user,
                                   passwd=pawd, db=dbse)
        cursor = connection.cursor()
        cursor.execute(command, params)
        connection.commit()
        return cursor.fetchall()
    except MySQLError as mysqlerror:
        string = "MySQL Error: %d: %s" % (mysqlerror.args[0], mysqlerror.args[1])
        getLogger('database').debug(string, extra=get_sql_log_dict())
    finally:
        try:
            if connection:
                connection.close()
        except UnboundLocalError:
            pass


def get_key_and_iv(localbox_path, user):
    """
    Fetches RSA encrypted key and IV from the database
    @param localbox_path (localbox specific) path to the encrypted file
    @param user name of whoes key to fetch
    @return a tuple containing the key and iv for a certain file.
    """
    sql = "select key, iv from keys where path = ? and user = ?"
    try:
        result = database_execute(sql, (localbox_path, user))[0]
    except IndexError:
        extradict = {'ip': '', 'user': user, 'path': localbox_path}
        getLogger("database").debug("cannot find key", extra=extradict)
        result = None
    return result
