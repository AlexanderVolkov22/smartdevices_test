import random
from random import randint

import asyncpg

import constants


async def poolmanager():
    pool = await asyncpg.create_pool(user=constants.postgresuser, password=constants.postgrespassw,
                                     database='test', host=constants.postgresurl)
    return pool


def macgen():
    return ':'.join([hex(randint(0, 255))[2:].upper() for _ in range(5)])


def ipgen():
    a = randint(0, 255)
    b = randint(0, 255)
    c = randint(0, 255)
    d = randint(0, 255)
    return f'{a}.{b}.{c}.{d}'  # Генерация ip адреса


async def devicecreate():
    pool = await poolmanager()
    async with pool.acquire() as conn:
        i = 1
        i2 = 1
        types = ['emeter', 'zigbee', 'lora', 'gsm']
        while i <= 10:
            mac = macgen()  # Функция генерации MAC-адреса
            type = random.choice(types)  # Выбор типа устройства из списка
            await conn.execute('''INSERT INTO devices(id, dev_id, dev_type) VALUES($1, $2, $3)''', i, str(mac),
                               type)
            if i % 2 != 0:
                await conn.execute('''INSERT INTO endpoints(id, device_id, comment) VALUES($1, $2, $3)''', i2, i,
                                   ipgen())
                i2 += 1
            i += 1
    await pool.close()


async def devtypes():
    pool = await poolmanager()
    async with pool.acquire() as conn:
        d = await conn.fetch(
            '''SELECT dev_type, COUNT(*) FROM devices, endpoints WHERE devices.id = endpoints.id GROUP BY dev_type''')
    await pool.close()
    return d
