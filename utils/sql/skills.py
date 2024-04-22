from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Skills(object):
    all_skills = {}

    def __init__(self, user_id:int, thievery:int=0, larceny:int=0):
        self.user_id = user_id
        self.thievery = thievery
        self.larceny = larceny

        self.all_skills[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO skills
                VALUES
                ($1, $2, $3)
                ''',
                self.user_id, self.thievery, self.larceny
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE skills SET
                thievery=$2, larceny=$3
                WHERE
                user_id=$1
                ''',
                self.user_id, self.thievery, self.larceny
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets table's connected varibles'''
        item = cls.all_skills.get(user_id)
        if item == None:
            return cls(
                user_id = user_id,
                thievery = 0,
                larceny = 0,
            )
        return item