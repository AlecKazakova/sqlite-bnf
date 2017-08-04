import urllib2
import codecs
from bs4 import BeautifulSoup

meta_inf = open('tokens.txt', 'r').read()


def definition_for_table(table):
    result = ''
    options = table.find_all('tr')

    # Add the LHS of the definition.
    name = options[0].find_all('td')
    prefix = name[0].string + ' ::= '

    # Use the override rule
    if prefix in meta_inf:
        return

    result += prefix

    # Add the RHS of the definition
    if len(options) > 1:
        result += '( '
    for option_index, option in enumerate(options):
        if option_index != 0:
            result += '\n' + (' ' * len(name[0].string + ' ::= ')) + '| '
        stack = []
        collapse_element(option.find_all('td')[2], stack)
        result += ' '.join(stack)
    if len(options) > 1:
        result += ' )'
    return result


def collapse_element(element, stack):
    if hasattr(element, 'children'):
        for child in element.children:
            collapse_element(child, stack)
        return

    # These are fragments in the sqlite bnf we dont want in our machine-readable bnf
    if element == '<' or element == '>':
        return

    if hasattr(element, 'a') and element.a is not None:
        child_string = element.a.string
    else:
        child_string = element.string
    for piece in child_string.split():
        if piece == ']*':
            stack.append(']')
            stack = switch_to_rounded_paren(stack)
            stack.append('*')
            continue
        if piece == '1' and stack[len(stack) - 1] == ']':
            # Required or repeated expressions use rounded braces.
            stack = switch_to_rounded_paren(stack)
            continue
        quoted = '\'' + piece + '\''
        if quoted in meta_inf:
            stack.append(quoted)
        else:
            stack.append(piece)


def switch_to_rounded_paren(stack):
    parens_observed = 0
    popped_items = []
    while len(stack) != 0:
        current_item = stack.pop()
        popped_items.append(current_item)
        if current_item == ']':
            parens_observed += 1
        if current_item == '[':
            parens_observed -= 1
        if parens_observed == 0:
            popped_items.pop()
            stack.append('(')
            while len(popped_items) != 1:
                stack.append(popped_items.pop())
            stack.append(')')
            return stack


response = urllib2.urlopen('http://www.sqlite.org/docsrc/doc/trunk/art/syntax/all-bnf.html')
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
output = codecs.open('sqlite.bnf', 'w', 'utf8')
for table_html in soup.body.find_all('table'):
    print >> output, definition_for_table(table_html)
output.close()
