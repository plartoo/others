# REFS:
# https://stackoverflow.com/questions/20838887/dispatch-dictionary-but-pass-different-parameters-to-functions
# https://codereview.stackexchange.com/questions/7433/dictionary-based-dispatch-in-python-with-multiple-parameters
# https://python-3-patterns-idioms-test.readthedocs.io/en/latest/MultipleDispatching.html
# https://stackoverflow.com/questions/52858079/how-to-invoke-python-methods-using-a-dictionary/52858899
# The best one: http://drunkenpython.org/tag/dispatcher.html
# https://stackoverflow.com/questions/19075843/dispatch-a-class-method



def rule_1(datum, **kwargs):
    modified_datum = datum
    if datum['Reason1']:
        modified_datum['Result'] = 1 # always set 'Result' to 1 whenever 'Reason1' is True
    else:
        modified_datum['Result'] = 1 # always set 'Result' to 0 whenever 'Reason1' is False
    return modified_datum


def rule_2(datum, **kwargs):
    modified_datum = datum
    if type(datum['Reason2']) is str:
        modified_datum['Result'] = 1 # always set 'Result' to 1 whenever 'Reason2' is of type 'str'
    elif type(datum['Reason2']) is int:
        modified_datum['Result'] = 2 # always set 'Result' to 2 whenever 'Reason2' is of type 'int'
    else:
        modified_datum['Result'] = 0
    return modified_datum


def rule_3(datum, **kwargs):
    modified_datum = datum
    # https://stackoverflow.com/questions/5624912/kwargs-parsing-best-practice
    strr = kwargs.get('strr')
    if strr == 'override':
        return {'wahaha':'heheheh'}

    if type(datum['Reason2']) is str:
        modified_datum['Result'] = 1 # always set 'Result' to 1 whenever 'Reason2' is of type 'str'
    elif type(datum['Reason2']) is int:
        modified_datum['Result'] = 2 # always set 'Result' to 2 whenever 'Reason2' is of type 'int'
    else:
        modified_datum['Result'] = 0
    return modified_datum



data = [
{'Result': 1, 'Reason1': False, 'Reason2': 1},
{'Result': 0, 'Reason1': False, 'Reason2':'haha'},
{'Result': 0, 'Reason1': True, 'Reason2': 'hehe'},
{'Result': 0, 'Reason1': True, 'Reason2': 0},
]
# There can be 'rule_3', 'rule_4' and so on... Also, these rules may have different method signatures (that is, they may take in more than one input parameter)
rule_book = [rule_2, rule_1] # I want to apply rule_2 first and then rule_1

processed_data = []
for datum in data:
    for rule in rule_book:
	    processed_data.append(rule(datum))
print('haha')

import pdb
rule_book = [(rule_2,{}), (rule_1,), (rule_3,{'strr': 'override'})] # rule 3 will supercede the others
processed_data = []
for datum in data:
    for rule in rule_book:
        if len(rule) == 2:
            processed_data.append(rule[0](datum,**rule[1]))
        else:
            processed_data.append(rule[0](datum))
pdb.set_trace()
print('hehe')
