
class Board:
    tag = 'board'
    fill = '#0000FF'

class Holes:
    tag = 'hole'
    fill = '#808080'
    outline = '#FFFFFF'

class Marbles:
    tag = 'marble'
    selected = '#FF0000'

class Players:
    class Black(int):
        fill = '#000000'
        vp = 0
        positions = [
                       (3,3), (3,4), (3,5),
             (2,1), (2,2), (2,3), (2,4), (2,5), (2,6),
                (1,1), (1,2), (1,3), (1,4), (1,5),
                ]

    class White(int):
        fill = '#FFFFFF'
        vp = 3
        positions = [
                (9,5), (9,6), (9,7), (9,8), (9,9),
            (8,4), (8,5), (8,6), (8,7), (8,8), (8,9),
                      (7,5), (7,6), (7,7),
                ]
