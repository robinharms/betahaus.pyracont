from pyramid.config import Configurator
from pyramid_zodbconn import get_connection



def main(global_config, **settings):
    """ This is a simple demo app to demonstrate how both the transformation tool works
        and how content types can be constructed.
    """
    config = Configurator(root_factory=root_factory, settings=settings)
    config.scan('betahaus.pyracont.demoapp')
    config.include('betahaus.pyracont.transformation')
    config.add_static_view('deform', 'deform:static')
    config.hook_zca()
    return config.make_wsgi_app()


def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())


def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        from betahaus.pyracont.factories import createContent
        site_root = createContent('Content')
        site_root.set_field_value('title', 'Site root')
        site_root.set_field_value('text', 'Edit this text and add a hashtag')
        zodb_root['app_root'] = site_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']

