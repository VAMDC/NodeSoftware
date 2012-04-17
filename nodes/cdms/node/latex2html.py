import re

translation_dict = {'\\Sigma':'&Sigma;',
                    '\\Delta':'&Delta;',
                    '\\Pi':'&Pi;',
                    '\\mu':'&mu;',
                    '\\nu':'&nu;',
                    }

def parse_mathmode(string):

    # find brackets
    reg_brackets = re.compile('{[^}]*}')
    in_brackets = reg_brackets.findall(string)
    before_brackets = reg_brackets.split(string)
    
    # number of elements in in_brackets has to be leq than in before_brackets

    i = 0
    for ib in in_brackets:
        try:
            if before_brackets[i][-1]=='^':
                # remove last string and attach it to the string within brackets
                before_brackets[i]=before_brackets[i][:-1]+"<sup>%s</sup>" % ib[1:-1]
            
            elif before_brackets[i][-1]=='_':
                # remove last string and attach it to the string within brackets
                before_brackets[i]=before_brackets[i][:-1]+"<sub>%s</sub>" % ib[1:-1]

            else:
                before_brackets[i]=before_brackets[i][:-1]+"%s" % ib[1:-1]
                            
        except:
            pass

        i+=1

    ret_string = ''.join(before_brackets)
    
    # find underscores
    ret_string = parse_cmd(ret_string,'\_')
    
    # find ^'s
    ret_string = parse_cmd(ret_string,'\^')
    
    return ret_string
                

def parse_cmd(string,cmd):
    cmds = {'\^':['<sup>','</sup>'], '\_':['<sub>','</sub>']}

    if cmd not in cmds.keys():
        return string 
    
    expr = re.compile(cmd)

    found = expr.search(string)
    
    while found:
        start = found.start()
        string='%s%s%s%s%s' % (string[:start], cmds[cmd][0],string[start+1], cmds[cmd][1],string[start+2:])
        found = expr.search(string)

    return string


def latex2html(string):

    # find mathmode
    
    strings = string.split('$')
    # odd elements are encapsulated in math mode

    for i in xrange(len(strings)):
        if i % 2 == 1:
            strings[i] = parse_mathmode(strings[i])


    # combine everything

    ret_string = ''.join(strings)

    for letter in translation_dict:
        ret_string = ret_string.replace(letter,translation_dict[letter])

    return ret_string
