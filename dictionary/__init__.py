from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency
import time
import sys
from dictionary.word_frequency import WordFrequency
from dictionary.base_dictionary import BaseDictionary
from dictionary.array_dictionary import ArrayDictionary
from dictionary.linkedlist_dictionary import LinkedListDictionary
from dictionary.trie_dictionary import TrieDictionary


class ListNode:
    """
    Define a node in the linked list
    """

    def __init__(self, word_frequency: WordFrequency):
        self.word_frequency = word_frequency
        self.next = None



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
            while node is not None:

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
            freq = self.search(newNode.word_frequency.word)
            if freq == word_frequency.frequency:
                return False
            else:
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
                while tempNode.next.word_frequency.word != word:
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
        while node is not None:
            if node.word_frequency.word.startswith(word):
                arr.append(node.word_frequency)
                arr.sort(key=lambda x: x.frequency, reverse=True)
            node = node.next

        num = 3
        if len(arr) < num:
            num = len(arr)
        arr = arr[:num]
        wordArr = []

        for wordfreq in arr:
            wordArr.append(WordFrequency(wordfreq.word, wordfreq.frequency))
        return wordArr


def main():
    def usage():
        """
        Print help/usage message.
        """
        # On Teaching servers, use 'python3'
        # On Windows, you may need to use 'python' instead of 'python3'
        print('python3 dictionary_file_based.py', '<approach> <data fileName> <command fileName> <output fileName>')
        print('<approach> = <array | linkedlist | trie>')
        sys.exit(1)

    if __name__ == '__main__':
        # Fetch the command line arguments
        args = sys.argv

        if len(args) != 5:
            print('Incorrect number of arguments.')
            usage()

        # initialise search agent
        agent: BaseDictionary = None
        if args[1] == 'array':
            agent = ArrayDictionary()
        elif args[1] == 'linkedlist':
            agent = LinkedListDictionary()
        elif args[1] == 'trie':
            agent = TrieDictionary()
        else:
            print('Incorrect argument value.')
            usage()

        # read from data file to populate the initial set of points
        data_filename = args[2]
        words_frequencies_from_file = []
        try:
            data_file = open(data_filename, 'r')
            for line in data_file:
                values = line.split()
                word = values[0]
                frequency = int(values[1])
                word_frequency = WordFrequency(word, frequency)  # each line contains a word and its frequency
                words_frequencies_from_file.append(word_frequency)
            data_file.close()
            agent.build_dictionary(words_frequencies_from_file)
        except FileNotFoundError as e:
            print("Data file doesn't exist.")
            usage()

        command_filename = args[3]
        output_filename = args[4]
        # Parse the commands in command file
        try:
            command_file = open(command_filename, 'r')
            output_file = open(output_filename, 'w')

            for line in command_file:
                command_values = line.split()
                command = command_values[0]
                # search
                if command == 'S':
                    word = command_values[1]
                    start = time.time()
                    search_result = agent.search(word)
                    end = time.time()
                    duration_in_sec = end - start
                    print(f"Searching took {duration_in_sec:.2f} seconds")
                    if search_result > 0:
                        output_file.write(f"Found '{word}' with frequency {search_result}\n")
                    else:
                        output_file.write(f"NOT Found '{word}'\n")

                # add
                elif command == 'A':
                    word = command_values[1]
                    frequency = int(command_values[2])
                    word_frequency = WordFrequency(word, frequency)
                    start = time.time()
                    if not agent.add_word_frequency(word_frequency):
                        output_file.write(f"Add '{word}' failed\n")
                    else:
                        end = time.time()
                        duration_in_sec = end - start
                        output_file.write(f"Add '{word}' succeeded\n")
                    print(f"Adding took {duration_in_sec:.2f} seconds")


                # delete
                elif command == 'D':
                    word = command_values[1]
                    start = time.time()
                    if not agent.delete_word(word):
                        output_file.write(f"Delete '{word}' failed\n")
                    else:
                        end = time.time()
                        duration_in_sec = end - start

                        output_file.write(f"Delete '{word}' succeeded\n")
                    print(f"Deleting took {duration_in_sec:.2f} seconds")

                # check
                elif command == 'AC':
                    word = command_values[1]
                    start = time.time()
                    list_words = agent.autocomplete(word)
                    end = time.time()
                    duration_in_sec = end - start
                    print(f"Autocomplete took {duration_in_sec:.2f} seconds")

                    line = "Autocomplete for '" + word + "': [ "
                    for item in list_words:
                        line = line + item.word + ": " + str(item.frequency) + "  "
                    output_file.write(line + ']\n')

                else:
                    print('Unknown command.')
                    print(line)

            output_file.close()
            command_file.close()
        except FileNotFoundError as e:
            print("Command file doesn't exist.")
            usage()


    start_time = time.time()
    LinkedListDictionary.delete_word(numbers)
    end_time = time.time()
    duration_in_sec = end_time - start_time
    print(f"After bubble sort: {numbers} \nSorted in {duration_in_sec:.2f} seconds")
    print("Size of array = " + str(len(numbers)))


if __name__ == "__main__":
    main()