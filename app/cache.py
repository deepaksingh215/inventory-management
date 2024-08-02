import aioredis
import json
import schemas
from typing import Optional

redis = aioredis.from_url("redis://localhost")


async def set_item_to_cache(item_id: int, item: schemas.Item):
    item_dict = item.dict()
    item_json = json.dumps(item_dict)
    await redis.set(item_id, item_json)


async def get_item_from_cache(item_id: int) -> Optional[schemas.Item]:
    item_json = await redis.get(item_id)
    if item_json:
        item_dict = json.loads(item_json)
        return schemas.Item(**item_dict)
    return None
