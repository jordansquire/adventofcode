from re import split

from util.util import timeit

def _find_matching_char(str1, str2) -> str:
    for char1 in str1:
        for char2 in str2:
            if char1 == char2:
                return char1

def _find_matching_char3(str1, str2, str3) -> str:
    for char1 in str1:
        for char2 in str2:
            for char3 in str3:
                if char1 == char2 == char3:
                    return char1

def _score_char(char: str) -> int:
    char_num = ord(char)
    if char_num <= 90:
        return char_num - 38
    else:
        return char_num - 96

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("input_test.txt", "r")
    else:
        file = open("input.txt", "r")

    score = 0
    for line in file:
        str1 = line[:int(len(line)/2)]
        str2 = line[int(len(line)/2):]
        score += _score_char(_find_matching_char(str1, str2))

    return score

@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = open("input_test.txt", "r")
    else:
        file = open("input.txt", "r")

    score = 0
    while True:
        lines = []
        while len(lines) < 3:
            line = file.readline()

            if not line:
                return score

            lines.append(line)
        score += _score_char(_find_matching_char3(lines[0], lines[1], lines[2]))

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')
