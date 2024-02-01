from asyncpg import connect as _connect, Connection

class DatabaseConnection(object):

    config = None


    def __init__(self, connection:Connection=None):
        self.conn = connection


    async def connect(self):
        self.conn = await _connect(**self.config)


    async def close(self):
        await self.conn.close()


    async def __aenter__(self):
        if not self.conn:
            self.conn = await _connect(**self.config)
        return self


    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()
        self.conn = None


    async def __call__(self, sql:str, *args):
        '''
        Runs a line of SQL using the internal database
        '''

        #+ Runs the SQL
        x = await self.conn.fetch(sql, *args)

        #? If it got something, return the dict, else None
        if x:
            return x
        if 'select' in sql.casefold() or 'returning' in sql.casefold():
            return []
        return None