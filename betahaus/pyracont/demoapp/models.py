import re

from betahaus.pyracont import BaseFolder
from betahaus.pyracont import Transformation
from betahaus.pyracont.decorators import content_factory
from betahaus.pyracont.decorators import transformator


@content_factory('Content')
class Content(BaseFolder):
    pass


TAG_PATTERN = re.compile(r'(\A|\s|[,.;:!?])#(?P<tag>\w*[\w-]+)(\w*)', flags=re.UNICODE)


@transformator()
class HashtagLink(Transformation):
    name = 'hashtag_link'
    
    def appstruct(self, appstruct, node_name, **kw):
        appstruct[node_name] = self.simple(appstruct[node_name], **kw)

    def simple(self, value, **kw):
        from webhelpers.html import HTML
        request = kw['request']

        def handle_match(matchobj):
            pre, tag, post = matchobj.group(1, 2, 3)
            link = {'href': request.resource_url(request.context, '', query={'tag': tag}).replace(request.application_url, ''),
                    'class': "tag",}
            return pre + HTML.a('#%s' % tag, **link) + post
    
        return re.sub(TAG_PATTERN, handle_match, value)


@transformator()
class HashtagToTag(Transformation):
    name = 'hashtags_as_tags'
    
    def appstruct(self, appstruct, node_name, **kw):
        from webhelpers.html import HTML

        request = kw['request']

        for matchobj in re.finditer(TAG_PATTERN, appstruct[node_name]):
            tag = matchobj.group(2)
            if tag not in appstruct['tags']:
                appstruct['tags'].append({'title': tag})

    def simple(self, value, **kw):
        raise NotImplementedError('Not possible to run simple on this transformation.')
            
        