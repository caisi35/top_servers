def versions(v1, v2):
    v1 = v1.split('.')
    v2 = v2.split('.')
    while v1 and v2:
        value1 = int(v1.pop(0))
        value2 = int(v2.pop(0))
        if value1 > value2:
            return 1
        elif value1 < value2:
            return -1
    if v1:
        for i in v1:
            if int(i):
                return 1
        return 0
    elif v2:
        for i in v2:
            if int(i):
                return -1
        return 0
    else:
        return 0


def test():
    version1 = "0.1"
    version2 = "1.1"
    assert versions(version1, version2) == -1

    version1 = "1.0.1"
    version2 = "1"
    assert versions(version1, version2) == 1

    version1 = "7.5.2.4"
    version2 = "7.5.3"
    assert versions(version1, version2) == -1

    version1 = "1.01"
    version2 = "1.001"
    assert versions(version1, version2) == 0

    version1 = "1.0"
    version2 = "1.0.0"
    assert versions(version1, version2) == 0


if __name__ == '__main__':
    test()
