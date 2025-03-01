def parser(strData, no_first=False):
    idx_left = 0
    idx_right = 0
    bracket = 0
    data = []

    # print("enter parser")
    for idx, char in enumerate(strData):
        if char == "(":  # find the left
            if bracket == 0:
                idx_left = idx + 1
            bracket += 1

            if no_first and idx_left != 1 and idx_right == 0:
                no_first = False
                if strData[idx_left - 2] == ' ':
                    data.append(strData[0:idx_left - 2])
                else:
                    data.append(strData[0:idx_left - 1])

        if char == ")":  # find the right
            bracket -= 1
            idx_right = idx

            if bracket == 0:  # find the whole bracket
                if '(' in strData[idx_left:idx_right]:
                    data.append(parser(strData[idx_left:idx_right], True))
                else:
                    data.append([x for x in strData[idx_left:idx_right].split() if x])

    return data


def sexp_decode(str):
    decodeData = parser(str)
    # print(decodeData)
    return decodeData


def pack(listData):
    strData = "("
    for idx, x in enumerate(listData, 1):
        if isinstance(x, list):
            x = pack(x)
        if idx != len(listData):
            strData = strData + str(x) + " "
        else:
            strData = strData + str(x)
    strData = strData + ")"
    return strData


def sexp_encode(list):
    encodeData = ""
    for x in list:
        encodeData += pack(x)
    return encodeData
