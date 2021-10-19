import sqlite3

class Person:
    def __init__(self, first, last, age):
        first : str
        last : str 
        age : int 
        # use datatypes as it allows for better cohesion between the persn object and the database 
        self._id = self.increment_id()
        self.first = first
        self.last = last
        self.age = age 
        self.connection = sqlite3.connect('mydata.db')
        self.cursor = self.connection.cursor() # remember to 
        #commit and close the connection at the end of each action 
    
    def __str__(self):
        return '''
        Person(
            name: {},
            last name: {},
            age: {}
        )
        '''.format(self.first, self.last, self.age)

    def increment_id(self):
        self.create_all()
        connection = sqlite3.connect('mydata.db')
        cursor = connection.cursor()
        cursor.execute('''
        SELECT * FROM persons
        ''')
        rows = cursor.fetchall()
        connection.commit()
        connection.close()
        _id = len(rows) + 1
        return _id

    def add_person(self):
        self.create_all()
        self.cursor.execute('''
        INSERT INTO persons VALUES
        ({},'{}','{}',{})
        '''.format(self._id, self.first, self.last, int(self.age)))
        self.connection.commit()
        self.connection.close()
        
    def load_person(self, _id):
        self.create_all()
        self.cursor.execute('''
        SELECT * FROM persons
        WHERE ID = {}
        '''.format(_id))
        person_ = self.cursor.fetchone()
        self.connection.close()
        return person_

    def create_all(self):
        database_name = 'mydata.db'
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS persons (
            ID INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            age INTEGER
        )
        ''')
        connection.commit()
        self.connection = connection