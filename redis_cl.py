from redis.asyncio import Redis

class AsyncRedisClient(Redis):
    def __init__(self, redis_instance: Redis, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis = redis_instance

    async def set_sub(self, user_id, product_id):
        await self.redis.sadd(user_id, product_id)
    
    async def get_sub_users(self):
        print('get_sub_users working')
        
        return await self.redis.keys()
    
    async def get_sub_products_ids(self, user_id):
        return await self.redis.smembers(user_id)
    
    async def remove_sub_product(self, user_id, product_id):
        await self.redis.srem(user_id, product_id)
    

    

# Вариант для локального тестирования
# redis_instance = Redis(
#     host='localhost', port=6379, decode_responses=True
# )

redis_instance = Redis(
    host='redis', port=6379, decode_responses=True
)
redis_client = AsyncRedisClient(redis_instance)
