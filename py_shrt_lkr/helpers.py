__author__ = 'matthieu'

#Returns the elements from the list b that are not in the list a
def list_diff(aLst, bLst):
	ret = []
	for a in bLst:
		if a not in aLst:
			ret.append(a)
	return ret
