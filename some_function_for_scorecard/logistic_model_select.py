

# 向前法
import statsmodels.formula.api as smf
import statsmodels.api as sm
def forward_select(data, response):
    """
    General Linear model forward selection.

    Parameters:
    -----------
    data : pandas DataFrame with all possible predictors and response

    response: string, name of response column in data

    Returns:
    --------
    model: an "optimal" fitted statsmodels general linear model
           selected by forward selection
           evaluated by bic
    """
    remaining = set(data.columns)
    remaining.remove(response)
    selected = []
    current_score, best_new_score = float('inf'), float('inf')
    while remaining:
        bic_with_candidates=[]
        for candidate in remaining:
            formula = "{} ~ {}".format(
                response,' + '.join(selected + [candidate]))
            bic = smf.glm(
                formula=formula, data=data, 
                family=sm.families.Binomial(sm.families.links.logit)
            ).fit().bic
            bic_with_candidates.append((bic, candidate))
        bic_with_candidates.sort(reverse=True)
        best_new_score, best_candidate=bic_with_candidates.pop()
        if current_score > best_new_score: 
            remaining.remove(best_candidate)
            selected.append(best_candidate)
            current_score = best_new_score
            print ('bic is {},continuing!'.format(current_score))
        else:        
            print ('forward selection over!')
            break
            
    formula = "{} ~ {} ".format(response,' + '.join(selected))
    print('final formula is {}'.format(formula))
    model = smf.glm(
        formula=formula, data=data, 
        family=sm.families.Binomial(sm.families.links.logit)
    ).fit()
    return(model)
    
# backward selection
import statsmodels.formula.api as smf
import statsmodels.api as sm
def backward_select(data, response):
    """
    General Linear model forward selection.

    Parameters:
    -----------
    data : pandas DataFrame with all possible predictors and response

    response: string, name of response column in data

    Returns:
    --------
    model: an "optimal" fitted statsmodels general linear model
           selected by backward selection
           evaluated by bic
    """
    remaining = set(data.columns)
    remaining.remove(response)
    selected = remaining
    formula = "{} ~ {}".format(
                response,' + '.join(selected))
    current_score =smf.glm(
                formula=formula, data=data, 
                family=sm.families.Binomial(sm.families.links.logit)
            ).fit().bic
    best_new_score = current_score
    
    while remaining:
        bic_with_candidates=[(best_new_score, '')]
        for candidate in remaining:
            selected = remaining.copy()
            selected.remove(candidate)
            formula = "{} ~ {}".format(
                response,' + '.join(selected))
            bic = smf.glm(
                formula=formula, data=data, 
                family=sm.families.Binomial(sm.families.links.logit)
            ).fit().bic
            bic_with_candidates.append((bic, candidate))
        bic_with_candidates.sort(reverse=True)
        best_new_score, best_candidate=bic_with_candidates.pop()
        if current_score > best_new_score: 
            remaining.remove(best_candidate)
            #selected.append(best_candidate)
            current_score = best_new_score
            print ('bic is {},continuing!'.format(current_score))
        else:        
            print ('backward selection over!')
            break
            
    formula = "{} ~ {} ".format(response,' + '.join(selected))
    print('final formula is {}'.format(formula))
    model = smf.glm(
        formula=formula, data=data, 
        family=sm.families.Binomial(sm.families.links.logit)
    ).fit()
    return(model)

# 逐步法
import statsmodels.formula.api as smf
import statsmodels.api as sm
def stepwise_select(data, response):
    """
    General Linear model stepwise selection.
    Dependent on backward_select function

    Parameters:
    -----------
    data : pandas DataFrame with all possible predictors and response

    response: string, name of response column in data

    Returns:
    --------
    model: an "optimal" fitted statsmodels general linear model
           selected by stepwise selection
           evaluated by bic
    """
    remaining = set(data.columns)
    remaining.remove(response)
    selected = []
    current_score, best_new_score = float('inf'), float('inf')
    while remaining:
        bic_with_candidates = []
        for candidate in remaining:
            formula = "{} ~ {}".format(
                response, ' + '.join(selected + [candidate]))
            bic = smf.glm(
                formula=formula, data=data,
                family=sm.families.Binomial(sm.families.links.logit)
            ).fit().bic
            bic_with_candidates.append((bic, candidate))
        bic_with_candidates.sort(reverse=True)
        best_new_score, best_candidate = bic_with_candidates.pop()
        if current_score > best_new_score:
            remaining.remove(best_candidate)
            selected.append(best_candidate)
            current_score = best_new_score
            print('{} added,bic is {},forward-continuing!'.format(best_candidate,current_score))



            while selected:
                bic_with_candidates = [(best_new_score, '')]
                if len(selected) == 1:
                    print("selected")
                    break
                for candidate in selected:
                    back_selected = selected.copy()
                    back_selected.remove(candidate)
                    formula = "{} ~ {}".format(
                        response, ' + '.join(back_selected))
                    bic = smf.glm(
                        formula=formula, data=data,
                        family=sm.families.Binomial(sm.families.links.logit)
                    ).fit().bic
                    bic_with_candidates.append((bic, candidate))
                bic_with_candidates.sort(reverse=True)
                best_new_score, best_candidate = bic_with_candidates.pop()
                if current_score > best_new_score:
                    selected.remove(best_candidate)
                    # selected.append(best_candidate)
                    current_score = best_new_score
                    print('{} removed,bic is {},backward-continuing!'.format(best_candidate,current_score))
                else:
                    print('backward selection over!')
                    break


        else:
            print('forward selection over!')
            break

    formula = "{} ~ {} ".format(response, ' + '.join(selected))
    print('final formula is {}'.format(formula))
    model = smf.glm(
        formula=formula, data=data,
        family=sm.families.Binomial(sm.families.links.logit)
    ).fit()
    return (model)
    
    
