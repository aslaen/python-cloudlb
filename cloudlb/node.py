# -*- encoding: utf-8 -*-
__author__ = "Chmouel Boudjnah <chmouel@chmouel.com>"
from cloudlb.base import SubResource, SubResourceDict


class NodeDict(SubResourceDict):
    def get(self, nodeId):
        for d in self.dico:
            if d.id == nodeId:
                return d


class Node(SubResource):
    def __repr__(self):
        return "<Node: %s:%s>" % (self.address, self.port)

    def __init__(self,
                 weight=None,
                 parent=None,
                 address=None,
                 port=None,
                 condition=None,
                 status=None,
                 id=None,
                 **kwargs):
        self.port = port
        self.weight = weight
        self.address = address
        self.condition = condition
        self.status = status
        self.id = id
        self._parent = parent
        self._originalInfo = self.toDict(includeNone=True)

        if not all([self.port, self.address, self.condition]):
            #TODO: Proper Exceptions
            raise Exception("You need to specify a" + \
                                " port address and a condition")

    def delete(self):
        self._parent.manager.delete_node(self._parent.id,
                                         self.id,
                                         )

    def update(self):
        ret = {}
        dico = self.toDict()
        #Not allowed to update.
        dico.pop('address')
        dico.pop('port')
        for k in dico.keys():
            if k in self._originalInfo and dico[k] != self._originalInfo[k]:
                ret[k] = dico[k]
        if not ret:
            #TODO: Proper exceptions
            raise Exception("Nothing to update nothing has changed.")

        self._parent.manager.update_node(self._parent.id,
                                         self.id, ret)
