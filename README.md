Master branch contains the raw sqlite bnf generated from the sqlite [website](http://www.sqlite.org/docsrc/doc/trunk/art/syntax/all-bnf.html).
It is worth noting the sqlite website bnf is unmaintained and obselete. A more accurate bnf could be made by converting the
lemon grammar sqlite uses internally.

grammar-kit branch contains a modified version of the generated grammar which is compatible with [Grammar-Kit](http://github.com/JetBrains/Grammar-Kit)
