from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency

# Class representing a node in the Trie
class TrieNode:

    def __init__(self, letter=None, frequency=None, is_last=False):
        self.counter = 0
        self.currentRoot = None
        self.letter = letter  # letter stored at this node
        self.frequency = frequency  # frequency of the word if this letter is the end of a word
        self.is_last = is_last  # True if this letter is the end of a word
        self.children: dict[str, TrieNode] = {}  # a hashtable containing children nodes, key = letter, value =
        # child node


class TrieDictionary(BaseDictionary):

    def __init__(self):
        self.root = TrieNode()
        self.counter = 0
        self.arr = []

    def build_dictionary(self, words_frequencies: [WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        # TO BE IMPLEMENTED
        for i in words_frequencies:
            self.add_word_frequency(i)

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        currentNode = self.root

        for i in word:
            node = currentNode.children.get(i)
            if node is None:  # case 1: does not exist in the Trie
                return 0
            currentNode = node

        if currentNode.is_last:  # case 2: does exit in the Trie
            return currentNode.frequency
        else:  # case 3: sting is a prefix in another string, but does not exist in Trie
            return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        curr = self.root
        for ch in word_frequency.word:
            node = curr.children.get(ch)
            curr.letter = ch

            if node is None:
                node = TrieNode()
                curr.children.update({ch: node})
            curr = node
        if curr.is_last:
            return False

        curr.is_last = True
        curr.frequency = word_frequency.frequency
        return True

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """

        currNode = self.root
        if self.search(word) != 0:
            for i in word:
                if i not in currNode.children:
                    return False
                else:
                    currNode = currNode.children[i]
        if currNode.is_last:
            currNode.frequency = None
            currNode.is_last = False
            return True
        else:
            return False


    def autocomplete(self, word: str) -> [WordFrequency]:
        self.arr = []

        node = self.root

        for i in word:
            # no string in the Trie has this prefix
            if not node.children.get(i):
                return []
            node = node.children[i]


        self.AutoCompleteHelper(node, word) # O(length of string)
        self.arr.sort(key=lambda x: x[1], reverse=True) # O(n log n)
        num = 3
        if len(self.arr) < num:
            num = len(self.arr)
        arr = self.arr[:num]
        wordArr = []

        for wordfreq in arr:
            wordArr.append(WordFrequency(wordfreq[0], wordfreq[1]))
        return wordArr

    # recursion helper, Time O(n), where n is number of nodes in branches
    def AutoCompleteHelper(self, node, word):
        # Method to recursively traverse the trie
        # and return a whole word.
        if node.is_last:
            self.arr.append((word, node.frequency))

        for key, val in node.children.items():
            self.AutoCompleteHelper(val, word + key)

