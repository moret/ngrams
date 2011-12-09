import redis

class RedisDB(object):
    def persist(self, ngrams, year):
        pipe = redis.Redis().pipeline()

        for grams_len in range(len(ngrams)):
            key = '%d:%d_gram' % (year, grams_len + 1)
            for gram, count in ngrams[grams_len].items():
                # redis-py known bug -
                # https://github.com/andymccurdy/redis-py/issues/70
                pipe.zincrby(key, gram, count)

        pipe.execute()

    def range(self, gram_size, how_many, year):
        conn = redis.Redis()
        key = '%d:%d_gram' % (year, gram_size + 1)
        return conn.zrange(key, -how_many, -1, withscores=True)

    def clear_year(self, year):
        conn = redis.Redis()
        grams_len = 1
        while conn.delete('%d:%d_gram' % (year, grams_len + 1)):
            grams_len += 1

redis_db = RedisDB()
