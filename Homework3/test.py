sentences = [[], [['~MiniSudoku', 'Ac', 'C']]], [[], [['MiniSudoku', 'Da', 'x'], '|', ['MiniSudoku', 'Db', 'x'], '|', ['MiniSudoku', 'Dc', 'x'], '|', ['MiniSudoku', 'Dd', 'x']]], [[], [['~MiniSudoku', 'x', 'D'], '|', ['~MiniSudoku', 'x', 'A']]]


sorted_sentences = sorted(sentences, key=lambda s: len(s))

print(sorted_sentences)