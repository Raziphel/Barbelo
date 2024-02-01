from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Tracking(object):
    all_tracking = {}

    def __init__(self, user_id:int, messages:int=0, vc_mins:int=0, last_bump:str=dt.now(), color:int=0):
        self.user_id = user_id
        self.messages = messages
        self.vc_mins = vc_mins
        self.last_bump = last_bump
        self.color = color

        self.all_tracking[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO tracking
                VALUES
                ($1, $2, $3, $4, $5)
                ''',
                self.user_id, self.messages, self.vc_mins, self.last_bump, self.color
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE tracking SET
                messages=$2, vc_mins=$3, last_bump=$4, color=$5
                WHERE
                user_id=$1
                ''',
                self.user_id, self.messages, self.vc_mins, self.last_bump, self.color
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_tracking.get(user_id)
        if user == None:
            return cls(user_id)
        return user
