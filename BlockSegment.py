""" Class for the individual block segments that represent a time slot """

class BlockSegment():
    
    def __init__(self, order=0, y=0, prev=None, next=None, blocks=[]):
        self.order = order
        self.blocks = blocks
        self.y = y
        self.prev = prev
        self.next = next
        self.isFull = False
        self.isBreak = False