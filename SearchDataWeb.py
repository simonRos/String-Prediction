#!/usr/bin/python
class LetterNode:
    """
    Object representing a combination of letters and it's followers
    """
    def __init__(self,letter_combo):
        """
        Initialize with a string
        """
        self.letter = letter_combo
        #dictionary of followers, weighted
        self.followers = {}
        #does this pattern represent a full word?
        self.isWord = False

    def add(self, new_letter):
        """
        Add a follower
        """
        if new_letter not in self.followers.keys():
            self.followers[new_letter] = 0
        self.followers[new_letter] += 1

    def guessNextLetter(self):
        """
        Guess the next letter
        """
        try:
            most_likely_node = max(self.followers, key=self.followers.get)
        except:
            return None
        most_likely_letter = most_likely_node.letter
        return most_likely_letter

class LetterWeb:
    """
    A collection of linked LetterNodes
    """
    def __init__(self):
        """
        Initialize with None base node
        """
        self.nodes = {None: LetterNode(None)}

    def add(self, front, follow_dirty):
        """"
        Add a new LetterNode
        """
        if follow_dirty == None:
            #useless. abort
            return None
        follow = follow_dirty.lower()
        if follow not in self.nodes.keys():
            #create a new LetterNode
            self.nodes[follow] = LetterNode(follow)
        if front not in self.nodes.keys():
            self.nodes[front] = LetterNode(front)
        #link it to a previous node.
        self.nodes[front].add(self.nodes[follow])

    def guessWord(self, so_far):
        """
        Guess the complete word
        """
        next_letter = self.nodes[so_far].guessNextLetter()
        if next_letter == None:
            return so_far
        this_word = so_far + next_letter
        this_node = self.nodes[this_word]
        if this_node.isWord == True:
            return this_word
        else:
            return self.guessWord(this_word)

class WordNode:
    """
    Object representing a word and it's followers
    """
    def __init__(self,word):
        """
        Initialize with a string
        """
        self.word = word
        self.followers = {}

    def add(self, new_word):
        """
        Add a follower
        """
        if new_word not in self.followers.keys():
            self.followers[new_word] = 0
        self.followers[new_word] += 1

    def guessNextWord(self):
        """
        Guesses the next word
        """
        try:
            most_likely_node = max(self.followers, key=self.followers.get)
        except:
            return None
        most_likely_word = most_likely_node.word
        return most_likely_word

class WordWeb:
    """
    A collection of WordNodes and the corresponding LetterWeb
    """
    def __init__(self):
        """
        Initialize with a base node and a LetterWeb
        """
        self.nodes = {None: WordNode(None)}
        self.letters = LetterWeb()

    def add(self, in1, in2=None):
        """
        overloaded method calls _add_word or _add_array
        depending on input
        """
        if in2 == None:
            self._add_array(in1)
        else:
            self._add_word(in1, in2)

    def _add_word(self, front_dirty, follow_dirty):
        """
        Add a new wordNode and add letters to LetterWeb
        """
        #sanitize data
        front = None
        if front_dirty != None:
            front = front_dirty.lower()
        follow = follow_dirty.lower()
        #word level
        if follow not in self.nodes.keys():
            #create a new WordNode
            self.nodes[follow] = WordNode(follow)
        #add to node of word it follows
        self.nodes[front].add(self.nodes[follow])
        if front == None:
            self.nodes[follow].starter = True
                #letter level
        word_so_far = None
        for letter in follow:
            #build word letter by letter
            self.letters.add(word_so_far, letter)
            if word_so_far == None:
                word_so_far = letter
            else:
                word_so_far += letter
        self.letters.add(None,word_so_far)
        self.letters.nodes[word_so_far].isWord = True

    def _add_array(self, data):
        """
        Add every word in an array of phrases
        """
        for phrase in data:
            last_word = None
            for word in phrase.split():
                self._add_word(last_word, word)
                last_word = word
                
    def guessPhrase(self, seed_word, most):
        """
        Guess the whole phrase
        """
        so_far = seed_word
        next_word = ""
        try:
            next_word = self.nodes[seed_word].guessNextWord()
        except:
            next_word = None
        while next_word != None and most > 0:
            so_far += " " + next_word
            try:
                next_word = self.nodes[next_word].guessNextWord()
            except:
                next_word = None
            most -= 1
        return so_far     

    def optimize(self):
        """
        Combine words which only appear together
        Results in fewer steps per prediction but larger data structure
        """
        rev_list = []
        comp_list = []
        for v in self.nodes:
            if v != None:
                #find words with only 1 follower
                if len(self.nodes[v].followers) == 1:
                    tail = list(self.nodes[v].followers)[0].word
                    rev_list.append((v, tail))
        for pair in rev_list:
            combo = pair[0] + " " + pair[1]
            self.nodes[combo] = self.nodes[pair[0]]
            self.nodes[combo].followers = self.nodes[pair[1]].followers
        #clean obsolete words
        for pair in rev_list:
            del self.nodes[pair[0]]
        
