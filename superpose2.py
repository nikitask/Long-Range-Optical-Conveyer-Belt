def superpose2(phi1, phi2, alpha, amp1 = [], amp2 = [], ampout = []):
    tempshape = phi1.shape
    w = tempshape[1]
    h = tempshape[0]
    if len(amp1) == 0:
        temp1 = np.ones(w)
        temp2 = np.ones(h)
        for r in temp2:
            amp1 += [temp1]
    if len(amp2) == 0:
        temp1 = ones(w)
        temp2 = ones(h)
        for r in temp2:
            amp2 += [temp1]
