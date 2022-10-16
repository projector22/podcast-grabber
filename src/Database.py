from src.Hash import md5

class Database:
    """Tool for handling database functions within the context of the app.
    """
    def __init__(self, db_name: str) -> None:
        """Class Constructor

        Args:
            db_name (str): Name of the database to be worked on.
        """
        self.db_name = db_name


    def connect(self):
        """Connect to the database and prepare connection & cursor properties.
        """
        import sqlite3
        from os.path import exists
        first_run = False
        if (exists(self.db_name) == False):
            first_run = True
        self.conn = sqlite3.connect(self.db_name)
        if first_run == True:
            self._write_tables()
        self.cursor = self.conn.cursor()


    def _write_tables(self) -> None:
        """Write the default tables to the database.
        """
        self.conn.execute(
            '''CREATE TABLE subscribed_podcasts
            (
                table_id CHAR(35) PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                image TEXT NOT NULL,
                hash CHAR(32) NOT NULL
            );
            '''
        )


    def subscribe_to_new_podcast(self, podcast_title: str, podcast_image: str, podcast_hash: str, entries: dict) -> None:
        """Create a new podcast table for episodes of a subscribed podcast.

        Args:
            podcast_title (str): The title of the podcast to subscribe to.
            podcast_image (str): The url to the cover image of the podcast.
            entries (dict): the 
        """
        new_table_name = 'pn_' + md5(podcast_title)

        self.conn.execute(
        '''CREATE TABLE {table_name}
            (
                guid CHAR(32) PRIMARY KEY NOT NULL,
                title TEXT NOT NULL,
                audio TEXT NOT NULL,
                duration TEXT NOT NULL,
                site_url TEXT NOT NULL,
                date_published INT NOT NULL,
                downloaded INT NOT NULL DEFAULT 0
            );
            '''.format(table_name=new_table_name)
        )

        sql = '''INSERT INTO subscribed_podcasts 
            (table_id,name,image,hash)
            VALUES
            (?,?,?,?);
            '''
        self.conn.execute(
            sql, (new_table_name, podcast_title, podcast_image, podcast_hash)
        )
        self.conn.commit()

        for line in entries:
            guid = md5(line)
            data = entries[line]
            title = data['title']
            audio = data['audioLink']
            duration = data['duration']
            link = data['siteURL']
            pub_date = self._get_timestamp(data['published'])

            sql = '''INSERT INTO {table_name}
            (guid,title,audio,duration,site_url,date_published)
            VALUES
            (?,?,?,?,?,?)
            '''.format(table_name=new_table_name)
            self.conn.execute(
                sql, (guid, title, audio, duration, link, pub_date)
            )
            self.conn.commit()


    def _get_timestamp(self, timestr: str) -> int:
        parts = timestr.split()
        day = int(parts[1])
        month = self._get_month(parts[2])
        year = int(parts[3])
        times = parts[4].split(':')
        hour = int(times[0])
        min = int(times[1])
        sec = int(times[2])
        from datetime import datetime
        import time
        date_time = datetime(year, month, day, hour, min, sec)
        return int(time.mktime(date_time.timetuple()))


    def _get_month(self, month: str) -> int:
        """Get the selected month as an int.

        Args:
            month (str): 3 letter month string.

        Returns:
            int: month number.
        """
        months = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12,
        }
        return months[month]


    def list_tables(self) -> list:
        """Generate a list of tables in the database.

        Returns:
            list: List of table names
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = []
        results = self.cursor.fetchall()
        for table in results:
            tables.append(table[0])
        return tables


    def _kill(self):
        """Kill the script immediately.
        """
        import sys
        sys.exit()
