```

str: '123'       is a float? expected(True ) got -> True
str: '-123'      is a float? expected(True ) got -> True
str: '+123'      is a float? expected(True ) got -> True
str: '123.45'    is a float? expected(True ) got -> True
str: '.45'       is a float? expected(True ) got -> True
str: '-123.45'   is a float? expected(True ) got -> True
str: '+123.45'   is a float? expected(True ) got -> True
str: '1.23e-4'   is a float? expected(True ) got -> True
str: '-1.23E4'   is a float? expected(True ) got -> True
str: '1.23e+4'   is a float? expected(True ) got -> True
str: '1.23E-4'   is a float? expected(True ) got -> True
str: '1.23E4'    is a float? expected(True ) got -> True
str: '2.'        is a float? expected(False) got -> False
str: 'abc'       is a float? expected(False) got -> False
str: '123a'      is a float? expected(False) got -> False
str: '--123'     is a float? expected(False) got -> False
str: '123.45.67' is a float? expected(False) got -> False
str: '123.45.67' is a float? expected(False) got -> False
str: '123.45a'   is a float? expected(False) got -> False
str: '123a2'     is a float? expected(False) got -> False
str: '123e2.2'   is a float? expected(False) got -> False
str: '123    '   is a float? expected(False) got -> False
str: '  123  '   is a float? expected(False) got -> False

Matched 23 out of 23 test cases!

```