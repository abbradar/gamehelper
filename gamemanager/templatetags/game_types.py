from ..views import GameDetailView, CharacterDetailView
from django.template import Library, TemplateSyntaxError
from functools import partial

register = Library()

# practically copied from future.url, URLnode with few modifications
class DynamicURLNode(Node):
    def __init__(self, view_name, args, kwargs, asvar):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        from django.core.urlresolvers import NoReverseMatch
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k, 'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])

        view_name = self.view_name
        resolver = self.get_resolver(context)

        url = ''
        try:
            url = resolver.reverse(view_name, args=args, kwargs=kwargs)
        except NoReverseMatch, e:
            if self.asvar is None:
                raise e

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url

def dynamic_url(parser, token, node):
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    viewname = parser.compile_filter(bits[1])
    args = []
    kwargs = {}
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to url tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))

    return node(viewname, args, kwargs, asvar)

class GameURLNode(DynamicURLNode):
    def get_resolver(self, context):
        try:
            object = context['game']
        except KeyError:
            raise TemplateSyntaxError("Game dynamic URL resolve works only with game exported in context.")
        return game_detail_view.get_resolver(object.type)

class CharacterURLNode(DynamicURLNode):
    def get_resolver(self, context):
        try:
            object = context['character']
        except KeyError:
            raise TemplateSyntaxError("Character dynamic URL resolve works only with character exported in context.")
        return character_detail_view.get_resolver(object.type)

game_url = register_tag(partial(dynamic_url, node=GameURLNode))
character_url = register_tag(partial(dynamic,url, node=CharacterURLNode))
