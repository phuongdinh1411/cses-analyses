#!/usr/bin/env python3
import os

# Problem information from CSES
problem_info = {
    'coin_piles_analysis.md': {
        'title': 'Coin Piles Analysis',
        'description': 'This problem involves coin piles and requires careful analysis of the constraints and optimal strategies.',
        'category': 'Greedy/Constructive Algorithms',
        'completion_rate': '48,555 / 53,214 (91.2%)'
    },
    'chessboard_and_queens_analysis.md': {
        'title': 'Chessboard and Queens Analysis',
        'description': 'This problem involves placing queens on a chessboard with specific constraints.',
        'category': 'Backtracking/Recursion',
        'completion_rate': '22,876 / 23,306 (98.2%)'
    },
    'creating_strings_analysis.md': {
        'title': 'Creating Strings Analysis',
        'description': 'This problem involves generating all possible strings from given characters.',
        'category': 'Permutations/Combinatorics',
        'completion_rate': '38,107 / 39,119 (97.4%)'
    },
    'digit_queries_analysis.md': {
        'title': 'Digit Queries Analysis',
        'description': 'This problem involves finding specific digits in a sequence of numbers.',
        'category': 'Number Theory/Pattern Recognition',
        'completion_rate': '16,187 / 18,992 (85.2%)'
    },
    'gray_code_analysis.md': {
        'title': 'Gray Code Analysis',
        'description': 'This problem involves generating Gray codes with specific properties.',
        'category': 'Bit Manipulation/Combinatorics',
        'completion_rate': '29,819 / 33,620 (88.7%)'
    },
    'grid_coloring_i_analysis.md': {
        'title': 'Grid Coloring I Analysis',
        'description': 'This problem involves coloring a grid with specific constraints.',
        'category': 'Graph Coloring/Constructive',
        'completion_rate': '1,953 / 2,020 (96.7%)'
    },
    'grid_path_description_analysis.md': {
        'title': 'Grid Path Description Analysis',
        'description': 'This problem involves describing paths on a grid with specific rules.',
        'category': 'Grid Algorithms/Pattern Recognition',
        'completion_rate': '9,079 / 11,819 (76.8%)'
    },
    'knight_moves_grid_analysis.md': {
        'title': 'Knight Moves Grid Analysis',
        'description': 'This problem involves knight movements on a grid with specific constraints.',
        'category': 'Grid Algorithms/Graph Theory',
        'completion_rate': '2,406 / 2,449 (98.2%)'
    },
    'mex_grid_construction_analysis.md': {
        'title': 'Mex Grid Construction Analysis',
        'description': 'This problem involves constructing a grid with specific MEX properties.',
        'category': 'Constructive Algorithms/Grid',
        'completion_rate': '2,353 / 2,520 (93.4%)'
    },
    'mex_grid_construction_ii_analysis.md': {
        'title': 'Mex Grid Construction II Analysis',
        'description': 'This is an advanced version of the MEX grid construction problem.',
        'category': 'Advanced Constructive/Grid',
        'completion_rate': '2,353 / 2,520 (93.4%)'
    },
    'palindrome_reorder_analysis.md': {
        'title': 'Palindrome Reorder Analysis',
        'description': 'This problem involves reordering characters to form palindromes.',
        'category': 'String Algorithms/Palindromes',
        'completion_rate': '44,988 / 47,536 (94.6%)'
    },
    'raab_game_i_analysis.md': {
        'title': 'Raab Game I Analysis',
        'description': 'This problem involves a specific game with optimal strategy analysis.',
        'category': 'Game Theory/Strategy',
        'completion_rate': '2,458 / 2,810 (87.5%)'
    },
    'string_reorder_analysis.md': {
        'title': 'String Reorder Analysis',
        'description': 'This problem involves reordering strings with specific constraints.',
        'category': 'String Algorithms/Constructive',
        'completion_rate': '2,032 / 2,360 (86.1%)'
    },
    'tower_of_hanoi_analysis.md': {
        'title': 'Tower of Hanoi Analysis',
        'description': 'This problem involves the classic Tower of Hanoi puzzle with specific constraints.',
        'category': 'Recursion/Pattern Recognition',
        'completion_rate': '27,568 / 28,676 (96.1%)'
    }
}

def add_placeholder_content(file_path):
    """Add placeholder content to an empty problem file."""
    
    filename = os.path.basename(file_path)
    if filename not in problem_info:
        return
    
    info = problem_info[filename]
    
    # Read the current content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if it's already been updated
    if 'Status' in content:
        print(f"Already updated: {filename}")
        return
    
    # Create the placeholder content
    placeholder = f"""

## Problem Description

**Status**: ⏳ Analysis in progress

{info['description']}

## Key Points

- **Difficulty**: Introductory
- **Category**: {info['category']}
- **Completion Rate**: {info['completion_rate']}

## TODO

- [ ] Problem statement analysis
- [ ] Solution approach
- [ ] Implementation details
- [ ] Time and space complexity analysis
- [ ] Example walkthrough
- [ ] Code solution

---

*This analysis will be completed soon. Check back for the full solution!*
"""
    
    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content + placeholder)
    
    print(f"Added placeholder to: {filename}")

def main():
    """Add placeholder content to all empty problem files."""
    
    intro_dir = 'problem_soulutions/introductory_problems'
    
    for filename in problem_info.keys():
        file_path = os.path.join(intro_dir, filename)
        if os.path.exists(file_path):
            add_placeholder_content(file_path)

if __name__ == "__main__":
    main() 