#!/usr/bin/python
"""Deck a filesystem

Options:
  -m            mounts deck (the default)
  -u            unmount deck (also refresh's the deck's fstab)
  -r            refresh the deck's fstab (without unmounting)
  -D            delete the deck

  -t --isdeck   test if path is a deck
     --isdirty  test if deck is dirty
     
"""
import sys
import help
import getopt

import deck

@help.usage(__doc__)
def usage():
    print >> sys.stderr, "Syntax: %s /path/to/dir/or/deck /path/to/new/deck" % sys.argv[0]
    print >> sys.stderr, "Syntax: %s [ -options ] /path/to/existing/deck" % sys.argv[0]

def fatal(s):
    print >> sys.stderr, "fatal: " + str(s)
    sys.exit(1)

class RigidVal:
    class AlreadySetError(Exception):
        pass
    
    def __init__(self):
        self.val = None

    def set(self, val):
        if self.val is not None:
            raise self.AlreadySetError()
        self.val = val

    def get(self):
        return self.val

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'tmurD',
                                       ['isdirty', 'isdeck'])
    except getopt.GetoptError, e:
        usage(e)

    rigid = RigidVal()
    try:
        for opt, val in opts:
            if opt == '-h':
                usage()
            elif opt == '-m':
                rigid.set(deck.mount)
            elif opt == '-u':
                rigid.set(deck.umount)
            elif opt == '-D':
                rigid.set(deck.delete)
            elif opt == '-r':
                rigid.set(deck.refresh_fstab)
            elif opt in ('-t', '--isdeck'):
                rigid.set(deck.isdeck)
            elif opt == '--isdirty':
                rigid.set(deck.isdirty)
    except rigid.AlreadySetError:
        fatal("conflicting deck options")

    if not args:
        usage()
        
    func = rigid.get()
    if func is None:
        if len(args) == 2:
            func = deck.create
            
        elif len(args) == 1:
            func = deck.mount

    if func is not deck.create and len(args) != 1:
        usage("bad number of arguments")

    try:
        if func in (deck.isdeck, deck.isdirty):
            path = args[0]
            error = func(path) != True
            sys.exit(error)
        elif func is deck.create:
            source_path, new_deck = args
            func(source_path, new_deck)
        else:
            existing_deck = args[0]
            func(existing_deck)
    except deck.Error, e:
        fatal(e)
    
if __name__=="__main__":
    main()

