from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency


class ListNode:
    """
    Define a node in the linked list
    """

    def __init__(self, word_frequency: WordFrequency):
        self.word_frequency = word_frequency
        self.next = None


# ------------------------------------------------------------------------
# This class  is required TO BE IMPLEMENTED
# Linked-List-based dictionary implementation
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------
class LinkedListDictionary(BaseDictionary):

    def __init__(self):
        # TO BE IMPLEMENTED
        self.head = None
        self.tail = None

    def build_dictionary(self, words_frequencies: [WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        for i in words_frequencies:

            self.add_word_frequency(i)

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """

        # TO BE IMPLEMENTED

        if self.head is None:
            return 0
        else:
            node = self.head
            while node is not None:  # O(n)

                if node.word_frequency.word == word:
                    return node.word_frequency.frequency
                node = node.next
            return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """

        newNode = ListNode(word_frequency)
        if self.head is None and self.tail is None:
            self.head = newNode
            self.tail = newNode
            return True
        else:
            if self.search(newNode.word_frequency.word) != 0:
                return False

            else: # Inserting new node to head O(1)
                newNode.next = self.head
                self.head = newNode
                return True

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        num = self.search(word)
        if num == 0:
            return False
        else:
            if self.head.word_frequency.word == word:
                self.head = self.head.next
                return True
            else:
                tempNode = self.head
                while tempNode.next.word_frequency.word != word: # O(n) - Look  thru entire list to find word
                    tempNode = tempNode.next
                nextNode = tempNode.next
                tempNode.next = nextNode.next
                return True


    def autocomplete(self, word: str) -> [WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        arr = []
        node = self.head
        while node is not None: #O(n)
            if node.word_frequency.word.startswith(word):
                arr.append(node.word_frequency)
                arr.sort(key=lambda x: x.frequency, reverse=True)# O(n log n )
            node = node.next


        num = 3
        if len(arr) < num:
            num = len(arr)
        arr = arr[:num]
        wordArr = []

        for wordfreq in arr:
            wordArr.append(WordFrequency(wordfreq.word, wordfreq.frequency))
        return wordArr
