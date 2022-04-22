def id3(Y, D, U):
    checked = 0
    for (x, y) in U:
        if y == klasa_y:
            checked += 1
    if checked == len(U):
        return Lisc_z_klasa_y
    if len(D) == 0:
        return Lisc_z_najczestsza_klasa_w_U
    d = infGain(max(D))
    Uj = []
    for (x, y) in U:
        if x[d] == d[j]:
            Uj.append((x, y))
    return Drzewo_z_korzeniem_d_i_krawedziami_dj_prowadzacymi_do_drzew

def infGain():
    pass
