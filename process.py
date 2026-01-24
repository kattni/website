import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        lines = f.readlines()
        words = set()
        for line in lines:
            if line == "Misspelled words:\n":
                print("Ignore.")
            elif line.startswith("<context>"):
                print("Ignore.")
            elif line.startswith("----------"):
                print("Ignore.")
            elif line == "\n":
                print("Ignore.")
            else:
                words.add(line)
    with open(f"{filename}-out.txt", 'w') as f:
        for word in sorted(words):
            f.write(word)
