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

    @classmethod
    def sort_coins(cls):
        '''sorts the user's by balance. getting ranks!'''
        sorted_coins = sorted(cls.all_currency.values(), key=lambda u: u.coins, reverse=True)
        return sorted_coins


    @classmethod 
    def get_total_coins(cls):
        '''
        Gets all the user's collected amount of gold 
        '''
        total = 0
        for i in cls.all_currency.values():
            total += i.coins
        return total


    @classmethod
    def delete(cls, user_id:int):
        '''
        Removes a user from cache via their ID, fails silently if not present
        '''
        try:
            del cls.all_currency[user_id]
        except KeyError:
            pass