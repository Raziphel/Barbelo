from utils.database import DatabaseConnection
import asyncpg

class Coins_Record(object):
    all_coins_record = {}

    def __init__(self, user_id:int, earned:int=0, spent:int=0, taxed:int=0, lost:int=0, stolen:int=0, gifted:int=0, given:int=0):
        self.user_id = user_id
        self.earned = earned
        self.spent = spent
        self.taxed = taxed
        self.lost = lost
        self.stolen = stolen
        self.gifted = gifted
        self.given = given

        self.all_coins_record[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO coins
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8)
                ''',
                self.user_id, self.earned, self.spent, self.taxed, self.lost, self.stolen, self.gifted, self.given
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE coins SET
                earned=$2, spent=$3, taxed=$4, lost=$5, stolen=$6, gifted=$7, given=$8
                WHERE
                user_id=$1
                ''',
                self.user_id, self.earned, self.spent, self.taxed, self.lost, self.stolen, self.gifted, self.given
            )


    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_coins_record.get(user_id)
        if user == None:
            return cls(user_id)
        return user


