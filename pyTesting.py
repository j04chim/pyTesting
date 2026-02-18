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

    _messages = { }
    _current_function_path = [ ]
    _total_tests = 0
    _failed_tests = 0
    _display_results = True
    _catch_error = True

    def displayLiveResults( display : bool ) -> None :

        """
        Change to wether or not display result of each tests when Testing.test()
        is called.

        Default: True

        In :
            display, bool : True will display the result, False hide them

        Out :
            None
        """

        Testing._display_results = display
        return None

    def catchErrors( catch : bool ) -> None :

        """
        Change to wether or not catch errors in referenced testing functions.
        Catched errors will be added in the _messages dictionnary

        Default: True

        In :
            catch, bool : True will catch errors, False will not

        Out :
            None
        """

        Testing._catch_error = catch
        return None

    def test( valid : bool, message : str ) -> bool :

        """
        Test a statement assert style. the statement is False, the
        test fail and is added to the messages dictionnary.

        In :
            valid, bool : Statement to be tested.
            message, str : Message if the test fail.
        Out :
            bool : Tested statement
        """

        res = "2m." # Green + '.'
        if not valid :
            res = "1mF" # Red + 'F'
            Testing._addMessage( Testing._current_function_path, Testing._messages, message )
            Testing._failed_tests += 1
        Testing._total_tests += 1
        if Testing._display_results :
            print( f"\033[3{ res }\033[0m", end="" )
        return valid

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
                raise Exception( f"Testing used out of the context of a referenced function! ({ hierarchy })" )
            Testing._addMessage( hierarchy[1:], tree[hierarchy[0]], message )
        return None

    def _displayHierarchy( tree : dict, start : str ) -> str :

        """
        Private function to display the _messages dictionnary.

        In :
            tree, dict : The dictionnary where to function should be added.
            start, str : Characters to add before an entry.

        Out :
            str : The resulting text
        """

        res = ""
        if isinstance( tree, list ) :
            last = len( tree ) - 1
            for i in range( 0, last + 1 ) :
                if ( i == last ):
                    res += f"\033[33m{ start }\u2570\u2574\033[0m"
                else:
                    res += f"\033[33m{ start }\u251C\u2574\033[0m"
                res += tree[i] + '\n'
            return res
        else :
            keys = list( tree.keys() )
            last = len( keys ) - 1
            start_c = '\u2502'
            for i in range( 0, last + 1 ) :
                if ( i == last ) :
                    res += f"\033[33m{ start }\u2570\u2574\033[0m"
                    start_c = ' '
                else :
                    res += f"\033[33m{ start }\u251C\u2574\033[0m"
                res += f"\033[1m\033[33m{ keys[i] }\033[0m\n"
                res += Testing._displayHierarchy( tree[ keys[i] ], f"{ start }{ start_c } " )
            return res

    def reference(func : type) -> None :

        """
        Reference a function in the _messages{} disctionnary
        and execute it.

        In :
            func, type : Test function to reference
        Out :
            None
        """

        def wrapper( *args, **kwargs ) :
            Testing._current_function_path = func.__qualname__.split( "." )
            Testing._addHierarchy( Testing._current_function_path, Testing._messages )
            if not Testing._catch_error:
                return func( *args, **kwargs )
            try:
                return func( *args, **kwargs )
            except Exception as e:
                Testing._addMessage( Testing._current_function_path, Testing._messages, '\033[31m' + e.__str__() + '\033[0m' )
        return wrapper

    def display( ) -> None :

        """
        Display the result of all tests ran so far and their hierarchy.

        In :

        Out :
            None
        """

        print(
            f"\n\033[32m\033[1m{ Testing._total_tests - Testing._failed_tests }"
            f"\033[0m\033[32m tests passed\033[0m, \033[31m\033[1m{ Testing._failed_tests }"
            f"\033[0m\033[31m tests failed\033[0m\n{ Testing._displayHierarchy( Testing._messages, '' ) }"
        )
        return None

