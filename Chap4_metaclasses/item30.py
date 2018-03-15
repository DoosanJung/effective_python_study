#!/usr/bin/env python
'''
Consider @property instead of refactoring attributes
'''
from datetime import datetime, timedelta

# plain Python objects
class Bucket(object):
    """
    A leaky bucket quota.
    Bucket class represents how much quota remains
    and the duration for which the quota will be available
    """
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return 'Bucket(quota=%d)' % self.quota

def fill(bucket, amount):
    """
    When the bucket is filled, the amount of quota
    does not carry over from one period to the next
    """
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount

def deduct(bucket, amount):
    """
    Each time a quota consumer do something, ensure that
    it can deduct the amount of quota it needs to use
    """
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True

# Keeping track of max_quota issued, quota_consumed in the period
class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return ('Bucket(max_quota=%d, quota_consumed=%d)' %
                (self.max_quota, self.quota_consumed))

    # to compute the current level of quota on-the-fly
    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    # fill and deduct
    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # Quota being reset for a new period
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # Quota being filled for the new period
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            # Quota being consumed during the period
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta


if __name__=="__main__":
    print("plain Python objects")
    bucket = Bucket(60)
    print(bucket)
    print(" ")

    print("fill..")
    bucket = Bucket(60)
    fill(bucket, 100)
    print(bucket)
    print(" ")

    print("deduct..")
    if deduct(bucket, 99):
        print('Had 99 quota')
    else:
        print('Not enough for 99 quota')
    print(bucket)
    print(" ")

    print("deduct more than a bucket has")
    if deduct(bucket, 3):
        print('Had 3 quota')
    else:
        print('Not enough for 3 quota')
    print(bucket)
    print("the bucket's quota level remains unchanged")
    print(" ")

    print("Keeping track of max_quota issued, quota_consumed in the period")
    print(
    """
    class Bucket(object):
        def __init__(self, period):
            self.period_delta = timedelta(seconds=period)
            self.reset_time = datetime.now()
            self.max_quota = 0
            self.quota_consumed = 0

        def __repr__(self):
            return ('Bucket(max_quota=%d, quota_consumed=%d)' %
                    (self.max_quota, self.quota_consumed))

        # to compute the current level of quota on-the-fly
        @property
        def quota(self):
            return self.max_quota - self.quota_consumed

        # fill and deduct
        @quota.setter
        def quota(self, amount):
            delta = self.max_quota - amount
            if amount == 0:
                # Quota being reset for a new period
                self.quota_consumed = 0
                self.max_quota = 0
            elif delta < 0:
                # Quota being filled for the new period
                assert self.quota_consumed == 0
                self.max_quota = amount
            else:
                # Quota being consumed during the period
                assert self.max_quota >= self.quota_consumed
                self.quota_consumed += delta
    """
    )
    bucket = Bucket(60)
    print('Initial', bucket)
    fill(bucket, 100)
    print('Filled', bucket)
    print(" ")

    if deduct(bucket, 99):
        print('Had 99 quota')
    else:
        print('Not enough for 99 quota')

    print('Now', bucket)
    print(" ")
    if deduct(bucket, 3):
        print('Had 3 quota')
    else:
        print('Not enough for 3 quota')

    print('Still', bucket)
    print(" ")
