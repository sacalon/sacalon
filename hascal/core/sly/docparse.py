__all__ = [ 'DocParseMeta' ]
class DocParseMeta(type):
    @staticmethod
    def __new__(meta, clsname, bases, clsdict):
        if '__doc__' in clsdict:
            lexer = meta.lexer()
            parser = meta.parser()
            lexer.cls_name = parser.cls_name = clsname
            lexer.cls_qualname = parser.cls_qualname = clsdict['__qualname__']
            lexer.cls_module = parser.cls_module = clsdict['__module__']
            parsedict = parser.parse(lexer.tokenize(clsdict['__doc__']))
            assert isinstance(parsedict, dict), 'Parser must return a dictionary'
            clsdict.update(parsedict)
        return super().__new__(meta, clsname, bases, clsdict)
    @classmethod
    def __init_subclass__(cls):
        assert hasattr(cls, 'parser') and hasattr(cls, 'lexer')