"""
Copyright 2026 Joachim REY

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

class Testing :

    """
    Testing allow to create Python tests easily.

    It require testing function to be referenced with the
    @Testing.reference decorator.

    Then, Testing.test() can be used to do tests.

    Testing.display() display the results of all the tests.
    """

    # Variables
    _messages = { }
    _current_function_path = [ ]
    _total_tests = 0
    _failed_tests = 0

    # Parameters
    _display_results = True
    _catch_errors = True
    _display_starting_char = ''
    _display_color = True
    _display_style = 0

    # Constants
    _colors = [
            "\033[33m", # Yellow
            "\033[32m", # Green
            "\033[31m"  # Red
    ]
    _pipes = [
            [
                '\u2570',
                '\u2574',
                '\u251C',
                '\u2502'
            ],
            [
                '\u2514'
            ],
            [
                '\u255A',
                '\u2550',
                '\u2560',
                '\u2551'
            ],
            [
                '-',
                ' ',
                '-',
                '|'
            ]
    ]

    @staticmethod
    def setDisplayLiveResults( display : bool ) -> None :

        """
        Change to wether or not display result of each tests when Testing.test()
        is called.

        Default: True

        In :
            display, bool : True will display the result, False hide them.

        Out :
            None
        """

        Testing._display_results = display
        return None

    @staticmethod
    def setCatchErrors( catch : bool ) -> None :

        """
        Change to wether or not catch errors in referenced testing functions.
        Catched errors will be added in the _messages dictionnary

        Default: True

        In :
            catch, bool : True will catch errors, False will not.

        Out :
            None
        """

        Testing._catch_errors = catch
        return None

    @staticmethod
    def setDisplayStartingChar( char : str ) -> None :

        """
        Define the starting character(s) of the tree-view created when
        displayed with Testing.display().

        Default: ''

        In :
            char, str : The new starting character.

        Out :
            None
        """

        Testing._display_starting_char = char
        return None

    @staticmethod
    def setDisplayColors( display : bool ) -> None :

        """
        Change to wether or not display ANSI colors.

        Default: True

        In :
            display, bool : True will display color, False won't.

        Out :
            None
        """

        Testing._display_color = display
        return None

    @staticmethod
    def setDisplayStyle( display : int ) -> None :

        """
        Change the style of the tree-view.
        0 uses round pipes,
        1 uses square pipes,
        2 uses hollow pipes and
        3 uses ASCII.

        Default: True

        In :
            display, bool : True will display color, False won't.

        Out :
            None
        """

        if display < len( Testing._pipes ) :
            Testing._display_style = display
        return None

    @staticmethod
    def test( valid : bool, message : str ) -> bool :

        """
        Test a statement assert style. the statement is False, the
        test fail and is added to the messages dictionnary.

        In :
            valid, bool : Statement to be tested.
            message, str : Message if the test fail.
        Out :
            bool : Tested statement.
        """

        res = Testing._colorize( ".", 1 )
        if not valid :
            res = Testing._colorize( "F", 2 )
            Testing._addMessage( Testing._current_function_path,
                                Testing._messages, message )
            Testing._failed_tests += 1
        Testing._total_tests += 1
        if Testing._display_results :
            print( res, end="" )
        return valid

    @staticmethod
    def _colorize( text: str, color: int ) -> str :

        """
        Colorize the given text with the given color indice in the
        _colors list.
        If _display_color if False or the indice is wrong, it will
        return the base text.

        In :
            text, str : Text to colorize.
            color, int : Color indice in _colors.

        Out :
            str : Colorized text.
        """

        if ( not Testing._display_color ) or \
            color > len( Testing._colors ) or color < 0:
            return text
        return Testing._colors[ color ] + text + "\033[0m"

    @staticmethod
    def _get_pipe( indice : int ) -> chr :
        """
        Return the correct pipe given an indice. If the pipe does not
        exists in the current style, it will return the pipe in the
        default style. If the indice does not correspond to any pipe,
        it will return an empty char.

        In:
            indice, int : Indice of the pipe

        Out:
            chr: The resulting pipe
        """

        if indice >= len( Testing._pipes[ 0 ] ) :
            return ''
        if indice >= len( Testing._pipes[ Testing._display_style ] ):
            return Testing._pipes[ 0 ][ indice ]
        return Testing._pipes[ Testing._display_style ][ indice ]

    @staticmethod
    def _addHierarchy( hierarchy : list, tree : dict ) -> None :

        """
        Private function to add a function in the _messages hierarchy.

        In :
            hierarchy, list: Path to the function to add.
            tree, dict : The dictionnary where to function should be added.

        Out :
            None
        """

        if len( hierarchy ) == 1 :
            tree[ hierarchy[0] ] = [ ]
        else :
            if not hierarchy[0] in tree.keys() :
                tree[ hierarchy[0] ] = {}
            Testing._addHierarchy( hierarchy[1:], tree[ hierarchy[0] ] )
        return None

    @staticmethod
    def _addMessage( hierarchy : list, tree : dict, message : str ) -> None :

        """
        Private function to add a message in the _messages at the given hierarchy.

        In :
            hierarchy, list : Path to the _messages to add.
            tree, dict: The dictionnary where to _messages should be added.
            _messages, str : Message to add.

        Out :
            None
        """

        if len( hierarchy ) == 1 :
            tree[ hierarchy[0] ].append( message )
        else:
            if not hierarchy[0] in tree.keys() :
                raise Exception( "Testing used out of the context of a"
                                f"referenced function! ({ hierarchy })" )
            Testing._addMessage( hierarchy[1:], tree[hierarchy[0]], message )
        return None

    @staticmethod
    def _displayHierarchy( tree : dict, start : str ) -> str :

        """
        Private function to display the _messages dictionnary.

        In :
            tree, dict : The dictionnary where to function should be added.
            start, str : Characters to add before an entry.

        Out :
            str : The resulting text.
        """

        res = ""
        if isinstance( tree, list ) :
            last = len( tree ) - 1
            for i in range( 0, last + 1 ) :
                if ( i == last ):
                    res += Testing._colorize( f"{ start }{ Testing._get_pipe( 0 ) }{ Testing._get_pipe( 1 ) }", 0 )
                else:
                    res += Testing._colorize( f"{ start }{ Testing._get_pipe( 2 ) }{ Testing._get_pipe( 1 ) }", 0 )
                res += tree[i] + '\n'
            return res
        else :
            keys = list( tree.keys() )
            last = len( keys ) - 1
            start_c = Testing._get_pipe( 3 )
            for i in range( 0, last + 1 ) :
                if ( i == last ) :
                    res += Testing._colorize( f"{ start }{ Testing._get_pipe( 0 ) }{ Testing._get_pipe( 1 ) }", 0 )
                    start_c = ' '
                else :
                    res += Testing._colorize( f"{ start }{ Testing._get_pipe( 2 ) }{ Testing._get_pipe( 1 ) }", 0 )
                res += Testing._colorize( f"{ keys[i] }\n", 0 )
                res += Testing._displayHierarchy( tree[ keys[i] ], f"{ start }{ start_c } " )
            return res

    @staticmethod
    def reference(func : type) -> None :

        """
        Reference a function in the _messages dictionnary
        and execute it.

        In :
            func, type : Test function to reference.
        Out :
            None
        """

        def wrapper( *args, **kwargs ) :
            Testing._current_function_path = func.__qualname__.split( "." )
            Testing._addHierarchy( Testing._current_function_path, Testing._messages )
            if not Testing._catch_errors:
                return func( *args, **kwargs )
            try:
                return func( *args, **kwargs )
            except Exception as e:
                Testing._addMessage( Testing._current_function_path, Testing._messages,
                                    Testing._colorize( e.__str__(), 2 ) )
        return wrapper

    @staticmethod
    def display( ) -> None :

        """
        Display the result of all tests ran so far and their hierarchy.

        In :

        Out :
            None
        """

        print(
            Testing._colorize( f"\n{ Testing._total_tests - Testing._failed_tests } tests passed, ", 1 ) +
            Testing._colorize( f"{ Testing._failed_tests }  tests failed\n", 2 ) +
            Testing._displayHierarchy( Testing._messages, Testing._display_starting_char )
        )
        return None
