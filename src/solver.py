import time

#SOLVER
class Solver:
    def __init__(self, operands, result):
        self.solve(operands, result)

    def solve(self, operands, result):
        self.operands = operands
        self.result = result
        self.valid_results = []
        self.nums = [i for i in range(10)]
        self.final_results = []
        self.solution_number = 0

        comb_letters = result
        for word in operands:
            comb_letters += word

        self.letters = []
        for letter in comb_letters:
            if letter not in self.letters:
                self.letters.append(letter)

        r = len(self.letters)
        n = len(self.nums)
        data = [0 for i in range(r)]
        start_time = time.time()

        self.combination(self.nums, n, r, 0, 0, data, self.valid_results)
        self.get_answers()
        
        end_time = time.time()
        self.runtime = end_time - start_time
        self.checks = len(self.valid_results)
        print(end_time - start_time)

    def read_file(self, file_name):
        list_of_words = []
        f = open(file_name, 'r')
        lines = f.readlines()
        
        for i in range(len(lines) - 2):
            list_of_words.append(lines[i].rstrip())
        list_of_words[-1] = list_of_words[-1][:-1]
        res = lines[-1].rstrip()
        return list_of_words, res


    def word2num(self, word, list_of_letters, list_of_num):
        num = 0
        for i in range(len(word)):
            idx = list_of_letters.index(word[len(word) - i - 1])
            # print(list_of_num)
            num += (10**i)*list_of_num[idx]
        return num

    def check(self, list_of_words, res, list_of_num):
        rhs = self.word2num(res, self.letters, list_of_num)
        lhs = 0
        for word in list_of_words:
            lhs += self.word2num(word, self.letters, list_of_num)
        return lhs == rhs

    def is_valid(self, list_of_words, res, list_of_letters, list_of_num):
        valid = True
        combined_list = list_of_words.copy()
        combined_list.append(res)
        for word in combined_list:
            idx = list_of_letters.index(word[0])
            if (list_of_num[idx] == 0):
                valid = False
        return valid

    def combination(self, initial, n, r, outer_index, inner_index, data, result):
        if (r == 0): #Base case 0: Array of size r achieved
            temp = data.copy()
            x = len(temp)
            self.permutation(temp, 0, x, result)
            return

        elif (n == 0): #Base case 1: Outer index reaches end of initial
            return

        else: #Recursion
            data[inner_index] = initial[outer_index]
            self.combination(initial, n-1, r-1, outer_index+1, inner_index+1, data, result)
            self.combination(initial, n-1, r, outer_index+1, inner_index, data, result)
    """
    EXAMPLE COMBINATION RUN THROUGH

    initial = [1, 2, 3, 4, 5]
    n = 5
    r = 3
    result = []
    data = [0, 0, 0]
    ([1, 2, 3, 4, 5], 5, 3, 0, 0, data, result)  
            -> [1, 0, 0], call(initial, 4, 2, 1, 1, [1, 0, 0], result)
            -> [1, 2, 0], call(initial, 3, 1, 2, 2, [1, 2, 0], result)
            -> [1, 2, 3], call(initial, 2, 1, 3, 2, [1, 2, 3], result)
            -> [1, 2, 4], call(initial, 1, 1, 4, 2, [1, 2, 4], result)
            -> [1, 2, 5],...
    """

    def permutation(self, array, first, last, result):
        if first == last: #Base case 0: end of array reached
            temp = array.copy()
            if (self.is_valid(self.operands, self.result, self.letters, temp)):      
                result.append(temp)
            return
        else: #Recursion
            for i in range(first, last):
                array[first], array[i] = array[i], array[first]
                self.permutation(array, first+1, last, result)
                array[first], array[i] = array[i], array[first]

    def get_answers(self):
        for i in range(len(self.operands)):
            print("word", i+1, ": ", self.operands[i])
        print("result: " + self.result)
        for p in self.valid_results:
            if (self.check(self.operands, self.result, p)):
                print(p)
                to_be_added = []
                for i in range(len(self.operands)):
                    to_be_added.append(str(self.word2num(self.operands[i], self.letters, p)))
                    print(self.word2num(self.operands[i], self.letters, p))
                to_be_added.append(str(self.word2num(self.result, self.letters, p)))
                print(self.word2num(self.result, self.letters, p))
                self.final_results.append(to_be_added)
