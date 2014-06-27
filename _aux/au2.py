from decimal import *

INTEREST_RATE = Decimal('0.99998')
BASE_PRICE    = Decimal(1)

getcontext().prec = 15
PREC = Decimal(10) ** -6

def dmul(a,b):
    return (a*b).quantize(PREC, rounding=ROUND_DOWN)
def dadd(a,b):
    return (a+b).quantize(PREC, rounding=ROUND_DOWN)
def dsub(a,b):
    return (a-b).quantize(PREC, rounding=ROUND_DOWN)

class Account:
    def __init__(self, name):
        self.name           = name
        self.means          = Decimal(0)
        self.withdraw       = Decimal(0)
        self.payback        = Decimal(0)
        self.ownershipPrice = None
    def __str__(self):
        return self.name + ": " + str(self.means) + " " + str(self.withdraw)

startBasePrice = Decimal(1)

def reset():
    global accounts
    global winner
    global ticks
    global changes
    global currentBasePrice
    changes = {}
    accounts = []
    winner = None
    ticks = 0
    currentBasePrice = startBasePrice

reset()

def newBasePrice(bp):
    print "[%d] new base price (%f)" % (ticks+1, bp)
    changes[ticks]=bp

def tick(n=1):
    global winner
    global ticks
    global currentBasePrice
    while n>0:
        if winner != None:
            payment = dmul(winner.ownershipPrice, currentBasePrice)
            if winner.means < payment:
                print "[%d] winner is lost (%s)" % (ticks+1, winner)
                winner = None
            else:
                winner.means    = dsub(winner.means, payment)
                winner.withdraw = dadd(winner.withdraw, payment)
        for acc in accounts:
            acc.means   = dmul(acc.means, INTEREST_RATE)
            acc.payback = dmul(acc.payback, dsub(Decimal(2), INTEREST_RATE))
        if ticks in changes:
            currentBasePrice = changes[ticks]
        ticks += 1
        n-=1

def bid(acc, bid):
    global winner
    if winner != None:
        if winner.ownershipPrice > bid:
            raise Exception()
        if acc != winner:
            print "[%d] payback to %s: %s" % (ticks+1, winner.name, winner.payback)
    payment = Decimal(0)
    basePrice = startBasePrice
    for i in range(0,ticks):
        payment = dadd(payment, dmul(basePrice, bid))
        if i in changes:
            basePrice = changes[i]
    if dadd(acc.means, acc.withdraw) < payment:
        raise Exception("Needed at least %f means" % (dsub(payment, acc.withdraw)))
    delta = max(dsub(payment, acc.withdraw), Decimal(0))
    acc.means    = dsub(acc.means, delta)
    acc.withdraw = dadd(acc.withdraw, delta)
    acc.ownershipPrice = bid
    winner = acc
    print "[%d] %s bids %f" % (ticks+1, acc.name, bid)

def newAcc(name, means):
    acc         = Account(name)
    acc.means   = means
    acc.payback = means
    accounts.append(acc)
    print "[%d] new acc %s with %d" % (ticks+1, acc.name, means)
    return acc

def transfer(acc, means):
    acc.means = dadd(acc.means, means)
    acc.payback = dadd(acc.payback, means)
    print "[%d] transfer %d to %s" % (ticks+1, means, acc.name)

def dump(accs):
    for acc in accs:
        print "[%d] %s" % (ticks, acc)
    print ""

#x create audition
x = newAcc("x", Decimal(72))
bid(x, Decimal(1))
tick()
dump([x])

#  n blocks pass
tick(60)
dump([x])

#x do transfer
transfer(x, Decimal(3000))
tick()
dump([x])

tick(50)
dump([x])

#y joins the audition & makes higher bid & x loses ownership
y = newAcc("y", Decimal(2200))
bid(y, Decimal(2))
tick(1)
dump([y])

# tick(45)
# dump([x])

# tick(5)

# #z joins and makes minimal bid
# z = newAcc("z", Decimal(1000))
# bid(z, Decimal(1))
# tick(1)
# dump([z])

# tick(196-69)
# dump([z, x])

# tick(5448+69)
# dump([x])
# tick(1)
# dump([x])

# print "############## CLOSE"

# startBasePrice = Decimal(2)
# reset()

# x = newAcc("x", Decimal(14000))
# bid(x, Decimal(1))
# tick()
# dump([x])

# tick(6048)
# dump([x])
