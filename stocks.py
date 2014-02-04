# Made with love by Austin Bishop
# Feb 2013

# Time analysis:
# 1. sort ~O(nlogn)
# 2. Do jobs (upper bound ~O(N))
# 3. Fix extras ~O(1)

# orders = [
#     stocks.make_o(995, 95, 0),
#     stocks.make_o(833, 76, 0),
#     stocks.make_o(671, 74, 0),
#     stocks.make_o(616, 73, 0),
#     stocks.make_o(541, 65, 0)]
from random import uniform  # random


class order():

    def __init__(self, **kwargs):
        self.MQ = kwargs.get('MQ', int(uniform(500, 1000)))
        self.u = kwargs.get('u', int(uniform(0, 100)))
        self.q = kwargs.get('q', 0)

    def __repr__(self):
        return "Max Quantity: {:<4}, Utility: {:<3}, q Sold: {}".format(
            self.MQ, self.u, self.q)

    def fufill(self, Q_remaining):
        if Q_remaining >= self.MQ:
            self.q = self.MQ
        else:
            self.q = Q_remaining
        return self.q

    def decrement(self, amt):
        if self.q >= amt:
            self.q -= amt
        else:
            print 'error'
        return amt


def make_o(MQ, u, q):
    return order(**{'MQ': MQ, 'u': u, 'q': q})


def print_orders(orders):
    for o in orders:
        print o
    print ''


def simulate(orders=False):
    # N = int(100*random())
    # Q = int(1000*random())
    # N, Q, mQ = 10, 100, 20
    N = 10
    Q = 5000
    Q_remaining = Q
    mQ = 200

    if not orders:
        orders = []
        for i in range(0, N):
            orders.append(order())
        # sort the orders, in increasing order, by u
        orders = sorted(orders, key=lambda x: x.u, reverse=True)

    print_orders(orders)
    for idx, o in enumerate(orders):

        if Q_remaining >= mQ:
            Q_remaining -= o.fufill(Q_remaining)
        elif Q_remaining > 0:
            print 'Extra'
            Q_extra = mQ - Q_remaining
            order_old = orders[idx - 1]
            UT_old = Q_extra * order_old.u
            UT_new = mQ * o.u
            #import pdb; pdb.set_trace()
            if UT_old < UT_new:
                Q_remaining += order_old.decrement(Q_extra)
                Q_remaining -= o.fufill(Q_remaining)
            break
        else:
            break

    print_orders(orders)
    if Q_remaining:
        print "REMAINING: {}".format(Q_remaining)
    print('===========================================')
    return orders, Q_remaining
        # case1: order MQ is less than number of shares remaining Q - QT
        # case2: order MQ is greater than number of remanming shares,
        #   and number of remainin shares is greater than mQ
        # case3: order MQ is greater than number of reminaing shares,
        #   and number of remaining shares is less than mQ


def run_sims(iters):
    for i in range(iters):
        orders, Q_remaining = simulate()
