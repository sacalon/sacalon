import sys
import inspect
from collections import OrderedDict, defaultdict, Counter
import colorama

__all__        = [ 'Parser' ]

class YaccError(Exception):
    pass

ERROR_COUNT = 3
MAXINT = sys.maxsize

class SlyLogger(object):
    def __init__(self, f):
        self.f = f

    def debug(self, msg, *args, **kwargs):
        self.f.write((msg % args) + '\n')

    info = debug

    def warning(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        self.f.write('ERROR: ' + (msg % args) + '\n')

    critical = debug

class YaccSymbol:
    def __str__(self):
        return self.type

    def __repr__(self):
        return str(self)

class YaccProduction:
    __slots__ = ('_slice', '_namemap', '_stack')
    def __init__(self, s, stack=None):
        self._slice = s
        self._namemap = { }
        self._stack = stack

    def __getitem__(self, n):
        if n >= 0:
            return self._slice[n].value
        else:
            return self._stack[n].value

    def __setitem__(self, n, v):
        if n >= 0:
            self._slice[n].value = v
        else:
            self._stack[n].value = v

    def __len__(self):
        return len(self._slice)

    @property
    def lineno(self):
        for tok in self._slice:
            if isinstance(tok, YaccSymbol):
                continue
            lineno = getattr(tok, 'lineno', None)
            if lineno:
                return lineno
        raise AttributeError('No line number found')

    @property
    def index(self):
        for tok in self._slice:
            if isinstance(tok, YaccSymbol):
                continue
            index = getattr(tok, 'index', None)
            if index is not None:
                return index
        raise AttributeError('No index attribute found')

    def __getattr__(self, name):
        if name in self._namemap:
            return self._namemap[name](self._slice)
        else:
            nameset = '{' + ', '.join(self._namemap) + '}'
            raise AttributeError(f'No symbol {name}. Must be one of {nameset}.')

    def __setattr__(self, name, value):
        if name[:1] == '_':
            super().__setattr__(name, value)
        else:
            raise AttributeError(f"Can't reassign the value of attribute {name!r}")

class Production(object):
    reduced = 0
    def __init__(self, number, name, prod, precedence=('right', 0), func=None, file='', line=0):
        self.name     = name
        self.prod     = tuple(prod)
        self.number   = number
        self.func     = func
        self.file     = file
        self.line     = line
        self.prec     = precedence
        
        self.len  = len(self.prod)

        self.usyms = []
        symmap = defaultdict(list)
        for n, s in enumerate(self.prod):
            symmap[s].append(n)
            if s not in self.usyms:
                self.usyms.append(s)
                
        namecount = defaultdict(int)
        for key in self.prod:
            namecount[key] += 1
            if key in _name_aliases:
                for key in _name_aliases[key]:
                    namecount[key] += 1

        nameuse = defaultdict(int)
        namemap = { }
        for index, key in enumerate(self.prod):
            if namecount[key] > 1:
                k = f'{key}{nameuse[key]}'
                nameuse[key] += 1
            else:
                k = key
            namemap[k] = lambda s,i=index: s[i].value
            if key in _name_aliases:
                for n, alias in enumerate(_name_aliases[key]):
                    if namecount[alias] > 1:
                        k = f'{alias}{nameuse[alias]}'
                        nameuse[alias] += 1
                    else:
                        k = alias
                    namemap[k] = lambda s,i=index,n=n: ([x[n] for x in s[i].value]) if isinstance(s[i].value, list) else s[i].value[n]

        self.namemap = namemap
                
        self.lr_items = []
        self.lr_next = None

    def __str__(self):
        if self.prod:
            s = '%s -> %s' % (self.name, ' '.join(self.prod))
        else:
            s = f'{self.name} -> <empty>'

        if self.prec[1]:
            s += '  [precedence=%s, level=%d]' % self.prec

        return s

    def __repr__(self):
        return f'Production({self})'

    def __len__(self):
        return len(self.prod)

    def __nonzero__(self):
        raise RuntimeError('Used')
        return 1

    def __getitem__(self, index):
        return self.prod[index]

    def lr_item(self, n):
        if n > len(self.prod):
            return None
        p = LRItem(self, n)
        try:
            p.lr_after = Prodnames[p.prod[n+1]]
        except (IndexError, KeyError):
            p.lr_after = []
        try:
            p.lr_before = p.prod[n-1]
        except IndexError:
            p.lr_before = None
        return p

class LRItem(object):
    def __init__(self, p, n):
        self.name       = p.name
        self.prod       = list(p.prod)
        self.number     = p.number
        self.lr_index   = n
        self.lookaheads = {}
        self.prod.insert(n, '.')
        self.prod       = tuple(self.prod)
        self.len        = len(self.prod)
        self.usyms      = p.usyms

    def __str__(self):
        if self.prod:
            s = '%s -> %s' % (self.name, ' '.join(self.prod))
        else:
            s = f'{self.name} -> <empty>'
        return s

    def __repr__(self):
        return f'LRItem({self})'

def rightmost_terminal(symbols, terminals):
    i = len(symbols) - 1
    while i >= 0:
        if symbols[i] in terminals:
            return symbols[i]
        i -= 1
    return None

class GrammarError(YaccError):
    pass

class Grammar(object):
    def __init__(self, terminals):
        self.Productions  = [None]  
                                    

        self.Prodnames    = {}      
                                  

        self.Prodmap      = {}      
                                   

        self.Terminals    = {}      
                                    

        for term in terminals:
            self.Terminals[term] = []

        self.Terminals['error'] = []

        self.Nonterminals = {}      
                                    

        self.First        = {}      

        self.Follow       = {}      

        self.Precedence   = {}      
                                    

        self.UsedPrecedence = set() 
                                    
                                    

        self.Start = None           


    def __len__(self):
        return len(self.Productions)

    def __getitem__(self, index):
        return self.Productions[index]

    def set_precedence(self, term, assoc, level):
        assert self.Productions == [None], 'Must call set_precedence() before add_production()'
        if term in self.Precedence:
            raise GrammarError(f'Precedence already specified for terminal {term!r}')
        if assoc not in ['left', 'right', 'nonassoc']:
            raise GrammarError(f"Associativity of {term!r} must be one of 'left','right', or 'nonassoc'")
        self.Precedence[term] = (assoc, level)

    def add_production(self, prodname, syms, func=None, file='', line=0):

        if prodname in self.Terminals:
            raise GrammarError(f'{file}:{line}: Illegal rule name {prodname!r}. Already defined as a token')
        if prodname == 'error':
            raise GrammarError(f'{file}:{line}: Illegal rule name {prodname!r}. error is a reserved word')

        for n, s in enumerate(syms):
            if s[0] in "'\"" and s[0] == s[-1]:
                c = s[1:-1]
                if (len(c) != 1):
                    raise GrammarError(f'{file}:{line}: Literal token {s} in rule {prodname!r} may only be a single character')
                if c not in self.Terminals:
                    self.Terminals[c] = []
                syms[n] = c
                continue

        if '%prec' in syms:
            if syms[-1] == '%prec':
                raise GrammarError(f'{file}:{line}: Syntax error. Nothing follows %%prec')
            if syms[-2] != '%prec':
                raise GrammarError(f'{file}:{line}: Syntax error. %prec can only appear at the end of a grammar rule')
            precname = syms[-1]
            prodprec = self.Precedence.get(precname)
            if not prodprec:
                raise GrammarError(f'{file}:{line}: Nothing known about the precedence of {precname!r}')
            else:
                self.UsedPrecedence.add(precname)
            del syms[-2:]     
        else:
            precname = rightmost_terminal(syms, self.Terminals)
            prodprec = self.Precedence.get(precname, ('right', 0))

        map = '%s -> %s' % (prodname, syms)
        if map in self.Prodmap:
            m = self.Prodmap[map]
            raise GrammarError(f'{file}:{line}: Duplicate rule {m}. ' +
                               f'Previous definition at {m.file}:{m.line}')

        pnumber  = len(self.Productions)
        if prodname not in self.Nonterminals:
            self.Nonterminals[prodname] = []

        for t in syms:
            if t in self.Terminals:
                self.Terminals[t].append(pnumber)
            else:
                if t not in self.Nonterminals:
                    self.Nonterminals[t] = []
                self.Nonterminals[t].append(pnumber)

        p = Production(pnumber, prodname, syms, prodprec, func, file, line)
        self.Productions.append(p)
        self.Prodmap[map] = p

        try:
            self.Prodnames[prodname].append(p)
        except KeyError:
            self.Prodnames[prodname] = [p]

    def set_start(self, start=None):
        if callable(start):
            start = start.__name__

        if not start:
            start = self.Productions[1].name

        if start not in self.Nonterminals:
            raise GrammarError(f'start symbol {start} undefined')
        self.Productions[0] = Production(0, "S'", [start])
        self.Nonterminals[start].append(0)
        self.Start = start


    def find_unreachable(self):

        def mark_reachable_from(s):
            if s in reachable:
                return
            reachable.add(s)
            for p in self.Prodnames.get(s, []):
                for r in p.prod:
                    mark_reachable_from(r)

        reachable = set()
        mark_reachable_from(self.Productions[0].prod[0])
        return [s for s in self.Nonterminals if s not in reachable]


    def infinite_cycles(self):
        terminates = {}

        for t in self.Terminals:
            terminates[t] = True

        terminates['$end'] = True


        for n in self.Nonterminals:
            terminates[n] = False

        while True:
            some_change = False
            for (n, pl) in self.Prodnames.items():
                for p in pl:
                    for s in p.prod:
                        if not terminates[s]:
                            p_terminates = False
                            break
                    else:
                        p_terminates = True

                    if p_terminates:
                        if not terminates[n]:
                            terminates[n] = True
                            some_change = True
                        break

            if not some_change:
                break

        infinite = []
        for (s, term) in terminates.items():
            if not term:
                if s not in self.Prodnames and s not in self.Terminals and s != 'error':
                    pass
                else:
                    infinite.append(s)

        return infinite

    def undefined_symbols(self):
        result = []
        for p in self.Productions:
            if not p:
                continue

            for s in p.prod:
                if s not in self.Prodnames and s not in self.Terminals and s != 'error':
                    result.append((s, p))
        return result

    def unused_terminals(self):
        unused_tok = []
        for s, v in self.Terminals.items():
            if s != 'error' and not v:
                unused_tok.append(s)

        return unused_tok

    def unused_rules(self):
        unused_prod = []
        for s, v in self.Nonterminals.items():
            if not v:
                p = self.Prodnames[s][0]
                unused_prod.append(p)
        return unused_prod

    def unused_precedence(self):
        unused = []
        for termname in self.Precedence:
            if not (termname in self.Terminals or termname in self.UsedPrecedence):
                unused.append((termname, self.Precedence[termname][0]))

        return unused

    def _first(self, beta):

        result = []
        for x in beta:
            x_produces_empty = False

            for f in self.First[x]:
                if f == '<empty>':
                    x_produces_empty = True
                else:
                    if f not in result:
                        result.append(f)

            if x_produces_empty:
                pass
            else:
                break
        else:
            result.append('<empty>')

        return result

    def compute_first(self):
        if self.First:
            return self.First

        for t in self.Terminals:
            self.First[t] = [t]

        self.First['$end'] = ['$end']


        for n in self.Nonterminals:
            self.First[n] = []

        while True:
            some_change = False
            for n in self.Nonterminals:
                for p in self.Prodnames[n]:
                    for f in self._first(p.prod):
                        if f not in self.First[n]:
                            self.First[n].append(f)
                            some_change = True
            if not some_change:
                break

        return self.First

    def compute_follow(self, start=None):
        if self.Follow:
            return self.Follow

        if not self.First:
            self.compute_first()

        for k in self.Nonterminals:
            self.Follow[k] = []

        if not start:
            start = self.Productions[1].name

        self.Follow[start] = ['$end']

        while True:
            didadd = False
            for p in self.Productions[1:]:
                for i, B in enumerate(p.prod):
                    if B in self.Nonterminals:
                        fst = self._first(p.prod[i+1:])
                        hasempty = False
                        for f in fst:
                            if f != '<empty>' and f not in self.Follow[B]:
                                self.Follow[B].append(f)
                                didadd = True
                            if f == '<empty>':
                                hasempty = True
                        if hasempty or i == (len(p.prod)-1):
                            for f in self.Follow[p.name]:
                                if f not in self.Follow[B]:
                                    self.Follow[B].append(f)
                                    didadd = True
            if not didadd:
                break
        return self.Follow


    def build_lritems(self):
        for p in self.Productions:
            lastlri = p
            i = 0
            lr_items = []
            while True:
                if i > len(p):
                    lri = None
                else:
                    lri = LRItem(p, i)
                    try:
                        lri.lr_after = self.Prodnames[lri.prod[i+1]]
                    except (IndexError, KeyError):
                        lri.lr_after = []
                    try:
                        lri.lr_before = lri.prod[i-1]
                    except IndexError:
                        lri.lr_before = None

                lastlri.lr_next = lri
                if not lri:
                    break
                lr_items.append(lri)
                lastlri = lri
                i += 1
            p.lr_items = lr_items

    def __str__(self):
        out = []
        out.append('Grammar:\n')
        for n, p in enumerate(self.Productions):
            out.append(f'Rule {n:<5d} {p}')
        
        unused_terminals = self.unused_terminals()
        if unused_terminals:
            out.append('\nUnused terminals:\n')
            for term in unused_terminals:
                out.append(f'    {term}')

        out.append('\nTerminals, with rules where they appear:\n')
        for term in sorted(self.Terminals):
            out.append('%-20s : %s' % (term, ' '.join(str(s) for s in self.Terminals[term])))

        out.append('\nNonterminals, with rules where they appear:\n')
        for nonterm in sorted(self.Nonterminals):
            out.append('%-20s : %s' % (nonterm, ' '.join(str(s) for s in self.Nonterminals[nonterm])))

        out.append('')
        return '\n'.join(out)


def digraph(X, R, FP):
    N = {}
    for x in X:
        N[x] = 0
    stack = []
    F = {}
    for x in X:
        if N[x] == 0:
            traverse(x, N, stack, F, X, R, FP)
    return F

def traverse(x, N, stack, F, X, R, FP):
    stack.append(x)
    d = len(stack)
    N[x] = d
    F[x] = FP(x)             

    rel = R(x)               
    for y in rel:
        if N[y] == 0:
            traverse(y, N, stack, F, X, R, FP)
        N[x] = min(N[x], N[y])
        for a in F.get(y, []):
            if a not in F[x]:
                F[x].append(a)
    if N[x] == d:
        N[stack[-1]] = MAXINT
        F[stack[-1]] = F[x]
        element = stack.pop()
        while element != x:
            N[stack[-1]] = MAXINT
            F[stack[-1]] = F[x]
            element = stack.pop()

class LALRError(YaccError):
    pass


class LRTable(object):
    def __init__(self, grammar):
        self.grammar = grammar

        self.lr_action     = {}        
        self.lr_goto       = {}        
        self.lr_productions  = grammar.Productions    
        self.lr_goto_cache = {}        
        self.lr0_cidhash   = {}        
        self._add_count    = 0         

        self.state_descriptions = OrderedDict()
        self.sr_conflict   = 0
        self.rr_conflict   = 0
        self.conflicts     = []

        self.sr_conflicts  = []
        self.rr_conflicts  = []

        self.grammar.build_lritems()
        self.grammar.compute_first()
        self.grammar.compute_follow()
        self.lr_parse_table()

        self.defaulted_states = {}
        for state, actions in self.lr_action.items():
            rules = list(actions.values())
            if len(rules) == 1 and rules[0] < 0:
                self.defaulted_states[state] = rules[0]

    def lr0_closure(self, I):
        self._add_count += 1

        J = I[:]
        didadd = True
        while didadd:
            didadd = False
            for j in J:
                for x in j.lr_after:
                    if getattr(x, 'lr0_added', 0) == self._add_count:
                        continue
                    J.append(x.lr_next)
                    x.lr0_added = self._add_count
                    didadd = True

        return J

    def lr0_goto(self, I, x):
        g = self.lr_goto_cache.get((id(I), x))
        if g:
            return g



        s = self.lr_goto_cache.get(x)
        if not s:
            s = {}
            self.lr_goto_cache[x] = s

        gs = []
        for p in I:
            n = p.lr_next
            if n and n.lr_before == x:
                s1 = s.get(id(n))
                if not s1:
                    s1 = {}
                    s[id(n)] = s1
                gs.append(n)
                s = s1
        g = s.get('$end')
        if not g:
            if gs:
                g = self.lr0_closure(gs)
                s['$end'] = g
            else:
                s['$end'] = gs
        self.lr_goto_cache[(id(I), x)] = g
        return g

    def lr0_items(self):
        C = [self.lr0_closure([self.grammar.Productions[0].lr_next])]
        i = 0
        for I in C:
            self.lr0_cidhash[id(I)] = i
            i += 1

        i = 0
        while i < len(C):
            I = C[i]
            i += 1

            asyms = {}
            for ii in I:
                for s in ii.usyms:
                    asyms[s] = None

            for x in asyms:
                g = self.lr0_goto(I, x)
                if not g or id(g) in self.lr0_cidhash:
                    continue
                self.lr0_cidhash[id(g)] = len(C)
                C.append(g)

        return C

    def compute_nullable_nonterminals(self):
        nullable = set()
        num_nullable = 0
        while True:
            for p in self.grammar.Productions[1:]:
                if p.len == 0:
                    nullable.add(p.name)
                    continue
                for t in p.prod:
                    if t not in nullable:
                        break
                else:
                    nullable.add(p.name)
            if len(nullable) == num_nullable:
                break
            num_nullable = len(nullable)
        return nullable

    def find_nonterminal_transitions(self, C):
        trans = []
        for stateno, state in enumerate(C):
            for p in state:
                if p.lr_index < p.len - 1:
                    t = (stateno, p.prod[p.lr_index+1])
                    if t[1] in self.grammar.Nonterminals:
                        if t not in trans:
                            trans.append(t)
        return trans

    def dr_relation(self, C, trans, nullable):
        dr_set = {}
        state, N = trans
        terms = []

        g = self.lr0_goto(C[state], N)
        for p in g:
            if p.lr_index < p.len - 1:
                a = p.prod[p.lr_index+1]
                if a in self.grammar.Terminals:
                    if a not in terms:
                        terms.append(a)

        if state == 0 and N == self.grammar.Productions[0].prod[0]:
            terms.append('$end')

        return terms

    def reads_relation(self, C, trans, empty):
        rel = []
        state, N = trans

        g = self.lr0_goto(C[state], N)
        j = self.lr0_cidhash.get(id(g), -1)
        for p in g:
            if p.lr_index < p.len - 1:
                a = p.prod[p.lr_index + 1]
                if a in empty:
                    rel.append((j, a))

        return rel

    def compute_lookback_includes(self, C, trans, nullable):
        lookdict = {}          
        includedict = {}       

        dtrans = {}
        for t in trans:
            dtrans[t] = 1

        for state, N in trans:
            lookb = []
            includes = []
            for p in C[state]:
                if p.name != N:
                    continue


                lr_index = p.lr_index
                j = state
                while lr_index < p.len - 1:
                    lr_index = lr_index + 1
                    t = p.prod[lr_index]

                    if (j, t) in dtrans:


                        li = lr_index + 1
                        while li < p.len:
                            if p.prod[li] in self.grammar.Terminals:
                                break
                            if p.prod[li] not in nullable:
                                break
                            li = li + 1
                        else:
                            includes.append((j, t))

                    g = self.lr0_goto(C[j], t)
                    j = self.lr0_cidhash.get(id(g), -1)

                for r in C[j]:
                    if r.name != p.name:
                        continue
                    if r.len != p.len:
                        continue
                    i = 0
                    while i < r.lr_index:
                        if r.prod[i] != p.prod[i+1]:
                            break
                        i = i + 1
                    else:
                        lookb.append((j, r))
            for i in includes:
                if i not in includedict:
                    includedict[i] = []
                includedict[i].append((state, N))
            lookdict[(state, N)] = lookb

        return lookdict, includedict

    def compute_read_sets(self, C, ntrans, nullable):
        FP = lambda x: self.dr_relation(C, x, nullable)
        R =  lambda x: self.reads_relation(C, x, nullable)
        F = digraph(ntrans, R, FP)
        return F

    def compute_follow_sets(self, ntrans, readsets, inclsets):
        FP = lambda x: readsets[x]
        R  = lambda x: inclsets.get(x, [])
        F = digraph(ntrans, R, FP)
        return F

    def add_lookaheads(self, lookbacks, followset):
        for trans, lb in lookbacks.items():
            for state, p in lb:
                if state not in p.lookaheads:
                    p.lookaheads[state] = []
                f = followset.get(trans, [])
                for a in f:
                    if a not in p.lookaheads[state]:
                        p.lookaheads[state].append(a)

    def add_lalr_lookaheads(self, C):
        nullable = self.compute_nullable_nonterminals()

        trans = self.find_nonterminal_transitions(C)

        readsets = self.compute_read_sets(C, trans, nullable)

        lookd, included = self.compute_lookback_includes(C, trans, nullable)

        followsets = self.compute_follow_sets(trans, readsets, included)

        self.add_lookaheads(lookd, followsets)

    def lr_parse_table(self):
        Productions = self.grammar.Productions
        Precedence  = self.grammar.Precedence
        goto   = self.lr_goto         
        action = self.lr_action       

        actionp = {}                  


        C = self.lr0_items()
        self.add_lalr_lookaheads(C)

        for st, I in enumerate(C):
            descrip = []
            actlist = []              
            st_action  = {}
            st_actionp = {}
            st_goto    = {}

            descrip.append(f'\nstate {st}\n')
            for p in I:
                descrip.append(f'    ({p.number}) {p}')

            for p in I:
                    if p.len == p.lr_index + 1:
                        if p.name == "S'":
                            st_action['$end'] = 0
                            st_actionp['$end'] = p
                        else:
                            laheads = p.lookaheads[st]
                            for a in laheads:
                                actlist.append((a, p, f'reduce using rule {p.number} ({p})'))
                                r = st_action.get(a)
                                if r is not None:
                                    if r > 0:

                                        sprec, slevel = Precedence.get(a, ('right', 0))

                                        rprec, rlevel = Productions[p.number].prec

                                        if (slevel < rlevel) or ((slevel == rlevel) and (rprec == 'left')):
                                            st_action[a] = -p.number
                                            st_actionp[a] = p
                                            if not slevel and not rlevel:
                                                descrip.append(f'  ! shift/reduce conflict for {a} resolved as reduce')
                                                self.sr_conflicts.append((st, a, 'reduce'))
                                            Productions[p.number].reduced += 1
                                        elif (slevel == rlevel) and (rprec == 'nonassoc'):
                                            st_action[a] = None
                                        else:
                                            if not rlevel:
                                                descrip.append(f'  ! shift/reduce conflict for {a} resolved as shift')
                                                self.sr_conflicts.append((st, a, 'shift'))
                                    elif r <= 0:
                                        oldp = Productions[-r]
                                        pp = Productions[p.number]
                                        if oldp.line > pp.line:
                                            st_action[a] = -p.number
                                            st_actionp[a] = p
                                            chosenp, rejectp = pp, oldp
                                            Productions[p.number].reduced += 1
                                            Productions[oldp.number].reduced -= 1
                                        else:
                                            chosenp, rejectp = oldp, pp
                                        self.rr_conflicts.append((st, chosenp, rejectp))
                                        descrip.append('  ! reduce/reduce conflict for %s resolved using rule %d (%s)' % 
                                                       (a, st_actionp[a].number, st_actionp[a]))
                                    else:
                                        raise LALRError(f'Unknown conflict in state {st}')
                                else:
                                    st_action[a] = -p.number
                                    st_actionp[a] = p
                                    Productions[p.number].reduced += 1
                    else:
                        i = p.lr_index
                        a = p.prod[i+1]      
                        if a in self.grammar.Terminals:
                            g = self.lr0_goto(I, a)
                            j = self.lr0_cidhash.get(id(g), -1)
                            if j >= 0:
                                actlist.append((a, p, f'shift and go to state {j}'))
                                r = st_action.get(a)
                                if r is not None:
                                    if r > 0:
                                        if r != j:
                                            raise LALRError(f'Shift/shift conflict in state {st}')
                                    elif r <= 0:
                                        rprec, rlevel = Productions[st_actionp[a].number].prec
                                        sprec, slevel = Precedence.get(a, ('right', 0))
                                        if (slevel > rlevel) or ((slevel == rlevel) and (rprec == 'right')):
                                            Productions[st_actionp[a].number].reduced -= 1
                                            st_action[a] = j
                                            st_actionp[a] = p
                                            if not rlevel:
                                                descrip.append(f'  ! shift/reduce conflict for {a} resolved as shift')
                                                self.sr_conflicts.append((st, a, 'shift'))
                                        elif (slevel == rlevel) and (rprec == 'nonassoc'):
                                            st_action[a] = None
                                        else:
                                            if not slevel and not rlevel:
                                                descrip.append(f'  ! shift/reduce conflict for {a} resolved as reduce')
                                                self.sr_conflicts.append((st, a, 'reduce'))

                                    else:
                                        raise LALRError(f'Unknown conflict in state {st}')
                                else:
                                    st_action[a] = j
                                    st_actionp[a] = p

            _actprint = {}
            for a, p, m in actlist:
                if a in st_action:
                    if p is st_actionp[a]:
                        descrip.append(f'    {a:<15s} {m}')
                        _actprint[(a, m)] = 1
            descrip.append('')

            nkeys = {}
            for ii in I:
                for s in ii.usyms:
                    if s in self.grammar.Nonterminals:
                        nkeys[s] = None
            for n in nkeys:
                g = self.lr0_goto(I, n)
                j = self.lr0_cidhash.get(id(g), -1)
                if j >= 0:
                    st_goto[n] = j
                    descrip.append(f'    {n:<30s} shift and go to state {j}')

            action[st] = st_action
            actionp[st] = st_actionp
            goto[st] = st_goto
            self.state_descriptions[st] = '\n'.join(descrip)

    def __str__(self):
        out = []
        for descrip in self.state_descriptions.values():
            out.append(descrip)
            
        if self.sr_conflicts or self.rr_conflicts:
            out.append('\nConflicts:\n')

            for state, tok, resolution in self.sr_conflicts:
                out.append(f'shift/reduce conflict for {tok} in state {state} resolved as {resolution}')

            already_reported = set()
            for state, rule, rejected in self.rr_conflicts:
                if (state, id(rule), id(rejected)) in already_reported:
                    continue
                out.append(f'reduce/reduce conflict in state {state} resolved using rule {rule}')
                out.append(f'rejected rule ({rejected}) in state {state}')
                already_reported.add((state, id(rule), id(rejected)))

            warned_never = set()
            for state, rule, rejected in self.rr_conflicts:
                if not rejected.reduced and (rejected not in warned_never):
                    out.append(f'Rule ({rejected}) is never reduced')
                    warned_never.add(rejected)

        return '\n'.join(out)

def _collect_grammar_rules(func):
    grammar = []
    while func:
        prodname = func.__name__
        unwrapped = inspect.unwrap(func)
        filename = unwrapped.__code__.co_filename
        lineno = unwrapped.__code__.co_firstlineno
        for rule, lineno in zip(func.rules, range(lineno+len(func.rules)-1, 0, -1)):
            syms = rule.split()
            ebnf_prod = []
            while ('{' in syms) or ('[' in syms):
                for s in syms:
                    if s == '[':
                        syms, prod = _replace_ebnf_optional(syms)
                        ebnf_prod.extend(prod)
                        break
                    elif s == '{':
                        syms, prod = _replace_ebnf_repeat(syms)
                        ebnf_prod.extend(prod)
                        break

            if syms[1:2] == [':'] or syms[1:2] == ['::=']:
                grammar.append((func, filename, lineno, syms[0], syms[2:]))
            else:
                grammar.append((func, filename, lineno, prodname, syms))
            grammar.extend(ebnf_prod)
            
        func = getattr(func, 'next_func', None)

    return grammar

def _replace_ebnf_repeat(syms):
    syms = list(syms)
    first = syms.index('{')
    end = syms.index('}', first)
    symname, prods = _generate_repeat_rules(syms[first+1:end])
    syms[first:end+1] = [symname]
    return syms, prods

def _replace_ebnf_optional(syms):
    syms = list(syms)
    first = syms.index('[')
    end = syms.index(']', first)
    symname, prods = _generate_optional_rules(syms[first+1:end])
    syms[first:end+1] = [symname]
    return syms, prods
                
_gencount = 0

def _unique_names(names):
    from collections import defaultdict, Counter
    counts = Counter(names)
    indices = defaultdict(int)
    newnames = []
    for name in names:
        if counts[name] == 1:
            newnames.append(name)
        else:
            newnames.append(f'{name}{indices[name]}')
            indices[name] += 1
    return newnames


_name_aliases = { }

def _generate_repeat_rules(symbols):
    global _gencount
    _gencount += 1
    name = f'_{_gencount}_repeat'
    oname = f'_{_gencount}_items'
    iname = f'_{_gencount}_item'
    symtext = ' '.join(symbols)

    _name_aliases[name] = symbols

    productions = [ ]
    _ = _decorator

    @_(f'{name} : {oname}')
    def repeat(self, p):
        return getattr(p, oname)

    @_(f'{name} : ')
    def repeat2(self, p):
        return []
    productions.extend(_collect_grammar_rules(repeat))
    productions.extend(_collect_grammar_rules(repeat2))

    @_(f'{oname} : {oname} {iname}')
    def many(self, p):
        items = getattr(p, oname)
        items.append(getattr(p, iname))
        return items

    @_(f'{oname} : {iname}')
    def many2(self, p):
        return [ getattr(p, iname) ]

    productions.extend(_collect_grammar_rules(many))
    productions.extend(_collect_grammar_rules(many2))

    @_(f'{iname} : {symtext}')
    def item(self, p):
        return tuple(p)

    productions.extend(_collect_grammar_rules(item))
    return name, productions

def _generate_optional_rules(symbols):
    global _gencount
    _gencount += 1
    name = f'_{_gencount}_optional'
    symtext = ' '.join(symbols)
    
    _name_aliases[name] = symbols

    productions = [ ]
    _ = _decorator

    no_values = (None,) * len(symbols)

    @_(f'{name} : {symtext}')
    def optional(self, p):
        return tuple(p)

    @_(f'{name} : ')
    def optional2(self, p):
        return no_values

    productions.extend(_collect_grammar_rules(optional))
    productions.extend(_collect_grammar_rules(optional2))
    return name, productions
    
class ParserMetaDict(dict):
    def __setitem__(self, key, value):
        if key in self and callable(value) and hasattr(value, 'rules'):
            value.next_func = self[key]
            if not hasattr(value.next_func, 'rules'):
                raise GrammarError(f'Redefinition of {key}. Perhaps an earlier {key} is missing @_')
        super().__setitem__(key, value)
    
    def __getitem__(self, key):
        if key not in self and key.isupper() and key[:1] != '_':
            return key.upper()
        else:
            return super().__getitem__(key)

def _decorator(rule, *extra):
     rules = [rule, *extra]
     def decorate(func):
         func.rules = [ *getattr(func, 'rules', []), *rules[::-1] ]
         return func
     return decorate

class ParserMeta(type):
    @classmethod
    def __prepare__(meta, *args, **kwargs):
        d = ParserMetaDict()
        d['_'] = _decorator
        return d

    def __new__(meta, clsname, bases, attributes):
        del attributes['_']
        cls = super().__new__(meta, clsname, bases, attributes)
        cls._build(list(attributes.items()))
        return cls

class Parser(metaclass=ParserMeta):
    log = SlyLogger(sys.stderr)     

    debugfile = None

    @classmethod
    def __validate_tokens(cls):
        if not hasattr(cls, 'tokens'):
            cls.log.error('No token list is defined')
            return False

        if not cls.tokens:
            cls.log.error('tokens is empty')
            return False

        if 'error' in cls.tokens:
            cls.log.error("Illegal token name 'error'. Is a reserved word")
            return False

        return True

    @classmethod
    def __validate_precedence(cls):
        if not hasattr(cls, 'precedence'):
            cls.__preclist = []
            return True

        preclist = []
        if not isinstance(cls.precedence, (list, tuple)):
            cls.log.error('precedence must be a list or tuple')
            return False

        for level, p in enumerate(cls.precedence, start=1):
            if not isinstance(p, (list, tuple)):
                cls.log.error(f'Bad precedence table entry {p!r}. Must be a list or tuple')
                return False

            if len(p) < 2:
                cls.log.error(f'Malformed precedence entry {p!r}. Must be (assoc, term, ..., term)')
                return False

            if not all(isinstance(term, str) for term in p):
                cls.log.error('precedence items must be strings')
                return False
            
            assoc = p[0]
            preclist.extend((term, assoc, level) for term in p[1:])

        cls.__preclist = preclist
        return True

    @classmethod
    def __validate_specification(cls):
        if not cls.__validate_tokens():
            return False
        if not cls.__validate_precedence():
            return False
        return True

    @classmethod
    def __build_grammar(cls, rules):
        grammar_rules = []
        errors = ''
        if not rules:
            raise YaccError('No grammar rules are defined')

        grammar = Grammar(cls.tokens)

        for term, assoc, level in cls.__preclist:
            try:
                grammar.set_precedence(term, assoc, level)
            except GrammarError as e:
                errors += f'{e}\n'

        for name, func in rules:
            try:
                parsed_rule = _collect_grammar_rules(func)
                for pfunc, rulefile, ruleline, prodname, syms in parsed_rule:
                    try:
                        grammar.add_production(prodname, syms, pfunc, rulefile, ruleline)
                    except GrammarError as e:
                        errors += f'{e}\n'
            except SyntaxError as e:
                errors += f'{e}\n'
        try:
            grammar.set_start(getattr(cls, 'start', None))
        except GrammarError as e:
            errors += f'{e}\n'

        undefined_symbols = grammar.undefined_symbols()
        for sym, prod in undefined_symbols:
            errors += '%s:%d: Symbol %r used, but not defined as a token or a rule\n' % (prod.file, prod.line, sym)

        unused_terminals = grammar.unused_terminals()
        if unused_terminals:
            unused_str = '{' + ','.join(unused_terminals) + '}'
            cls.log.warning(f'Token{"(s)" if len(unused_terminals) >1 else ""} {unused_str} defined, but not used')

        unused_rules = grammar.unused_rules()
        for prod in unused_rules:
            cls.log.warning('%s:%d: Rule %r defined, but not used', prod.file, prod.line, prod.name)

        if len(unused_terminals) == 1:
            cls.log.warning('There is 1 unused token')
        if len(unused_terminals) > 1:
            cls.log.warning('There are %d unused tokens', len(unused_terminals))

        if len(unused_rules) == 1:
            cls.log.warning('There is 1 unused rule')
        if len(unused_rules) > 1:
            cls.log.warning('There are %d unused rules', len(unused_rules))

        unreachable = grammar.find_unreachable()
        for u in unreachable:
           cls.log.warning('Symbol %r is unreachable', u)

        if len(undefined_symbols) == 0:
            infinite = grammar.infinite_cycles()
            for inf in infinite:
                errors += 'Infinite recursion detected for symbol %r\n' % inf

        unused_prec = grammar.unused_precedence()
        for term, assoc in unused_prec:
            errors += 'Precedence rule %r defined for unknown symbol %r\n' % (assoc, term)

        cls._grammar = grammar
        if errors:
            raise YaccError('Unable to build grammar.\n'+errors)

    @classmethod
    def __build_lrtables(cls):
        lrtable = LRTable(cls._grammar)
        num_sr = len(lrtable.sr_conflicts)

        if num_sr != getattr(cls, 'expected_shift_reduce', None):
            if num_sr == 1:
                cls.log.warning('1 shift/reduce conflict')
            elif num_sr > 1:
                cls.log.warning('%d shift/reduce conflicts', num_sr)

        num_rr = len(lrtable.rr_conflicts)
        if num_rr != getattr(cls, 'expected_reduce_reduce', None):
            if num_rr == 1:
                cls.log.warning('1 reduce/reduce conflict')
            elif num_rr > 1:
                cls.log.warning('%d reduce/reduce conflicts', num_rr)

        cls._lrtable = lrtable
        return True

    @classmethod
    def __collect_rules(cls, definitions):
        rules = [ (name, value) for name, value in definitions
                  if callable(value) and hasattr(value, 'rules') ]
        return rules

    @classmethod
    def _build(cls, definitions):
        if vars(cls).get('_build', False):
            return

        rules = cls.__collect_rules(definitions)

        if not cls.__validate_specification():
            raise YaccError('Invalid parser specification')

        cls.__build_grammar(rules)

        if not cls.__build_lrtables():
            raise YaccError('Can\'t build parsing tables')

        if cls.debugfile:
            with open(cls.debugfile, 'w') as f:
                f.write(str(cls._grammar))
                f.write('\n')
                f.write(str(cls._lrtable))
            cls.log.info('Parser debugging for %s written to %s', cls.__qualname__, cls.debugfile)

    def error(self, token):
        colorama.init()
        if token:
            lineno = getattr(token, 'lineno', 0)
            if lineno:
                sys.stderr.write(colorama.Fore.RED+"Error : ")
                sys.stderr.write(colorama.Style.RESET_ALL)
                sys.stderr.write(f'Syntax error at line {lineno}, token={token.type}, value={token.value}\n')
            else:
                sys.stderr.write(colorama.Fore.RED+"Error : ")
                sys.stderr.write(colorama.Style.RESET_ALL)
                sys.stderr.write(f'Error  : Syntax error, token={token.type}')
        else:
            sys.stderr.write(colorama.Fore.RED+"Error : ")
            sys.stderr.write(colorama.Style.RESET_ALL)
            sys.stderr.write('Error : Parse error in input. EOF\n')
 
    def errok(self):
        self.errorok = True

    def restart(self):
        del self.statestack[:]
        del self.symstack[:]
        sym = YaccSymbol()
        sym.type = '$end'
        self.symstack.append(sym)
        self.statestack.append(0)
        self.state = 0

    def parse(self, tokens):
        lookahead = None                                  
        lookaheadstack = []                               
        actions = self._lrtable.lr_action                 
        goto    = self._lrtable.lr_goto                   
        prod    = self._grammar.Productions               
        defaulted_states = self._lrtable.defaulted_states 
        pslice  = YaccProduction(None)                    
        errorcount = 0                                    

        self.tokens = tokens
        self.statestack = statestack = []                 
        self.symstack = symstack = []                     
        pslice._stack = symstack                           
        self.restart()

        errtoken   = None                                 
        while True:
            if self.state not in defaulted_states:
                if not lookahead:
                    if not lookaheadstack:
                        lookahead = next(tokens, None)  
                    else:
                        lookahead = lookaheadstack.pop()
                    if not lookahead:
                        lookahead = YaccSymbol()
                        lookahead.type = '$end'

                ltype = lookahead.type
                t = actions[self.state].get(ltype)
            else:
                t = defaulted_states[self.state]

            if t is not None:
                if t > 0:
                    statestack.append(t)
                    self.state = t

                    symstack.append(lookahead)
                    lookahead = None

                    if errorcount:
                        errorcount -= 1
                    continue

                if t < 0:
                    self.production = p = prod[-t]
                    pname = p.name
                    plen  = p.len
                    pslice._namemap = p.namemap

                    pslice._slice = symstack[-plen:] if plen else []

                    sym = YaccSymbol()
                    sym.type = pname       
                    value = p.func(self, pslice)
                    if value is pslice:
                        value = (pname, *(s.value for s in pslice._slice))
                    sym.value = value
                    if plen:
                        del symstack[-plen:]
                        del statestack[-plen:]

                    symstack.append(sym)
                    self.state = goto[statestack[-1]][pname]
                    statestack.append(self.state)
                    continue

                if t == 0:
                    n = symstack[-1]
                    result = getattr(n, 'value', None)
                    return result

            if t is None:
                if errorcount == 0 or self.errorok:
                    errorcount = ERROR_COUNT
                    self.errorok = False
                    if lookahead.type == '$end':
                        errtoken = None               
                    else:
                        errtoken = lookahead

                    tok = self.error(errtoken)
                    if tok:
                        lookahead = tok
                        self.errorok = True
                        continue
                    else:
                        if not errtoken:
                            return
                else:
                    errorcount = ERROR_COUNT

                if len(statestack) <= 1 and lookahead.type != '$end':
                    lookahead = None
                    self.state = 0
                    del lookaheadstack[:]
                    continue

                if lookahead.type == '$end':
                    return

                if lookahead.type != 'error':
                    sym = symstack[-1]
                    if sym.type == 'error':
                        lookahead = None
                        continue

                    t = YaccSymbol()
                    t.type = 'error'

                    if hasattr(lookahead, 'lineno'):
                        t.lineno = lookahead.lineno
                    if hasattr(lookahead, 'index'):
                        t.index = lookahead.index
                    t.value = lookahead
                    lookaheadstack.append(lookahead)
                    lookahead = t
                else:
                    sym = symstack.pop()
                    statestack.pop()
                    self.state = statestack[-1]
                continue
            raise RuntimeError('Error : internal parser error!!!\n')
