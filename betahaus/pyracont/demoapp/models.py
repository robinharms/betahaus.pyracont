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
    
    def __call__(self, appstruct, node_name, **kw):
        from webhelpers.html import HTML
        if node_name not in appstruct:
            return #nothing to do

        request = kw['request']

        def handle_match(matchobj):
            pre, tag, post = matchobj.group(1, 2, 3)
            link = {'href': request.resource_url(request.context, '', query={'tag': tag}).replace(request.application_url, ''),
                    'class': "tag",}
            
            return pre + HTML.a('#%s' % tag, **link) + post
    
        appstruct[node_name] = re.sub(TAG_PATTERN, handle_match, appstruct[node_name])

@transformator()
class HashtagToTag(Transformation):
    name = 'hashtags_as_tags'
    
    def __call__(self, appstruct, node_name, **kw):
        from webhelpers.html import HTML
        if node_name not in appstruct:
            return #nothing to do

        request = kw['request']

        for matchobj in re.finditer(TAG_PATTERN, appstruct[node_name]):
            tag = matchobj.group(2)
            if tag not in appstruct['tags']:
                appstruct['tags'].append({'title': tag})

            
        