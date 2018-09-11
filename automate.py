import surprisal
import lexicon_generator
import random

#Semiuseful notes:
#unigram freq lookup is case insensitive because those dicts have everything converted to lowercase already
#probably should use normal case for surprisal
#will need to deal with reparsing punctuation for everything at some point

UNIGRAM_FREQ=lexicon_generator.load_dict('uni.p')
LEXICON=lexicon_generator.load_dict('test.p')

def get_surprisal(context, word):
    '''get in-context surprisal of word'''
    return (surprisal.Context_Surprisal(context+" "+word))

def get_unigram_freq(word):
    freq=UNIGRAM_FREQ.get(word.lower())
    if freq!=None:
        return freq
    else:
        print (word+" is not in dictionary")


def get_alternates(word):
    alts=LEXICON.get((len(word),get_unigram_freq(word)))
    if alts==None:
        print (word+" does not have alternates")
    else:
        return alts

def check_badness(context, word, alt):
    baseline_surp = get_surprisal(context, word)
    baseline_freq = get_unigram_freq(word)
    alt_surp = get_surprisal(context, alt)
    alt_freq = get_unigram_freq(alt)
    return([baseline_surp, alt_surp, baseline_freq, alt_freq])
        
def test_alternates(context, word):
    alts =get_alternates(word)
    good=get_surprisal(context,word)
    to_return=[[word,good]]
    used_so_far=[]
    for i in range(10):
        alt=random.choice(alts)
        if alt not in used_so_far:
            alt_surp=get_surprisal(context, alt)
            to_return.append([alt, alt_surp])
            used_so_far.append(alt)
    return(to_return)

#test surprisal on some of their examples to get a baseline for how bad is bad

#and then see how much I need to try to get something that bad?

def do_stuff():
    a=test_alternates("The", "reporter")
    b=test_alternates("The reporter", "had")
    c=test_alternates("The reporter had", "dinner")
    d=test_alternates("The reporter had dinner", "yesterday")
    e=test_alternates("The reporter had dinner yesterday", "with")
    f=test_alternates("The reporter had dinner yesterday with", "the")
    g=test_alternates("The reporter had dinner yesterday with the", "baseball")
    h=test_alternates("The reporter had dinner yesterday with the baseball", "player")
    i=test_alternates("The reporter had dinner yesterday with the baseball player", "who")
    j=test_alternates("The reporter had dinner yesterday with the baseball player who", "Kevin")
    k=test_alternates("The reporter had dinner yesterday with the baseball player who Kevin", "admired")
    print([a,b,c,d,e,f,g,h,i,j,k])

def do_stuff_2():
    a= check_badness("The","reporter", "admired")
    b= check_badness("The reporter", "had", "are")
    c= check_badness("The reporter had", "dinner", "save")
    d= check_badness("The reporter had dinner","yesterday", "myself")
    e= check_badness("The reporter had dinner yesterday","with", "tank")
    f= check_badness("The reporter had dinner yesterday with", "the", "go")
    g= check_badness("The reporter had dinner yesterday with the", "baseball", "take")
    h= check_badness("The reporter had dinner yesterday with the baseball","player", "pose")
    i= check_badness("The reporter had dinner yesterday with the baseball player","who", "speak")
    j= check_badness("The reporter had dinner yesterday with the baseball player who","Kevin", "body")
    k= check_badness("The reporter had dinner yesterday with the baseball player who Kevin","admired", "guys")
    print([a,b,c,d,e,f,g,h,i,j,k])
def check_lexicon():
    for key in sorted(LEXICON):
        if len(LEXICON[key])<10:
            print(key,LEXICON[key])


do_stuff_2()