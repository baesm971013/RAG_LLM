import  redis

class RedisCounter:
    def __init__(
        self,
        conn_redis,
        key,
        is_counter_reset=True,
        init_num=0
    ):
        self.conn_redis = conn_redis
        self.key = key
        
        if isinstance(init_num,int) is False:
            raise Exception("init_num must be Integer")
        self.init_num = init_num
        
        if is_counter_reset is True:
            self.conn_redis.set(name = self.key, value=init_num)

    def plus(self, int_plus_num=1, is_error_reset = True):
        if isinstance(int_plus_num,int) is False:
            raise Exception("Must be integer")
        return int(self.conn_redis.incr(name=self.key, amount = int_plus_num))
    
    def get(self):
        return int(self.conn_redis.get(name=self.key))
      
if __name__ == "__main__":
    conn_redis = redis.Redis(
         host = "localhost",
        port = 6379,
        password = "asianaidt",
        decode_responses=True
    )
    ViewCounter = RedisCounter(conn_redis= conn_redis,key = "ABCService:View:Coutner")
    
    from multiprocessing import Process
    pids = []
    for i in range(999):
        p = Process(target=ViewCounter.plus)
        pids.append(p) p.start()
    for pid in pids:
        pid.join()    
    
    print(ViewCounter.get())
        