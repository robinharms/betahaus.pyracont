import colander
from pyramid.interfaces import ISettings
from zope.interface import implements
from zope.component import getUtility

from betahaus.pyracont.interfaces import ITransformUtil
from betahaus.pyracont.interfaces import ITransformation


class TransformUtil(object):
    """ """
    implements(ITransformUtil)

    def output(self, appstruct, schema, **kw):
        return self.apply_transformations(appstruct, schema, 'transform_out', **kw)

    def input(self, appstruct, schema, **kw):
        return self.apply_transformations(appstruct, schema, 'transform_in', **kw)

    def transform_node(self, appstruct, node_name, chain, **kw):
        for tname in chain:
            transformation = getUtility(ITransformation, name = tname)
            transformation(appstruct, node_name, **kw)

    def apply_transformations(self, appstruct, schema, attr, **kw):
#        if hasattr(schema, attr):
#            chain_name = getattr(schema, attr)
#            chain = self.get_chain(chain_name)
#            self.transform_node(appstruct, schema.name, chain, **kw)

        print "\n\nstarting apply for node %s" % schema
        print "appstruct"
        print '---'

        for node in schema.children:
            print "processing node %s" % node
            #Sequence objects should be recursed into
            if isinstance(node.typ, colander.Sequence):
                print 'sequence'
                for sub_app in appstruct.get(node.name, ()):
                    self.apply_transformations(sub_app, node, attr, **kw)
                continue
            else:
                print "mapping"
            if hasattr(node, attr):
                print 'will apply for %s' % node
                chain_name = getattr(node, attr)
                chain = self.get_chain(chain_name)
                self.transform_node(appstruct, node.name, chain, **kw)
                print "Transforming node"
            else:
                print "No attrs set for this node"
            print "Recursing"
            if isinstance(node.typ, colander.Mapping):
                print "Instance is mapping, will recurse regardless of appstruct"
                self.apply_transformations(appstruct, node, attr, **kw)
            if node.name in appstruct:
                print "node name in appstruct, recursing"
                self.apply_transformations(appstruct[node.name], node, attr, **kw)
            else:
                print "node name NOT in appstruct, won't recurse"
                

                
#            if hasattr(node, attr):
#                print 'will apply for %s' % node
#                chain_name = getattr(node, attr)
#                chain = self.get_chain(chain_name)
#                self.transform_node(appstruct, node.name, chain, **kw)
#            else:
#                print 'skipping apply for %s' % node
#            if node.name in appstruct:
#                print 'recursing into %s' % node
#                self.apply_transformations(appstruct[node.name], node, attr, **kw)
#            else:
#                print 'checking children instead of recursing for %s' % node
#                for snode in node.children:
#                    if hasattr(snode, attr):
#                        print 'child %s of %s will be applied - with subsection loop' % (snode, node)
#                        chain_name = getattr(snode, attr)
#                        chain = self.get_chain(chain_name)
#                        #try:
#                        for subsection in appstruct:
#                            self.transform_node(subsection, snode.name, chain, **kw)
#                        #except:
#                        #    import pdb;pdb.set_trace()
#                    else:
#                        print 'skipping apply for child %s of %s' % (snode, node)
#                    if snode.name in appstruct:
#                        print 'recursing into child %s of node %s - with subsection loop' % (snode, node)
#                        for subsection in appstruct:
#                            self.apply_transformations(subsection[snode.name], snode, attr, **kw)
#                    else:
#                        print 'Will not recurse into child %s of node %s' % (snode, node)

    def get_chain(self, chain_name):
        settings = getUtility(ISettings)
        return settings.get("transform.%s" % chain_name, '').strip().splitlines()


class Transformation(object):
    """ Base class for transformations. They're named utils that will be called by the TransformUtil. """
    implements(ITransformation)
    name = None

    def __call__(self, appstruct, node_name, **kw):
        raise NotImplementedError("Must be implemented by subclass")


def includeme(config):
    """ Register transformation util. """
    config.registry.registerUtility(TransformUtil())
