__all__ = ["Lexer", "LexerStateChange"]
import re
import copy


class LexError(Exception):
    def __init__(self, message, text, error_index):
        self.args = (message,)
        self.text = text
        self.error_index = error_index


class PatternError(Exception):
    pass


class LexerBuildError(Exception):
    pass


class LexerStateChange(Exception):
    def __init__(self, newstate, tok=None):
        self.newstate = newstate
        self.tok = tok


class Token(object):
    __slots__ = ("type", "value", "lineno", "index")

    def __repr__(self):
        return f"Token(type={self.type!r}, value={self.value!r}, lineno={self.lineno}, index={self.index})"


class TokenStr(str):
    @staticmethod
    def __new__(cls, value, key=None, remap=None):
        self = super().__new__(cls, value)
        self.key = key
        self.remap = remap
        return self

    def __setitem__(self, key, value):
        if self.remap is not None:
            self.remap[self.key, key] = value

    def __delitem__(self, key):
        if self.remap is not None:
            self.remap[self.key, key] = self.key


class _Before:
    def __init__(self, tok, pattern):
        self.tok = tok
        self.pattern = pattern


class LexerMetaDict(dict):
    def __init__(self):
        self.before = {}
        self.delete = []
        self.remap = {}

    def __setitem__(self, key, value):
        if isinstance(value, str):
            value = TokenStr(value, key, self.remap)
        if isinstance(value, _Before):
            self.before[key] = value.tok
            value = TokenStr(value.pattern, key, self.remap)
        if key in self and not isinstance(value, property):
            prior = self[key]
            if isinstance(prior, str):
                if callable(value):
                    value.pattern = prior
                else:
                    raise AttributeError(f"Name {key} redefined")
        super().__setitem__(key, value)

    def __delitem__(self, key):
        self.delete.append(key)
        if key not in self and key.isupper():
            pass
        else:
            return super().__delitem__(key)

    def __getitem__(self, key):
        if key not in self and key.split("ignore_")[-1].isupper() and key[:1] != "_":
            return TokenStr(key, key, self.remap)
        else:
            return super().__getitem__(key)


class LexerMeta(type):
    @classmethod
    def __prepare__(meta, name, bases):
        d = LexerMetaDict()

        def _(pattern, *extra):
            patterns = [pattern, *extra]

            def decorate(func):
                pattern = "|".join(f"({pat})" for pat in patterns)
                if hasattr(func, "pattern"):
                    func.pattern = pattern + "|" + func.pattern
                else:
                    func.pattern = pattern
                return func

            return decorate

        d["_"] = _
        d["before"] = _Before
        return d

    def __new__(meta, clsname, bases, attributes):
        del attributes["_"]
        del attributes["before"]
        cls_attributes = {
            str(key): str(val) if isinstance(val, TokenStr) else val
            for key, val in attributes.items()
        }
        cls = super().__new__(meta, clsname, bases, cls_attributes)
        cls._attributes = dict(attributes)
        cls._remap = attributes.remap
        cls._before = attributes.before
        cls._delete = attributes.delete
        cls._build()
        return cls


class Lexer(metaclass=LexerMeta):
    tokens = set()
    literals = set()
    ignore = ""
    reflags = 0
    regex_module = re
    _token_names = set()
    _token_funcs = {}
    _ignored_tokens = set()
    _remapping = {}
    _delete = {}
    _remap = {}
    __state_stack = None
    __set_state = None

    @classmethod
    def _collect_rules(cls):
        rules = []
        for base in cls.__bases__:
            if isinstance(base, LexerMeta):
                rules.extend(base._rules)
        existing = dict(rules)
        for key, value in cls._attributes.items():
            if (
                (key in cls._token_names)
                or key.startswith("ignore_")
                or hasattr(value, "pattern")
            ):
                if callable(value) and not hasattr(value, "pattern"):
                    raise LexerBuildError(
                        f"function {value} doesn't have a regex pattern"
                    )
                if key in existing:
                    n = rules.index((key, existing[key]))
                    rules[n] = (key, value)
                    existing[key] = value
                elif isinstance(value, TokenStr) and key in cls._before:
                    before = cls._before[key]
                    if before in existing:
                        n = rules.index((before, existing[before]))
                        rules.insert(n, (key, value))
                    else:
                        rules.append((key, value))
                    existing[key] = value
                else:
                    rules.append((key, value))
                    existing[key] = value
            elif (
                isinstance(value, str)
                and not key.startswith("_")
                and key not in {"ignore", "literals"}
            ):
                raise LexerBuildError(f"{key} does not match a name in tokens")
        rules = [(key, value) for key, value in rules if key not in cls._delete]
        cls._rules = rules

    @classmethod
    def _build(cls):
        if "tokens" not in vars(cls):
            raise LexerBuildError(
                f"{cls.__qualname__} class does not define a tokens attribute"
            )
        cls._token_names = cls._token_names | set(cls.tokens)
        cls._ignored_tokens = set(cls._ignored_tokens)
        cls._token_funcs = dict(cls._token_funcs)
        cls._remapping = dict(cls._remapping)
        for (key, val), newtok in cls._remap.items():
            if key not in cls._remapping:
                cls._remapping[key] = {}
            cls._remapping[key][val] = newtok
        remapped_toks = set()
        for d in cls._remapping.values():
            remapped_toks.update(d.values())
        undefined = remapped_toks - set(cls._token_names)
        if undefined:
            missing = ", ".join(undefined)
            raise LexerBuildError(f"{missing} not included in token(s)")
        cls._collect_rules()
        parts = []
        for tokname, value in cls._rules:
            if tokname.startswith("ignore_"):
                tokname = tokname[7:]
                cls._ignored_tokens.add(tokname)
            if isinstance(value, str):
                pattern = value
            elif callable(value):
                cls._token_funcs[tokname] = value
                pattern = getattr(value, "pattern")
            part = f"(?P<{tokname}>{pattern})"
            try:
                cpat = cls.regex_module.compile(part, cls.reflags)
            except Exception as e:
                raise PatternError(f"Invalid regex for token {tokname}") from e
            if cpat.match(""):
                raise PatternError(f"Regex for token {tokname} matches empty input")
            parts.append(part)
        if not parts:
            return
        cls._master_re = cls.regex_module.compile("|".join(parts), cls.reflags)
        if not isinstance(cls.ignore, str):
            raise LexerBuildError("ignore specifier must be a string")
        if not all(isinstance(lit, str) for lit in cls.literals):
            raise LexerBuildError("literals must be specified as strings")

    def begin(self, cls):
        assert isinstance(cls, LexerMeta), "state must be a subclass of Lexer"
        if self.__set_state:
            self.__set_state(cls)
        self.__class__ = cls

    def push_state(self, cls):
        if self.__state_stack is None:
            self.__state_stack = []
        self.__state_stack.append(type(self))
        self.begin(cls)

    def pop_state(self):
        self.begin(self.__state_stack.pop())

    def tokenize(self, text, lineno=1, index=0):
        _ignored_tokens = (
            _master_re
        ) = _ignore = _token_funcs = _literals = _remapping = None

        def _set_state(cls):
            nonlocal _ignored_tokens, _master_re, _ignore, _token_funcs, _literals, _remapping
            _ignored_tokens = cls._ignored_tokens
            _master_re = cls._master_re
            _ignore = cls.ignore
            _token_funcs = cls._token_funcs
            _literals = cls.literals
            _remapping = cls._remapping

        self.__set_state = _set_state
        _set_state(type(self))
        _mark_stack = []

        def _mark():
            _mark_stack.append((type(self), index, lineno))

        self.mark = _mark

        def _accept():
            _mark_stack.pop()

        self.accept = _accept

        def _reject():
            nonlocal index, lineno
            cls, index, lineno = _mark_stack[-1]
            _set_state(cls)

        self.reject = _reject
        self.text = text
        try:
            while True:
                try:
                    if text[index] in _ignore:
                        index += 1
                        continue
                except IndexError:
                    return
                tok = Token()
                tok.lineno = lineno
                tok.index = index
                m = _master_re.match(text, index)
                if m:
                    index = m.end()
                    tok.value = m.group()
                    tok.type = m.lastgroup
                    if tok.type in _remapping:
                        tok.type = _remapping[tok.type].get(tok.value, tok.type)
                    if tok.type in _token_funcs:
                        self.index = index
                        self.lineno = lineno
                        tok = _token_funcs[tok.type](self, tok)
                        index = self.index
                        lineno = self.lineno
                        if not tok:
                            continue
                    if tok.type in _ignored_tokens:
                        continue
                    yield tok
                else:
                    if text[index] in _literals:
                        tok.value = text[index]
                        tok.type = tok.value
                        index += 1
                        yield tok
                    else:
                        self.index = index
                        self.lineno = lineno
                        tok.type = "ERROR"
                        tok.value = text[index:]
                        tok = self.error(tok)
                        if tok is not None:
                            yield tok

                        index = self.index
                        lineno = self.lineno
        finally:
            self.text = text
            self.index = index
            self.lineno = lineno

    def error(self, t):
        raise LexError(
            f"Sacalon : Illegal character {t.value[0]!r} at index {self.index}",
            t.value,
            self.index,
        )
