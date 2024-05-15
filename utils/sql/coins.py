from utils.database import DatabaseConnection
import asyncpg

class Coins(object):
    all_coins = {}

    def __init__(self, user_id:int, coins:int=0, earned:int=0, spent:int=0, taxed:int=0, lost:int=0, stolen:int=0, gifted:int=0, given:int=0, banked:int=0):
        self.user_id = user_id
        self.coins = coins
        self.earned = earned
        self.spent = spent
        self.taxed = taxed
        self.lost = lost
        self.stolen = stolen
        self.gifted = gifted
        self.given = given
        self.banked = banked

        self.all_coins[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO coins
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                ''',
                self.user_id, self.coins, self.earned, self.spent, self.taxed, self.lost, self.stolen, self.gifted, self.given, self.banked
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE coins SET
                coins=$2, earned=$3, spent=$4, taxed=$5, lost=$6, stolen=$7, gifted=$8, given=$9, banked=$10
                WHERE
                user_id=$1
                ''',
                self.user_id, self.coins, self.earned, self.spent, self.taxed, self.lost, self.stolen, self.gifted, self.given, self.banked
            )


    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_coins.get(user_id)
        if user == None:
            return cls(user_id)
        return user


    @classmethod
    def sort_coins(cls):
        '''sorts the user's by balance. getting ranks!'''
        sorted_coins = sorted(cls.all_coins.values(), key=lambda u: u.coins, reverse=True)
        return sorted_coins


    @classmethod 
    def get_total_coins(cls):
        '''
        Gets all the user's collected amount of gold 
        '''
        total = 0
        for i in cls.all_coins.values():
            total += i.coins
        return total


    @classmethod
    def delete(cls, user_id:int):
        '''
        Removes a user from cache via their ID, fails silently if not present
        '''
        try:
            del cls.all_coins[user_id]
        except KeyError:
            pass