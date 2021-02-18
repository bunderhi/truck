import numpy as np
import math

def setgoal(mask):
    """ 
        Find the coordinates for the goal using the freespace mask (birdseye view) 
    """   
    def first_nonzero(arr, axis, invalid_val=-1):
        """ List leftmost nonzero entry for each row in an array """
        mask = arr!=0
        return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)

    def last_nonzero(arr, axis, invalid_val=-1):
        """ List rightmost nonzero entry for each row in an array """
        mask = arr!=0
        val = arr.shape[axis] - np.flip(mask, axis=axis).argmax(axis=axis) - 1
        return np.where(mask.any(axis=axis), val, invalid_val)

    goal = None
    left = first_nonzero(mask, axis=1, invalid_val=-1)
    right = last_nonzero(mask, axis=1, invalid_val=-1)
    print (left,right)
    # find topmost row with at least one nonzero entry
    for idx, x in np.ndenumerate(left):   
        if x>-1:
            print(idx[0],x,right[idx])
            if right[idx] > x:
                xval = math.floor(((x + right[idx]) / 2))
                yval = idx[0]
                print ("Goal",xval,yval,mask[yval,xval])
                if mask[yval,xval] > 0:
                    print (xval,yval)
                    goal = (xval,yval)
                    break;
    return goal