def bubble_sort_right_to_left(elements):
    print(f"Original list: {elements}")
    n = len(elements)
    
    for i in range(n):
        made_change = False  # Reset each outer loop pass
        print(f"\n=== Outer loop iteration {i} ===")
        
        # Move from right to left (start at end, stop at 1)
        for j in range(n - 1, 0, -1):
            left = elements[j - 1]
            right = elements[j]
            print(f"  Comparing {right} < {left}")
            
            if right < left:
                # Swap
                elements[j], elements[j - 1] = left, right
                made_change = True
                print(f"  Swapped -> {elements}")
            else:
                print(f"  No swap needed")

        if not made_change:
            print("  No changes made this pass, list is sorted.")
            break

    print(f"\nSorted list: {elements}")


element_list = [34, 12, 25, 45, 2, 23, 0]
bubble_sort_right_to_left(element_list)
