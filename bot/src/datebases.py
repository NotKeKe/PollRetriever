import aiosqlite
import orjson
from collections import defaultdict
import asyncio

from bot.utils.time import to_datetime, current_datetime_obj

_locks = defaultdict(asyncio.Lock)

class Schedule:
    PATH = './data/schedule.db'

    @classmethod
    async def create_table(cls):
        async with aiosqlite.connect(cls.PATH) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    msg_id INTEGER NOT NULL,
                    event TEXT NOT NULL,
                    description TEXT,
                    available_times TEXT,
                    final_detect_time TEXT,
                    vote_end_time TEXT,
                    status TEXT NOT NULL DEFAULT 'voting'
                )
            ''')
            await db.commit()

    @classmethod
    async def init_schedule(cls, msg_id: int, event: str, vote_end_time: str, description: str = None):
        time = to_datetime(vote_end_time)
        
        if ( current_datetime_obj() - time ).total_seconds() <= 0:
            return 'Invaild Time'
        
        async with aiosqlite.connect(cls.PATH) as db:
            await db.execute(
                "INSERT INTO schedules (msg_id, event, description, vote_end_time) VALUES (?, ?, ?, ?)",
                (msg_id, event, description, vote_end_time)
            )
            await db.commit()

    @classmethod
    async def add_user_available_time(cls, msg_id: int, user_id: int, time: str):
        async with _locks[msg_id]:
            async with aiosqlite.connect(cls.PATH) as db:
                db.row_factory = aiosqlite.Row
                
                cursor = await db.execute("SELECT available_time FROM schedules WHERE msg_id = ?", (msg_id,))
                row = await cursor.fetchone()
 
                new_user_entry = {'user_id': user_id, 'time': [time]}
 
                if row is None or not row['available_time']:
                    json_to_insert = orjson.dumps([new_user_entry])
                    await db.execute(
                        "INSERT INTO schedules (msg_id, available_time) VALUES (?, ?) "
                        "ON CONFLICT(msg_id) DO UPDATE SET available_time = excluded.available_time",
                        (msg_id, json_to_insert)
                    )
                else:
                    current_data: list = orjson.loads(row['available_time'])
                    
                    user_found = False
                    for entry in current_data:
                        if entry.get('user_id') == user_id:
                            if time not in entry['time']:
                                entry['time'].append(time)
                            user_found = True
                            break
                    
                    if not user_found:
                        current_data.append(new_user_entry)
 
                    json_to_update = orjson.dumps(current_data)
                    await db.execute(
                        "UPDATE schedules SET available_time = ? WHERE msg_id = ?",
                        (json_to_update, msg_id)
                    )
 
                await db.commit()

    @classmethod
    async def detect_final_time(cls, msg_id: int):
        async with aiosqlite.connect(cls.PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT final_time FROM schedules WHERE msg_id = ?", (msg_id,))
            #TODO

    @classmethod
    async def add_time(cls, user_id: int, event: str, description: str, time: str):
        ...

    @classmethod
    async def add_schedule(cls, event: str, description: str = None):
        async with aiosqlite.connect(cls.PATH) as db:
            await db.execute("INSERT INTO schedules (event, description) VALUES (?, ?)", (event, description))
            await db.commit()

    @classmethod
    async def get_all_schedules(cls):
        async with aiosqlite.connect(cls.PATH) as db:
            async with db.execute("SELECT event, description FROM schedules") as cursor:
                return await cursor.fetchall()
