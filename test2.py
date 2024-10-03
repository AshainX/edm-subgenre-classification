def highscore(parents):
    n = len(parents)
    children = [[] for _ in range(n)]
    for i in range(1, n):
        children[parents[i]].append(i)
    
    subtree = [0] * n
    
    # DFS to calculate the size of each subtree
    def dfs(node):
        size = 1  # Each node counts as part of its own subtree
        for child in children[node]:
            size += dfs(child)
        subtree[node] = size
        return size

    # Calculate the size of the whole tree
    totalsize = dfs(0)
    
    ms = 0
    countms = 0
    
    # Now calculate the score for each node
    for node in range(n):
        score = 1
        remsize = totalsize - subtree[node]  # Size of the rest of the tree
        
        if remsize > 0:
            score *= remsize
        
        # Multiply by the sizes of the subtrees of the current node
        for child in children[node]:
            score *= subtree[child]
        
        if score > ms:
            ms = score
            countms = 1
        elif score == ms:
            countms += 1
    
    return countms

# Test cases
test_cases = [
    [-1, 2, 0, 2, 0],  # Sample test case 1
    [-1, 2, 0],        # Sample test case 2
    [-1, 0, 1, 2],     # Additional test case
    [-1, 0, 0, 1, 1],  # Additional test case
]

for i, parents in enumerate(test_cases, 1):
    result = highscore(parents)
    print(f"Test case {i}:")
    print(f"Input: {parents}")
    print(f"Output: {result}")
    print()
