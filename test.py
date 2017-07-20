import sqlite3

if __name__ == '__main__':

    """Connects to the specific database."""
    db = sqlite3.connect('/tmp/flaskr.db')
    db.row_factory = sqlite3.Row
    db.close()
