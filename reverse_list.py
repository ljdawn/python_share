#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Node(object):
    def __init__(self, data, p=0):
        self.data = data
        self.next = p


class Reverse(object):
    def __init__(self):
        self.head = 0

    def initlist(self):
        print "input numbers here. '!' to quit"
        try:
            data =  raw_input()
            if data is not '!':
                self.head = Node(int(data))
            p = self.head
            while data != '!':
                data = raw_input()
                if data == '!':
                    break
                else:
                    p.next = Node(int(data))
                    p = p.next
        except ValueError:
            print "input error!"
        finally:z
            print "end"

    def rever(self):
        self.initlist()
        p = self.head
        nex = self.head.next
        pre = Node(0)

        while self.head.next != 0:
            nex = self.head.next
            self.head.next = pre
            pre = self.head
            self.head = nex
        self.head.next = pre
        pre = self.head
        #debug
        print "reverse\t",
        while pre.next != 0:
            print pre.data,
            pre = pre.next

if __name__ == '__main__':
    # test data
    # data = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    l = Reverse()
    l.rever()
