import aioredis
from fastapi import FastAPI, status
import constants
from modules import anagrams, devices
from fastapi.responses import JSONResponse

app = FastAPI()
redis = aioredis.from_url(constants.redis)


@app.post("/devices", responses={400: {'Created': False}, 201: {'Created': True}})
async def create_devices():
    """
        Функция создает 10 устройств в таблице devices и добавляет 5 из них в таблицу endpoints,
        если данные добавленны успешно - статус 201, в ином случае - статус 400
    """
    try:
        await devices.devicecreate()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={'Created': True})
    except:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'Created': False})


@app.get("/anagram/word1={word1}&word2={word2}")
async def anagram_check(word1: str, word2: str):
    """
        Функция проверяет являются строки word1 и word2 анаграммами
    """
    count = await redis.get("anagramcount")  # Получение счетчика Redis
    if count is None:  # Если счетчик пустой, то устанавливаем значение 0
        count = 0
    else:
        count = int(count.decode("utf-8"))
    d = anagrams.anagrams(word1, word2)
    if d is True:  # Если значения являются анаграмами, увеличиваем значение счетчика
        count += 1
        await redis.set("anagramcount", count)
    await redis.close()
    return {"count": count, 'is_anagram': d}


@app.get("/devices")
async def list_devices():
    """
        Функция получает устройства не привязанные к endpoint
    """
    dev = await devices.devtypes()
    return {"dev_types": dev}
