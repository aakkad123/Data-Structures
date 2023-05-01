from dictionary.word_frequency import WordFrequency
from dictionary.base_dictionary import BaseDictionary
import bisect
import time


class ArrayDictionary(BaseDictionary):

    def __init__(self):
        # TO BE IMPLEMENTED
        # self._mydict = {}

        self.arr = []

    def build_dictionary(self, words_frequencies: [WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """

    # each element in words_frequencies is a tuple of (word, freq).
    # So we loop through that list and pass each element to add_w_f function

        for i in words_frequencies:
            self.add_word_frequency(i)



    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """

        for someWord in self.arr:
            if someWord[0] == word:
                return someWord[1]  # frequency # O(log n)

        return 0  # NOT FOUND


    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """

        word = word_frequency.word
        freq = word_frequency.frequency

        if len(self.arr) != 0:
            if self.search(word) != 0:  # NOT FOUND
                return False  # WORD ALRDY IN
            else:
                bisect.insort(self.arr, (word, freq))  # add word to list in sorted order O(n)
                return True

        else:  # EMPTY LIST
            self.arr.append((word, freq)) #add object to empty list
            self.arr.sort(key=lambda x: x[0], reverse=False) #sort
            return True

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """

        if self.search(word) == 0:  # NOT FOUND O(log n)
            return False
        else:
            for i in range(len(self.arr)): # O(n)
                if self.arr[i][0] == word:
                    self.arr.remove((self.arr[i]))
                    return True


    def autocomplete(self, prefix_word: str) -> [WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'prefix_word' as a prefix
        @param prefix_word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'prefix_word'
        """


        temp = []
        for (word, freq) in self.arr: # O(log n)
            if word.startswith(prefix_word):  # if start of word matches prefix :
                temp.append((word, freq))     # add the tuple to the temporary list
                temp.sort(key=lambda x: x[1], reverse=True)  # and sort the array from highest frequency to lowest  #O(n log n)

        num = 3
        if len(temp) < num:
            num = len(temp)  # check number results
        temp = temp[:num]   #  list goes up to 3, and will show results for less than 3

        autoCompleteList = []
        for (word, freq) in temp:
            autoCompleteList.append(WordFrequency(word, freq))  # loop through temp list,
                                                                # append results to new list with wordfrequency objects.

        return autoCompleteList