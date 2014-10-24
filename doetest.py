import numpy as np
import doe_add2 as da

phi1 = np.array([[1,2,3,4,5,6,7,8,9,10],[11,12,13,14,15,16,17,18,19,20]])
phi2 = phi1 + 20

amp1 = np.array([[1,1,1,1,1,1,1,1,1,10],[1,1,0.2,1,1,1,1,1,1,1]])
amp2 = amp1 + 1

phi = da.doe_add2(phi1,phi2, amp1=amp1, amp2=amp2)
print(phi)