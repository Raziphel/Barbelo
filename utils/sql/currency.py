from utils.database import DatabaseConnection
import asyncpg

class Currency(object):
    all_currency = {}

    def __init__(self, user_id:int, coins:int=0, coins_earned:int=0, last_coin:str=None, xp:int=0, xp_earned:int=0, last_xp:str=None, lot_tickets:int=0):
        self.user_id = user_id
        self.coins = coins
        self.coins_earned = coins_earned
        self.last_coin = last_coin
        self.xp = xp
        self.xp_earned = xp_earned
        self.last_xp = last_xp
        self.lot_tickets = lot_tickets

        self.all_currency[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO currency
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8)
                ''',
                self.user_id, self.coins, self.coins_earned, self.last_coin, self.xp, self.xp_earned, self.last_xp, self.lot_tickets
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE currency SET
                coins=$2, coins_earned=$3, last_coin=$4, xp=$5, xp_earned=$6, last_xp=$7, lot_tickets=$8
                WHERE
                user_id=$1
                ''',
                self.user_id, self.coins, self.coins_earned, self.last_coin, self.xp, self.xp_earned, self.last_xp, self.lot_tickets
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
    def sort_tickets(cls):
        '''sorts the user's by tickets. getting ranks!'''
        sorted_tickets = sorted(cls.all_currency.values(), key=lambda u: u.lot_tickets, reverse=True)
        return sorted_tickets


    @classmethod 
    def get_total_tickets(cls):
        '''Gets total tickets'''
        total = 0
        for i in cls.all_currency.values():
            total += i.lot_tickets
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

