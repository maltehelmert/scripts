def fac(n):
    """Compute n factorial."""
    assert n >= 0, "Invalid argument: fac(%s)" % n
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def bin(n, k):
    """Compute n choose k."""
    assert 0 <= k <= n, "Invalid arguments: bin(%s, %s)" % (n, k)
    return fac(n) // (fac(k) * fac(n - k))

def powerset(seq):
    """Generate the power set of seq."""
    atuple = tuple(seq)
    for mask in xrange(2 ** len(atuple)):
        yield [item for bit_no, item in enumerate(atuple) if mask & 1 << bit_no]

def permutations(seq):
    """Generate all permutations of a sequence.
    Implements Knuth's 'Algorithm P' ('plain changes')."""
    alist = list(seq) # Copy list so that we can modify it in place.
    N = len(alist)
    if N <= 1: # Special-case small numbers for speed.
        yield alist
    elif N == 2:
        yield alist
        yield [alist[1], alist[0]]
    else:
        c = [0] * N
        d = [1] * N
        while True:
            yield list(alist)
            s = 0
            for j in xrange(N - 1, -1, -1):
                q = c[j] + d[j]
                if q == j + 1:
                    if j == 0:
                        return
                    s += 1
                elif q >= 0:
                    index1, index2 = j - c[j] + s, j - q + s
                    alist[index1], alist[index2] = alist[index2], alist[index1]
                    c[j] = q
                    break
                d[j] = -d[j]


def tuples(seq, k):
    """Generate all k-tuples over sequence seq."""
    alist = list(seq)
    if k == 0:
        yield ()
    else:
        for rest in tuples(seq, k - 1):
            for elem in alist:
                yield rest + (elem,)


def functions(seq1, seq2):
    """Generate all functions from seq1 to seq2."""
    alist1 = list(seq1)
    alist2 = list(seq2)
    for tup in tuples(seq2, len(alist1)):
        yield zip(alist1, tup)

from collections import defaultdict
def func_to_sets(f):
    result = defaultdict(set)
    for src, dest in f:
        result[dest].add(src)
    return dict(result)
