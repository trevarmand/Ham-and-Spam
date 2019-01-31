# Thank you to Professor Friefeld for the inspiration.
# Recreation of a Java program covered in lecture.


class MailDetector:
    def __init__(self):
        self.spam_words = {}
        self.ham_words = {}

        self.spam_word_count = 0
        self.ham_word_count = 0
        self.total_words = 0

        self.spam_email_count = 0
        self.ham_email_count = 0

    def load(self):
        print("File extension not necessary.\n")
        spam_name = input("Enter name of spam training data file:\n") + ".txt"
        ham_name = input("Enter name of ham training data file:\n") + ".txt"
        spam_file = open(spam_name, 'r')
        ham_file = open(ham_name, 'r')

        # Put spam words in the spam dictionary
        for line in spam_file:
            # All training emails are one line long
            self.spam_email_count += 1
            for word in line.split():
                self.spam_words[word] = self.spam_words.get(word, 0) + 1
                self.spam_word_count += 1

        # Put ham words in the ham dictionary
        for line in ham_file:
            self.ham_email_count += 1
            for word in line.split():
                self.ham_words[word] = self.ham_words.get(word, 0) + 1
                self.ham_word_count += 1

        self.total_words = self.spam_word_count + self.ham_word_count

        print('Model Trained!\n')
        print('Ham words read: ' + str(self.ham_word_count))
        print('Spam words read: ' + str(self.spam_word_count))

    def analyze(self, target):
        target_file = open(target + ".txt", 'r')

        running_prob_sum = 0.0
        words_analyzed_count = 0;

        for line in target_file:
            for word in line.split():
                spam_freq = self.spam_words.get(word, 0)
                ham_freq = self.spam_words.get(word, 0)

                print("for: " + word)
                print("spam freq: " + str(spam_freq))
                print("ham freq: " + str(ham_freq))
                if spam_freq == 0 & ham_freq == 0:
                    print("ignoring" + word)
                    continue # Ignore words that haven't been trained in
                else:
                    # Probability of word given email is spam
                    spam_word_prob = spam_freq / self.spam_word_count

                    # Avoid sabotaging the probability with 0 values
                    if spam_word_prob == 0:
                        spam_prob = 0.0001

                    # Probability a given email is spam
                    # THIS DEPENDS ON TRAINING DATA: SPAM:HAM RATIO MUST BE ACCURATE
                    spam_prob = self.spam_email_count / (self.ham_email_count + self.spam_email_count)

                    word_prob = spam_freq + ham_freq / (self.ham_email_count + self.spam_email_count)

                    # P(Spam | word) = (P(Word | Spam) * P(Spam)) / P(word)
                    spam_prob = (spam_word_prob * spam_prob) / word_prob

                    running_prob_sum += spam_prob
                    words_analyzed_count += 1

        if words_analyzed_count == 0:
            print("Sorry, we cannot confidently categorize this data!")
        else:
            average_probability = running_prob_sum / words_analyzed_count
            print("We determined there is a " + str(average_probability)
                  + ' chance this is spam')


md = MailDetector()
md.load()
md.analyze("test")
