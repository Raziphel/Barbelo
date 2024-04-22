from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Skills(object):
    all_skills = {}

    def __init__(self, user_id:int, thievery:bool=False, larceny:bool=False, larceny_stamp:str=dt.utcnow()):
        self.user_id = user_id
        self.thievery = thievery
        self.larceny = larceny
        self.larceny_stamp = larceny_stamp

        self.all_skills[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO skills
                VALUES
                ($1, $2, $3, $4)
                ''',
                self.user_id, self.thievery, self.larceny, self.larceny_stamp
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE skills SET
                thievery=$2, larceny=$3, larceny_stamp=$4
                WHERE
                user_id=$1
                ''',
                self.user_id, self.thievery, self.larceny, self.larceny_stamp
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets table's connected varibles'''
        user = cls.all_skills.get(user_id)
        if user == None:
            return cls(user_id)
        return user