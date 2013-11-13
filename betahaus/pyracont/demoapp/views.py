from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
try:
    import deform
except ImportError:
    pass
    #FIXME: Create a separate dummy package to avoid import errors

from betahaus.pyracont.factories import createSchema
from betahaus.pyracont.interfaces import ITransformUtil


@view_config(renderer = 'view.pt')
def view(context, request):
    schema = createSchema('ContentSchema')
    form = deform.Form(schema)
    response = {}
    response['form_resources'] = form.get_widget_resources()
    appstruct = context.get_field_appstruct(schema)
    response['appstruct'] = appstruct
    transform = request.registry.getUtility(ITransformUtil)
    transform.output(appstruct, schema, request = request)
    response['form'] = form.render(appstruct = appstruct,
                                   readonly = True)
    return response

@view_config(name = 'edit', renderer = 'edit.pt')
def edit(context, request):
    schema = createSchema('ContentSchema')
    form = deform.Form(schema, buttons = ('save',))
    response = {}
    response['form_resources'] = form.get_widget_resources()
    response['appstruct'] = context.get_field_appstruct(schema)

    if 'save' in request.POST:
        try:
            # try to validate the submitted values
            controls = request.POST.items()
            appstruct = form.validate(controls)
            response['appstruct'] = appstruct
            transform = request.registry.getUtility(ITransformUtil)
            transform.input(appstruct, schema, request = request)
            context.set_field_appstruct(appstruct)
            return HTTPFound(location = '/')
        except deform.ValidationFailure as e:
            # the submitted values could not be validated
            response['form'] = e.render()
            return response

    response['form'] = form.render(appstruct = response['appstruct'])
    return response

