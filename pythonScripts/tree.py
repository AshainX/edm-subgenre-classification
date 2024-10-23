from typing import List 



#high value score count
def high(parents: List[int])->int:
    n=len(parents)
    child = [[] for _ in range(n)]
    for i in range(0,n):
        child[parents[i]].append(i)
    

    def depth(node: int) -> List[int, int]:
        if not child(node):
            return 1,1
        
        s = 1
        score = 1
        for c in child[node]:
            cs, csc = depth(child)
            s+=cs
            score*=cs

        return s, score
    
    scores = [depth(i)[1] for i in range(n)]
    ms= max(scores)
    return sum(1 for s in scores if s==ms)




test_cases = [
    [-1, 2, 0, 2, 0],  
    [-1, 2, 0],        
    [-1, 0, 1, 2],     
    [-1, 0, 0, 1, 1],  
]

for i, parents in enumerate(test_cases,1):
    r = high(parents)
    print(f"testcase {i}:")
    print(f"inpt: {parents}")
    print(f"out: {r}")
    
    