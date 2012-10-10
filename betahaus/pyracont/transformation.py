import colander
from pyramid.interfaces import ISettings
from zope.interface import implements
from zope.component import getUtility

from betahaus.pyracont.interfaces import ITransformUtil
from betahaus.pyracont.interfaces import ITransformation


class TransformUtil(object):
    """ See .interfaces.ITransformUtil """
    implements(ITransformUtil)

    def output(self, appstruct, schema, **kw):
        return self.apply_transformations(appstruct, schema, 'transform_out', **kw)

    def input(self, appstruct, schema, **kw):
        return self.apply_transformations(appstruct, schema, 'transform_in', **kw)

    def transform_node(self, appstruct, node_name, chain, **kw):
        for tname in chain:
            transformation = getUtility(ITransformation, name = tname)
            transformation.appstruct(appstruct, node_name, **kw)

    def apply_transformations(self, appstruct, schema, attr, **kw):
        for node in schema.children:
            #Sequence objects should be recursed into.
            #In that case appstruct will be a list or a similar iterable
            if isinstance(node.typ, colander.Sequence):
                for sub_app in appstruct.get(node.name, ()):
                    self.apply_transformations(sub_app, node, attr, **kw)
                continue
            #Transform this node
            if hasattr(node, attr):
                chain_name = getattr(node, attr)
                chain = self.get_chain(chain_name)
                self.transform_node(appstruct, node.name, chain, **kw)
            #If current node is a mapping node, we should recurse into it.
            if isinstance(node.typ, colander.Mapping):
                self.apply_transformations(appstruct, node, attr, **kw)
            
            if node.name in appstruct:
                self.apply_transformations(appstruct[node.name], node, attr, **kw)

    def get_chain(self, chain_name):
        settings = getUtility(ISettings)
        return settings.get("transform.%s" % chain_name, '').strip().splitlines()


class Transformation(object):
    """ See .interfaces.ITransformation
        You can inherit this baseclass to implement the interface.
    """
    implements(ITransformation)
    name = None

    def appstruct(self, appstruct, node_name, **kw): #pragma : no cover
        raise NotImplementedError("Must be implemented by subclass")

    def simple(self, value, **kw): #pragma : no cover
        raise NotImplementedError("Must be implemented by subclass")


def includeme(config):
    """ Register transformation util. """
    config.registry.registerUtility(TransformUtil())
