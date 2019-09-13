import pyparsing

from pyparsing import OneOrMore, nestedExpr

import itertools, json, string, re

POODLE_SPLIT_MATH_LOCK_PREDICATE_NAME = "poodle-split-math-not-in-progress"

def list_to_lisp(v):
    if hasattr(v,"asList"): v=v.asList()
    if not "(" in repr(v):
        return repr(v).replace("[","(").replace("]",")").replace("'","").replace(",","")\
        .replace("\"","").replace(" {}","")#.replace("((","(").replace("))",")")
    else:
        return v

# class ListLike(list):
#     def asList(self):
#         return self

def lisp_to_list(v):
    return OneOrMore(nestedExpr()).parseString(v).asList()

filt = re.compile("^"+string.ascii_letters+string.digits+"-_:=")
transr = re.compile("([^\\[^\\]^\s]+)")

def lisp_to_list_fast(v):
    return [eval(",".join(transr.sub(r'"\1"' ,filt.sub('',v).replace("(","[").replace(")","]")).split()))]

lisp_to_list = lisp_to_list_fast

#look for list of list recursively for var
def containVar(someList, var):
    # print("check list ", someList, " some var ", var, "type ", type(someList))
    ret = False
    if isinstance(someList, list) or isinstance(someList, pyparsing.ParseResults):
        # print("is list")
        for v in someList:
            if containVar(v, var):
                return True
    else:
        # if someList == var: print("catch ", var)
        return someList == var
    return ret

def getVars(someList):
    ret = []
    if isinstance(someList, list) or isinstance(someList, pyparsing.ParseResults):
        for v in someList:
            ret.extend(getVars(v))
    else:
        if "?" in someList:
            ret.append(someList)
    return ret

class ActionStruct():
    def __init__(self, name):
        self.name = name
        self.cost = 1
        self.parameters = []
        self.precondition = []
        self.effect = []
        self.preconditionPrepend = []
        self.effectAppend = []
    
    def hasPreconditionVariable(self, var):
        if var in repr(self.precondition):
            return True
        return False

    def haveVariable(self, var):
        # print("check for ", var)
        if containVar(self.precondition, var):
            return True
        if containVar(self.effect, var):
            return True
        return False
   
    def __str__(self):
        precondition = [list_to_lisp(pc) for pc in self.preconditionPrepend]
        precondition.extend([list_to_lisp(pc) for pc in self.precondition]) 
        effects = [list_to_lisp(pc) for pc in self.effect]
        effects.extend([list_to_lisp(pc) for pc in self.effectAppend])
        parameters = [list_to_lisp(pc) for pc in self.parameters]
        return """
    (:action {action_name}
        :parameters ({parameters})
        :precondition (and
            {precondition}
        )
        :effect (and
            {effect}
            {cost}
        )
    )
            """.format(action_name = self.name,
                parameters=' '.join(parameters),
                precondition='\n            '.join(precondition),
                effect='\n            '.join(effects),
                cost='(increase (total-cost) {0})'.format(self.cost)
            )

def extractTypeFromVariableName(varn):
    sp = varn.replace("?","").split("-")
    if len(sp) == 2:
        return sp[0]
    return sp[1]

class ActionSplitter():

    def __init__(self, pddl_text, cutBy = 'SumResult-result'):
        self.pddl_text = pddl_text
        self.cutBy = cutBy
        self.splitted_actions = []
    
    def fix_problem(self, problem_file):
        l_problem = lisp_to_list(problem_file)
        for b in l_problem[0]:
            if b[0] == ":init":
                initSection = b
            if b[0] == ":goal":
                goalSection = b[1]
        initSection.append([POODLE_SPLIT_MATH_LOCK_PREDICATE_NAME])
        goalSection.append([POODLE_SPLIT_MATH_LOCK_PREDICATE_NAME])
        return list_to_lisp(l_problem[0])
        

    
    def split(self):
        data = lisp_to_list(self.pddl_text)  #OneOrMore(nestedExpr()).parseString(self.pddl_text)
        #print(data[0])
        #def actions
        action = {}

        predicateList = []

        allGeneratedExports = []

        for a in data[0]:
            if a[0] == ':action':
                action[a[1]] = ActionStruct(a[1])
                for idx, val in enumerate(a):
                    if val == ':precondition':
                        if a[idx+1][0] == 'and':
                            action[a[1]].precondition = a[idx+1][1:len(a[idx+1])] # cut AND
                        else :
                            action[a[1]].precondition = a[idx+1]
                    if val == ':effect':
                        if a[idx+1][0] == 'and':
                            action[a[1]].effect = a[idx+1][1:len(a[idx+1])] #cut And
                        else:
                            action[a[1]].effect = a[idx+1]
                        action[a[1]].cost = action[a[1]].effect[len(action[a[1]].effect)-1][2]
                        action[a[1]].effect.remove(action[a[1]].effect[len(action[a[1]].effect)-1])
                    if val == ':parameters':
                        action[a[1]].parameters = a[idx+1] #cut And
            if a[0] == ":predicates":
                for p in list(a)[1:]:
                    predicateList.append(p)


        #look for splittable action
        splittableAction = {}
        for a in action:
            # print(a, ": ", action[a].precondition,'\n')
            splitMe = 0
            for p in action[a].precondition:
                if p[0] == self.cutBy: 
                    splitMe += 1 #split if 2 or more SumResult-result in precondition
            if splitMe > 1:
                splittableAction[a] = action[a]

        # I split action on small actions which I named slices or slice of action
        # print("splittable: \n")
        self.all_actions = action.copy()
        for sa in splittableAction:
            del action[sa]

        unsplittableAction = action
        action = splittableAction
        splittedAction = {}
        #sliceOfAction = ActionStruct()
        #split actions
        for a in action:
            # print(a, ": ", action[a].precondition,'\n')
            tmpAction = action[a]
            splittedAction[a] = {}
            counter=0
            sliceOfAction = ActionStruct("{0}-{1}".format(a, counter))
            for p in tmpAction.precondition:
                # print("sliceOfAction \n\n", sliceOfAction)
                sliceOfAction.precondition.append(p)
                # print("splittedAction ",splittedAction[a])
                # print("precondition ->>", p)
                if p[0] == self.cutBy:
                    # print("precondition catch ->>", p)
                    splittedAction[a]["{0}-{1}".format(a, counter)] = sliceOfAction
                    # print("slice\n", "{0}-{1}".format(a, counter), ": ", sliceOfAction)
                    counter += 1
                    sliceOfAction = ActionStruct("{0}-{1}".format(a, counter))
            counter -= 1
        #    print("slice\n", "{0}-{1}".format(a, counter), ": ", sliceOfAction)
            splittedAction[a]["{0}-{1}".format(a, counter)].precondition.extend(sliceOfAction.precondition)
            cost = int(tmpAction.cost) - (len(splittedAction[a]) - 1)
            if cost < 1:
                cost = 1
            for s in splittedAction[a]:
                splittedAction[a][s].cost = str(int(cost))
                # Only first action has calculated cost another just 1
                if cost != 1:
                    cost = 1

        #generate snakable useful for next step variables
        for a in splittedAction:
            arr = [] #load into list
            for s in splittedAction[a]:
                arr.append(splittedAction[a][s])
            parameters = action[a].parameters
            effect = action[a].effect
            # print(parameters)
            # print("full effect ",  effect)
            consumedEffects = []
            # do effect in last slice with coresponding variable
            for idx, slice in reversed(list(enumerate(arr))):
                for pIdx, eff in enumerate(effect):
                    useFullEffect = False
                    # print("eff ", eff, " vars only ", getVars(eff))

                    for par in getVars(eff):
                        if containVar(slice.precondition, par):
                            useFullEffect = True
                            break
                    if useFullEffect :
                        if eff not in consumedEffects:
                            # print("effect ", eff , "add to ", slice.name)
                            consumedEffects.append(eff)
                            slice.effect.append(eff)
            loopCondition = True
            while loopCondition:
                loopCondition = False
                for idx, slice in enumerate(arr):
                    maxEffectAmount = 2
                    # if slice.name != 'StartPod-5': continue
                    if len(slice.effect) > maxEffectAmount:
                        loopCondition = True
                        lenght = len(slice.effect)
                        sAmount = lenght / maxEffectAmount if lenght % maxEffectAmount == 0 else (lenght / maxEffectAmount) + 1
                        sumResultArg = None
                        for precond100 in slice.precondition:
                            if precond100[0] == 'SumResult-result':
                                sumResultArg = precond100[2]
                                break
                        for count in range(1, int(sAmount)):
                            ac = ActionStruct("{0}-{1}-{2}".format(a, idx, count))
                            startFrom = 0
                            for subCounter in range(maxEffectAmount):
                                if len(slice.effect) == startFrom : break
                                if containVar(slice.effect[startFrom], sumResultArg) : 
                                    startFrom += 1
                                ac.effect.append(slice.effect[startFrom])
                                del(slice.effect[startFrom])
                            arr.insert(idx+count, ac)
                            splittedAction[a][ac.name] = ac
                        if loopCondition: break


            #fill correct parameters
            for idx, slice in enumerate(arr):
                for pIdx, par in enumerate(parameters): #iterate full list of action's parameters
                    if pIdx % 3 == 0:
                        # print("check parameter ", par)
                        if slice.haveVariable(par):
                            # print("ok")
                            slice.parameters.append(parameters[pIdx])     # variable
                            slice.parameters.append(parameters[pIdx+1])   # -
                            slice.parameters.append(parameters[pIdx+2])   # type
                # print(slice)
            
            # export usefull parameters(variables) for next sliced action sequence
            for idx, slice in enumerate(arr):
                # print(slice.name,"has parameters", repr(slice.parameters))
                if (idx + 1) == len(arr): break
                arrNext = arr[idx+1:len(arr)]
                for idxNext, sliceNext in enumerate(arrNext):
                    # print("exported-{0}-{1}-{2}".format(a, idx, 1+idx+idxNext))
                    sliceEffectAppend =            ["exported-{0}-{1}-{2}".format(a, idx, 1+idx+idxNext)]             # predicate
                    sliceNextPreconditionPrepend = ["exported-{0}-{1}-{2}".format(a, idx, 1+idx+idxNext)]  # predicate
                    predicateDeclaration =         ["exported-{0}-{1}-{2}".format(a, idx, 1+idx+idxNext)]
                    for pIdx, par in enumerate(slice.parameters): #iterate list of slice's parameters and export(in effect) and import in next slice
                        if not "?" in par: continue
                        if sliceNext.haveVariable(par):
                            # print(slice.name, "has param", par)
                            predicateDeclaration.append("?var{0}".format(len(predicateDeclaration))) # variable
                            predicateDeclaration.append("-")
                            predicateDeclaration.append(extractTypeFromVariableName(par)) # type
                            sliceEffectAppend.append(par)                # variable
                            sliceNextPreconditionPrepend.append(par)     # variable
                    # skip blank predicates
                    if len(predicateDeclaration) == 1 and idxNext != 0:
                        continue
                    cont = False
                    #skip duplicates
                    for effA in slice.effectAppend:
                        if isinstance(effA, list):
                            if effA[1:] == sliceEffectAppend[1:]:
                                tmplist = []
                                tmplist.append(effA[0])
                                tmplist.extend(sliceEffectAppend[1:])
                                sliceNext.preconditionPrepend.append(tmplist)      # full predicate
                                notP = "(not %s)" % list_to_lisp(tmplist)
                                # delete duplicated (not %s ) from history
                                for ggSlice in arr[0:1+idx+idxNext]:
                                    for eA in ggSlice.effectAppend:
                                        # print(eA, " == ", notP)
                                        if eA == notP:
                                            # print("ok")
                                            ggSlice.effectAppend.remove(eA)
                                sliceNext.effectAppend.append(notP)
                                cont = True
                    if cont :
                        continue
                    predicateList.append(predicateDeclaration)
                    # print("adding line", sliceEffectAppend, "to", slice.name)
                    slice.effectAppend.append(sliceEffectAppend)                            # full predicate
                    sliceNext.preconditionPrepend.append(sliceNextPreconditionPrepend)      # full predicate   
                    sliceNext.effectAppend.append("(not %s)" % list_to_lisp(sliceNextPreconditionPrepend))
                    allGeneratedExports.append(sliceNextPreconditionPrepend)         
            
            # close the snake first with last
            wa = ["working-{0}".format(a)]
            arr[0].effectAppend.append(wa)
            arr[0].effectAppend.append(f"(not ({POODLE_SPLIT_MATH_LOCK_PREDICATE_NAME}))")
            arr[0].preconditionPrepend.append("(not %s)" % list_to_lisp(wa))
            arr[0].preconditionPrepend.append(f"({POODLE_SPLIT_MATH_LOCK_PREDICATE_NAME})")
            arr[len(arr)-1].effectAppend.append("(not %s)" % list_to_lisp(wa))
            arr[-1].effectAppend.append(f"({POODLE_SPLIT_MATH_LOCK_PREDICATE_NAME})")
            predicateList.append(wa)



            # for s in splittedAction[a]:
                # print(splittedAction[a][s])
        # for ex in set([list_to_lisp(x) for x in allGeneratedExports]):
        #     splittedAction[a][s].effect.append("(not %s)" % ex)
        # print("LAST:",s)

        # for ua in unsplittableAction:
            # print(unsplittableAction[ua])
        predicateList.append(f"({POODLE_SPLIT_MATH_LOCK_PREDICATE_NAME})")
        all_predicates_gen = "(:predicates {0})".format('\n            '.join([list_to_lisp(pc) for pc in predicateList]))

        # print("-------")

        # for a,v in splittedAction.items():
        #     print(a, v)
        #     if len(v) > 2:
        #         print(list(v.values())[-1])

        ldata = data # .asList()

        self.splitted_actions = splittedAction

        combined_actions = []
        for an in self.all_actions:
            # print(an)
            if an in splittedAction:
                combined_actions += [str(x) for x in splittedAction[an].values()]
            else: 
                # TODO HERE: append to every precondition (not (poodle-split-math-in-progress))
                if len(splittedAction): self.all_actions[an].precondition.insert(0,f"({POODLE_SPLIT_MATH_LOCK_PREDICATE_NAME})")
                combined_actions.append(str(self.all_actions[an]))

        domainStr = \
        """(define (domain {dom_name})
            
            {orig_requirements}
            
            {orig_types}

            {predicates}

            (:functions
                (total-cost)
            )

            {actions}
        )
        """.format(
            dom_name=ldata[0][1][1],
            orig_requirements=list_to_lisp(ldata[0][2]),
            orig_types=list_to_lisp(ldata[0][3]),
            predicates=all_predicates_gen,
            actions='\n'.join(combined_actions)
        )
        return domainStr
    
    def unsplit_plan(self, plan_split):
        loAllActions = {k.lower():v for k,v in self.all_actions.items()}
        loSplitActions = {k2.lower():v2 for k2,v2 in ({k: v for d in self.splitted_actions.values() for k, v in d.items()}).items()}
        lplan = [p.replace("(","").replace(")","").split() \
            for p in plan_split.split("\n") if not p.startswith(";")]
        if not lplan: 
            print("NO PLAN")
            return plan_split
        if not lplan[0]: 
            print("NO PLAN 2")
            return plan_split
        us_plan = []
        params = {}
        collecting_action = ""
        action_num = 9999999999
        for plannedAct in lplan:
            if plannedAct: 
                print("PLANNED_ACT", plannedAct)
                action_name_lower = plannedAct[0]
                objectNames = plannedAct[1:]
                if action_name_lower in loSplitActions:
                    action_num = int(action_name_lower.split("-")[-1])
                else:
                    action_num = -1
            if (action_num < 1 or not plannedAct) and len(params) != 0:
                orig_action_name = '-'.join(collecting_action.split("-")[:-1])
                unsplit_action_p = [orig_action_name]
                for p in loAllActions[orig_action_name].parameters:
                    if not p.startswith("?"): continue
                    unsplit_action_p.append(params.get(p, null_object_from_param(p)))
                us_plan.append(unsplit_action_p)
                params = {}
            if plannedAct and action_name_lower in loSplitActions:
                if action_num == 0 and len(params) != 0: raise AssertionError(f"pa: {plannedAct} anl: {action_name_lower} an: {action_num} -- p: {params}")
                if not len(params): collecting_action = action_name_lower
                params.update(dict(zip([x for x in loSplitActions[action_name_lower].parameters if x.startswith("?")],objectNames)))
            else:
                if plannedAct: us_plan.append(plannedAct)
        return "".join(["%s\n"%list_to_lisp(p) for p in us_plan])

def null_object_from_param(p):
    cls = p.replace("?","").split("-")[0]
    assert not "?" in cls and not "-" in cls
    nullobjName = "p-null-%s" % cls
    return nullobjName







if __name__ == "__main__":
    pddl_text = open("./test/domain.pddl").read()
    open("./splitted_domain.pddl", "w+").write(ActionSplitter(pddl_text).split())




