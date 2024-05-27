from utils.database import DatabaseConnection
import asyncpg

class Currency(object):
    all_currency = {}

    def __init__(self, user_id:int, coins:int=0, credits:int=0):
        self.user_id = user_id
        self.coins = coins
        self.credits = credits

        self.all_currency[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO currency
                VALUES
                ($1, $2, $3)
                ''',
                self.user_id, self.coins, self.credits
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE currency SET
                coins=$2, credits=$3
                WHERE
                user_id=$1
                ''',
                self.user_id, self.coins, self.credits
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_currency.get(user_id)
        if user == None:
            return cls(user_id)
        return user

