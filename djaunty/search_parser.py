import re

from django.db.models import Q

from ply import lex, yacc


class ParserException(Exception):
    pass


class SearchParser:
    attributes = [
        'keyword',
        'lab',
        'institution',
        'doi',
        'experimenter',
        'units',
        'electrodes'
    ]

    binary_operators = {
        r'=': 'EQUAL',
        r'!=': 'NOTEQUAL',
        r'\>=': 'GREATEREQUAL',
        r'\>': 'GREATER',
        r'\<=': 'LESSEQUAL',
        r'\<': 'LESS',
        r'in': 'IN',
        r'and': 'AND',
        r'or': 'OR'
    }

    literals = ['[', ']', '(', ')', ',']

    tokens = [
        # attributes
        'ATTRIBUTE',

        # values
        'STRING',
        'INTEGER',

        'NOT'
    ] + list(binary_operators.values())

    t_NOT = r'not'

    t_ignore_WHITESPACE = r'\s+'
    t_ignore_COMMENT = r'\#.*'

    # for the parser
    precedence = [
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NOT'),
        ('right', 'IN')
    ]

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, reflags=re.IGNORECASE)
        self.parser = yacc.yacc(module=self, write_tables=False, debug=False)

    def tokenize(self, text):
        self.lexer.input(text)
        while True:
            token = self.lexer.token()
            if not token:
                break
            print(token)

    def parse(self, text):
        return self.parser.parse(text, lexer=self.lexer)

    def t_STRING(self, t):
        r"""("[^"]*")|('[^']*')"""  # '...' or "..."
        t.value = t.value[1:-1]
        return t

    def t_INTEGER(self, t):
        r'-?\d+'
        t.value = int(t.value)
        return t

    @lex.TOKEN('(' + ')|('.join(binary_operators.keys()) + ')')
    def t_BINARYOP(self, t):
        value = t.value.replace('>', r'\>')
        value = value.replace('<', r'\<')
        t.type = self.binary_operators[value]
        return t

    @lex.TOKEN('(' + ')|('.join(attributes) + ')')
    def t_ATTRIBUTE(self, t):
        if t.value == 'doi':
            t.value = 'related_publications__doi'
        elif t.value == 'keyword':
            t.value = 'keywords__keyword'
        elif t.value == 'electrodes':
            t.value = 'number_of_electrodes'
        return t

    def t_error(self, t):
        raise ParserException(
            f'Error tokenizing "{t.value}" at line {t.lineno}, position {t.lexpos}'
        )

    # Parser rules

    def p_filter(self, p):
        'filter : expression'
        p[0] = p[1]

    def p_expression_rule(self, p):
        'expression : rule'
        p[0] = p[1]

    def p_expression_and(self, p):
        'expression : expression AND expression'
        # and filter
        p[0] = p[1] & p[3]

    def p_expression_or(self, p):
        'expression : expression OR expression'
        # or filter
        p[0] = p[1] | p[3]

    def p_expression_not(self, p):
        'expression : NOT expression'
        # not filter
        p[2].negate()
        p[0] = p[2]

    def p_expression_group(self, p):
        "expression : '(' expression ')'"
        p[0] = p[2]

    def p_rule_binary(self, p):
        '''rule : ATTRIBUTE EQUAL value
                | ATTRIBUTE NOTEQUAL value
                | ATTRIBUTE GREATEREQUAL INTEGER
                | ATTRIBUTE GREATER INTEGER
                | ATTRIBUTE LESSEQUAL INTEGER
                | ATTRIBUTE LESS INTEGER
        '''
        key = p[1]
        op = p[2]
        value = p[3]
        if op in ('=', '!=') and isinstance(value, str):
            key = key + '__iexact'
        elif op == '<':
            key = key + '__lt'
        elif op == '<=':
            key = key + '__lte'
        elif op == '>':
            key = key + '__gt'
        elif op == '>=':
            key = key + '__gte'

        kwargs = dict([(key, value)])
        q = Q(**kwargs)
        if op == '!=':
            q.negate()
        p[0] = q

    def p_rule_in(self, p):
        "rule : ATTRIBUTE IN '[' list ']'"
        key = p[1] + '__in'
        value = p[3]
        kwargs = dict([(key, value)])
        p[0] = Q(**kwargs)

    def p_list(self, p):
        '''list : list ',' value
                | value
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[3])

    def p_value(self, p):
        '''value : STRING
                 | INTEGER
        '''
        p[0] = p[1]

    def p_error(self, p):
        raise ParserException(
            f'parsing error: "{p.value}" at line {p.lineno}, position {p.lexpos}'
        )
