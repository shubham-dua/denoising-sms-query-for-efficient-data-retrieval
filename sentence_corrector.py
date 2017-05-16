while True:
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




    
    global inp
    inp1 = raw_input("Enter your Query:\n")
    inp = inp1.split()
    freq()
    #print inp
    if inp1 == "exit" or inp1 == "Exit" or inp1 == "EXIT":
        break
    
        
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
        pass
        print "\nDID YOU MEAN:"
    for w in output_list:
        op = op + w + " "
    print op.upper(), "\n"
    op.lower()

    print "============================================================================================================="



    #############################          TOKENIZER        ###############################
    handler = open("stop_words.txt", "r")
    read = handler.read()
    reader = read.split()

    token_list = []

    for wrds in output_list:
        if wrds not in reader:
            token_list.append(wrds.lower())
    #print token_list
    break

    ########################## INTEGRATING DATABASE ######################################

#print op
#print token_list

a = open("faq.txt")
b = a.read()
c = b.split("_")
questions = []
answers = []

for item in c:
    if c.index(item) % 2 == 0:
        questions.append(item)
    elif c.index(item) % 2 != 0:
        answers.append(item)

questions_tokens = []
lst = []

o = open("stop_words.txt")
p = o.read()
p1 = p.split()

for x in questions:
    y = x.split()
    for z in y:
        if z.lower() not in p1:
            lst.append(z)
    questions_tokens.append(lst)
    lst = []
############################ CLEANING QUESTION TOKENS ##############################

for t in questions_tokens:
    for u in t:
        indx1 = t.index(u)
        if u[-1] == "?" or u[-1] == "!" or u[-1] == "." or u[-1] == "," or u[-1] == "'" or u[-1] == '"':
            u = u[:-1]
            t[indx1] = u

########################### CONVERTING FAQ TOKENS TO LOWER CASE ####################

for t in questions_tokens:
    for u in t:
        inx = t.index(u)
        u = u.lower()
        t[inx] = u



##################################### MAIN POROCESSING #############################

rank_inc = 0
rank_list = [rank_inc] * len(questions)

for g in questions_tokens:
    for tokens in token_list:
        if tokens in g:
            idx = questions_tokens.index(g)
            rank_list[idx] += 1

############################### FOR GETTING RELEVENT QUESTIONS #############################


print "THESE ARE THE MOST MATCHING FAQS TO YOUR INPUT QUERY: \n"


#for y in questions_tokens: print y
#print rank_list
#print token_list

op_flag = 0

while True:
    op_flag += 1
    g = max(rank_list)
    idx1 = rank_list.index(g)
    if g >= 1:
        rank_list[idx1] = 0
    elif g < 1 and op_flag == 1:
        op_flag = 7
        print "SORRY!\nNo Questions Found In Database\nPlease search through another query"
        print "SAMPLE QUESTION: \n"
    else:
        op_flag = 7
    print questions[idx1]
    print answers[idx1], "\n\n"
    if op_flag >= 7:
        break

print "\n\nFOR MORE DETAILS ABOUT UDACITY VISIT OFFICIAL WEBSITE:\nwww.udacity.org\nYOU CAN ALSO DOWNLOAD THE OFFCIAL APP ON PLAYSTORE FOR ANDROID AND APPSTORE FOR IPHONE"
