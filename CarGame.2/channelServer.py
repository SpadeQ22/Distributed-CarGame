import json
import os
from redis.cluster import RedisCluster
import uuid

class Channel:
    def __init__(self, flush=False):
        # self.address_mapping = {
        #     ("172.31.28.112", 6379): ("54.211.23.63", 6379),
        #     ("172.31.28.7", 6379): ("54.90.175.60", 6379),
        #     ("172.31.31.154", 6379): ("50.19.55.253", 6379),
        #     ("172.31.25.0", 6379): ("50.17.9.93", 6379),
        #     ("172.31.28.52", 6379): ("34.228.37.76", 6379),
        #     ("172.31.30.28", 6379): ("18.205.22.37", 6379),
        #     ("172.31.31.143", 6379): ("75.101.200.157", 6379)
        # }
        self.channel = RedisCluster(host='172.31.28.112', port=6379, read_from_replicas=True)
        print("Connected to Cluster -- Success")
        self.osmembers = {}
        if flush:
            self.channel.flushall()

    def map(self, src):
        return self.address_mapping[src]

    def join(self, subgroup):
        if os.getpid() not in self.osmembers.keys():
            newpid = uuid.uuid4()
            self.osmembers[os.getpid()] = newpid
        else:
            newpid = self.osmembers[os.getpid()]
        if self.channel.sismember(subgroup, str(newpid)):
            return str(newpid)
        self.channel.sadd('members', str(newpid))
        self.channel.sadd(subgroup, str(newpid))
        return str(newpid)

    def leave(self, subgroup):
        ospid = os.getpid()
        pid = self.osmembers[ospid]
        assert self.channel.sismember('members', str(pid)), ''
        del self.osmembers[ospid]
        self.channel.srem('members', str(pid))
        self.channel.srem(subgroup, str(pid))
        return

    def force_leave(self, subgroup, uuid):
        caller = self.osmembers[os.getpid()]
        pid = uuid
        assert self.channel.sismember('members', str(pid)), ''
        self.channel.srem('members', str(pid).encode())
        self.channel.srem(subgroup, str(pid).encode())
        self.channel.delete(json.dumps([str(pid), str(caller)]))
        self.channel.delete(json.dumps([str(caller), str(pid)]))
        return

    def exists(self, pid):
        return self.channel.sismember('members', str(pid))

    def bind(self, pid):
        ospid = os.getpid()
        self.osmembers[ospid] = str(pid)

    # print "Process "+str(ospid)+" ["+pid+"] joined "
    # print self.osmembers

    def subgroup(self, subgroup):
        return [i.decode('UTF-8') for i in self.channel.smembers(subgroup)]

    def sendTo(self, destinationSet, message):
        caller = self.osmembers[os.getpid()]
        assert self.channel.sismember('members', str(caller)), ''
        for i in destinationSet:
            assert self.channel.sismember('members', str(i))
            self.channel.rpush(json.dumps([str(caller), str(i)]), json.dumps(message))

    def sendToAll(self, message):
        caller = self.osmembers[os.getpid()]
        assert self.channel.sismember('members', str(caller)), ''
        for i in self.channel.smembers('members'):
            self.channel.rpush(json.dumps([str(caller), str(i)]), json.dumps(message))

    def recvFromAny(self, timeout=0):
        caller = self.osmembers[os.getpid()]
        assert self.channel.sismember('members', str(caller)), ''
        members = self.channel.smembers('members')
        xchan = [json.dumps([str(i), str(caller)]) for i in members]
        msg = self.channel.blpop(xchan, timeout)
        if msg:
            return [msg[0].split("'")[0], msg[0].split("'")[1], json.loads(msg[1])]

    def recvFrom(self, senderSet, timeout=0):
        caller = self.osmembers[os.getpid()]
        assert self.channel.sismember('members', str(caller)), ''
        for i in senderSet:
            assert self.channel.sismember('members', i), ''
        xchan = [json.dumps([str(i), str(caller)]) for i in senderSet]
        msg = self.channel.blpop(xchan, timeout)
        if msg:
            return [json.loads(msg[0].decode('UTF-8'))[1], json.loads(msg[1].decode('UTF-8'))]
        else:
            return None
