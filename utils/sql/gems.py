from utils.database import DatabaseConnection
import asyncpg

class gems(object):
    all_gems = {}

    def __init__(self, user_id:int, silver:int=0, gold:int=0, diamond:int=0, emerald:int=0, ruby:int=0, sapphire:int=0, amethyst:int=0, hellstone:int=0):
        self.user_id = user_id
        self.diamond = diamond
        self.emerald = emerald
        self.ruby = ruby
        self.sapphire = sapphire
        self.amethyst = amethyst
        self.hellstone = hellstone

        self.all_gems[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO gems
                VALUES
                ($1, $2, $3, $4, $5, $6, $7)
                ''',
                self.user_id, self.emerald, self.diamond, self.ruby, self.sapphire, self.amethyst, self.hellstone
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE gems SET
                emerald=$2, diamond=$3, ruby=$4, sapphire=$5, amethyst=$6, hellstone=$7
                WHERE
                user_id=$1
                ''',
                self.user_id, self.emerald, self.diamond, self.ruby, self.sapphire, self.amethyst, self.hellstone
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_gems.get(user_id)
        if user == None:
            return cls(user_id)
        return user