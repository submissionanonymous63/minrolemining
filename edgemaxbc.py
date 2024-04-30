#! /usr/bin/python3

import sys
import time
import os
import datetime
from readup import readup
from readup import uptopu
from removedominatorsbp import hasbeenremoved
from removedominatorsbp import neighbours
from removedominatorsbp import removedominators
from removedominatorsbp import saveem
from removedominatorsbp import readem
from removedominatorsbp import dmfromem
from findcliquesbp import getedgeset
from findcliquesbp import find_bicliquesbp
from maxsetsbp import maxsetsbp

def removeedge(tope, mc, em, dm, up, pu, seq):
    if not mc:
        m = 0
        mc = None
        st = time.time()
        for c in find_bicliquesbp(em, up, pu, [tope]):
            if len(c) > m:
                m = len(c)
                mc = sorted(c)
            if time.time() - st > 1800:
                print('removeedge(): 1800s exceeded for edge', tope)
                break
        et = time.time()

        print('m:', m, ', tope:', tope, ', time taken:', et - st)
        sys.stdout.flush()

    print('removeedge(); m:', len(mc), ', tope:', tope)
    sys.stdout.flush()
    negone = False

    #Overwrite tope, because we don't care
    tope = tuple((-1,-1))
    for e in mc:
        if hasbeenremoved(e, em):
            continue
        t = None
        if not negone:
            # pick this one to be the "root"
            t = tuple((-1,-1))
            em[e] = tuple((-1, -1, seq))
            tope = e
            negone = True
        else:
            t = tuple((tope[0], tope[1]))
            em[e] = tuple((tope[0], tope[1], seq))
        seq += 1

        if t not in dm:
            dm[t] = set()
        (dm[t]).add(e)

    return seq

def removeedges(remedgelist, remmclist, em, dm, up, pu, seq):
    for idx, tope in enumerate(remedgelist):
        #if hasbeenremoved(tope, em):
        #    print('removeedges():', tope, 'already has been removed!')
        #    sys.stdout.flush()
        #    continue
        newseq = None
        if remmclist:
            newseq = removeedge(tope, remmclist[idx], em, dm, up, pu, seq)
        else:
            newseq = removeedge(tope, None, em, dm, up, pu, seq)
        print(tope, 'removed; # edges removed:', newseq - seq)
        sys.stdout.flush()
        seq = newseq

    return seq

def main():
    print('Start time:', datetime.datetime.now())
    sys.stdout.flush()

    if len(sys.argv) != 2:
        print('Usage: ', end = '')
        print(sys.argv[0], end = ' ')
        print('<input-file>')
        return
    up = readup(sys.argv[1])

    if not up:
        return

    pu = uptopu(up)

    nedges = 0
    for u in up:
        nedges += len(up[u])

    print('Total # edges:', nedges)
    sys.stdout.flush()

    timeone = time.time()
    timetwo = time.time()

    emfilename = sys.argv[1]+'-em.txt'

    if not os.path.isfile(emfilename):
        print('Removing doms + zero-neighbour edges...')
        sys.stdout.flush()
        em = dict()
        dm = dict()
        seq = 0
        seq = removedominators(em, dm, up, seq)
        timetwo = time.time()
        print('done! Time taken:', timetwo - timeone)
        sys.stdout.flush()
        print('Saving em to', emfilename, end=' ')
        sys.stdout.flush()
        saveem(em, emfilename)
        print('done!')
        sys.stdout.flush()
    else:
        print('Reading em from', emfilename, end=' ')
        sys.stdout.flush()
        em = readem(emfilename)
        print('done!')
        sys.stdout.flush()
        print('Determining dm and seq', end=' ')
        sys.stdout.flush()
        dm = dmfromem(em)
        seq = 0
        for e in em:
            if seq < em[e][2]:
                seq = em[e][2]
        print('done!')
        sys.stdout.flush()

    print("Original # edges:", nedges)
    print('# dominators + zero neighbour edges removed:', seq)
    nzerodeg = 0
    if tuple((-1,-1)) in dm:
        nzerodeg = len(dm[tuple((-1, -1))])

    print('# edges with -1 annotation:', nzerodeg)
    sys.stdout.flush()

    print('# remaining edges:', nedges - seq)
    sys.stdout.flush()

    remedgelist = list()
    remmclist = list()

    # add to remedgelist and, optionally, to remmclist the edges whose large maximal bicliques we want
    # to remove. remmclist, if None, forces the method to search for that large maximal biclique

    seq = removeedges(remedgelist, remmclist, em, dm, up, pu, seq)
    print('New seq:', seq)

    print('len(-1)s:', len(dm[tuple((-1,-1))]))
    sys.stdout.flush()

    print('Saving em after edge-removal to', emfilename, end=' ')
    sys.stdout.flush()
    saveem(em, emfilename)
    print('done!')
    sys.stdout.flush()

    # The following searches for large-sized maximal bicliques

    CSIZE_THRESH = 200
    nc = 0
    timeone = time.time()
    for c in find_bicliquesbp(em, up, pu, list()):
        if not nc:
            timetwo = time.time()
            print('First clique found, time taken:', timetwo - timeone, '...')
            sys.stdout.flush()
        nc += 1
        if len(c) >= CSIZE_THRESH:
            print(os.getpid(), 'tope:', c[0], ', topm:', len(c))
            print(set(c))
        if not (nc % 1000):
            timetwo = time.time()
            print('# cliques:', nc, '; time taken:', timetwo - timeone, '...')
            sys.stdout.flush()
            timeone = time.time()

    print('End time:', datetime.datetime.now())

if __name__ == '__main__':
    main()
