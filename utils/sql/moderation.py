from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Moderation(object):
    all_moderation = {}

    def __init__(self, user_id:int, adult:bool=False, child:bool=False, muted:bool=False, image_banned:bool=False):
        self.user_id = user_id
        self.adult = adult
        self.child = child
        self.muted = muted
        self.image_banned = image_banned

        self.all_moderation[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO moderation
                VALUES
                ($1, $2, $3, $4, $5)
                ''',
                self.user_id, self.adult, self.child, self.muted, self.image_banned
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE moderation SET
                adult=$2, child=$3, muted=$4, image_banned=$5
                WHERE
                user_id=$1
                ''',
                self.user_id, self.adult, self.child, self.muted, self.image_banned
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets adult table's connected varibles'''
        user = cls.all_moderation.get(user_id)
        if user == None:
            return cls(user_id)
        return user

    @classmethod
    def sort_moderation(cls):
        '''sorts the user's by balance. getting ranks!'''
        sorted_moderation = sorted(cls.all_moderation.values(), key=lambda u: u.adult, reverse=True)
        return sorted_moderation