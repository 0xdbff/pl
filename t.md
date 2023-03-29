# NFA

    d = [0,1,,2,3,4,5,6,7,8,9]

    d*|.


    States: {q0, q1}

    --OPTIONAL SIGN
    Alphabet: {'+', '-'}
    Start state: q0
    Final state: {q0, q1}
    Transitions:
        q0 -ε-> q0
        q0 -+-> q1
        q0 ---> q1


    --INTEGER PART
    States: {q2, q3}
    Alphabet: {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    Start state: q2
    Final state: {q3}
    Transitions:
        q2 -0-> q3
        q2 -1-> q3
        ...
        q2 -9-> q3
        q3 -0-> q3
        q3 -1-> q3
        ...
        q3 -9-> q3

    --OPTIONAL DECIMAL PART
    States: {q4, q5, q6}
    Alphabet: {'.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    Start state: q4
    Final state: {q4, q6}
    Transitions:
        q4 -ε-> q4
        q4 -.-> q5
        q5 -0-> q6
        q5 -1-> q6
        ...
        q5 -9-> q6
        q6 -0-> q6
        q6 -1-> q6
        ...
        q6 -9-> q6

