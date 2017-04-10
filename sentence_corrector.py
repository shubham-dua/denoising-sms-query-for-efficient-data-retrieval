import enchant
d = enchant.DictWithPWL("en_US")
d1 = enchant.request_pwl_dict("faq_words.txt")

h = open("faq_words.txt", "r")
r = h.read()
y = r.split()
dic = {}
n =1

length = len(y)
output_list = []



##############FUNCTION TO CALCULATE LONGEST COMMON SUBSEQENCE#################

def lcs(X, Y, m, n):
    L = [[0 for x in xrange(n+1)] for x in xrange(m+1)]
 
    # Following steps build L[m+1][n+1] in bottom up fashion. Note
    # that L[i][j] contains length of LCS of X[0..i-1] and Y[0..j-1] 
    for i in xrange(m+1):
        for j in xrange(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
 
    # Following code is used to print LCS
    index = L[m][n]
 
    # Create a character array to store the lcs string
    lcs = [""] * (index+1)
    lcs[index] = "\0"
 
    # Start from the right-most-bottom-most corner and
    # one by one store characters in lcs[]
    i = m
    j = n
    while i > 0 and j > 0:
 
        # If current character in X[] and Y are same, then
        # current character is part of LCS
        if X[i-1] == Y[j-1]:
            lcs[index-1] = X[i-1]
            i-=1
            j-=1
            index-=1
 
        # If not same, then find the larger of two and
        # go in the direction of larger value
        elif L[i-1][j] > L[i][j-1]:
            i-=1
        else:
            j-=1
 
    #print "LCS of " + X + " and " + Y + " is " + "".join(lcs)
    #RETURN LENGTH OF LCS
            
    l = "".join(lcs)
    length_lcs = len(l) - 1
    return length_lcs




###########   FUNCTION TO CALCULATE REFERENCE DICTIONARY ##########
def freq():
    global dic, n, y
    for i in y:
        i.lower()
        if (i[-1] == "?") or (i[-1] ==  "!") or (i[-1] ==  "'") or (i[-1] ==  '"') or (i[-1] ==  ",") or (i[-1] ==  "."):
            i = i[:-1]
            
        if i not in dic.keys():
            dic.update({i:n})

        else:
            dic[i] = dic[i] + 1

flag = False


####################FUNCTION TO CALCULATE LCS LIST OF WORDS######################
def lcs_func():
    global flag
    flag = True
    global length, dic, sugg, output_list, words
    lcs_words = []
    lcs_length_list = []
    for word in sugg:
        if word in dic.keys():
            lcs_words.append(word)
            l = lcs(word, words, len(word), len(words))
            lcs_length_list.append(l)
    #mx1 = max(lcs_length_list)
    mx = lcs_length_list.index( max(lcs_length_list))

    #####################test code####################




    ####################################################
    output_list.append(lcs_words[mx])




def start():
    global inp
    inp1 = raw_input("Enter your Query:\n")
    inp = inp1.split()
    freq()
    #print inp

start()

    
########### RECURSIVELY CHECK FOR EACH WORD IN INPUT ############
for words in inp:
    m = []
    if d.check(words) == False or d1.check(words) == False:
        sugg = d.suggest(words) + d1.suggest(words)
        lcs_func()
    else:
        output_list.append(words)

op = ""
if flag == True:
    print "Did You Mean?"
for w in output_list:
    op = op + w + " "
print op





#############################          TOKENIZER        ###############################
handler = open("stop_words.txt", "r")
read = handler.read()
reader = read.split()

token_list = []

for wrds in output_list:
    if wrds not in reader:
        token_list.append(wrds)
print token_list
