def setPlayMode(playmode):  # play mode BKO/PO/KOL
    msg = ""
    if playmode == "BKO":
        msg = "(playMode BeforeKickOff)"
    elif playmode == "PO":
        msg = "(playMode PlayOn)"
    elif playmode == "KOL":
        msg = "(playMode KickOff_Left)"
    return msg


def setBallPos(x, y, z, vx=0, vy=0, vz=0):
    msg = "(ball (pos " + str(x) + " " + str(y) + " " + str(z) + ")" \
          + "(vel " + str(vx) + " " + str(vy) + " " + str(vz) + "))"
    return msg


def reqFullState():
    return "(reqfullstate)"
