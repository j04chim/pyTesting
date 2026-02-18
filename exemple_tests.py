from pyTesting import Testing

def pow2(a):
    return a ** 2

def squareRoot(a):
    return a ** 0.5

@Testing.reference
def testWithParameter(a):
    Testing.test( a == 1,
                 f"{a} != 1"
        )

class GrandParent:
    @Testing.reference
    def willThrowAnError():

        res = squareRoot(9)

        Testing.test( res.readline() ,
                    f"{res} != 3"
            )

    class Parent:
        class Child:
            @Testing.reference
            def passingTests():

                res = pow2(2)

                Testing.test( res == 4,
                            f"{res} != 4"
                    )

                res = pow2(6)

                Testing.test( res == 36,
                            f"{res} != 36"
                    )

class FailingTests:

    @Testing.reference
    def willFail():
        Testing.test( 2 == 1,
                    "2 != 1"
            )
        Testing.test( "Hello" == "world!",
                    "\"Hello\" != \"world!\""
            )

testWithParameter(1)
GrandParent.willThrowAnError()
GrandParent.Parent.Child.passingTests()
FailingTests.willFail()

Testing.display()
