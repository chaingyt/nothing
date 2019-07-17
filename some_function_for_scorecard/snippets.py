


def encode(df, col):
    """
    :param  df: DataFrame   
    :param col: columns name (like 'col_1')
    :return df: the result df with OneHotEncoding & LabelEncoding
    """
    from sklearn.preprocessing import LabelEncoder
    from sklearn.preprocessing import OneHotEncoder
    le = LabelEncoder()
    ohe = OneHotEncoder()
    col_le = col + "_encoded"
    df[col_le] =  le.fit_transform(df[col].astype(str))
    X = ohe.fit_transform(df[col_le].values.reshape(-1,1)).toarray()
    dfOneHot = pd.DataFrame(X, columns = [col + "_" + str(int(i)) for i in range(X.shape[1])])
    df = pd.concat([df, dfOneHot], axis = 1,join_axes=[df.index])
    return df
    


def binarization(df, col):
    """
    :binarization
    """
    import numpy as np
    col_le = col + "_tag"
    df[col_le] = np.where(df[col]>0, 1, 0)
    return df

def get_df(file):
    """
    :import big data through chunk
    """
    import pandas as pd
    chunks = []
    for chunk in  pd.read_csv(file, sep='\t', iterator=True, chunksize=1000000):
        chunks.append(chunk)
    df = pd.concat(chunks, axis= 0)
    del chunks
    return df

    

def lift_curve_(result):
    from scipy.stats import scoreatpercentile
    result.columns = ['target','proba']
    result_ = result.copy()
    proba_copy = result.proba.copy()
    for i in range(10):
        point1 = scoreatpercentile(result_.proba, i*(100/10))
        point2 = scoreatpercentile(result_.proba, (i+1)*(100/10))
        proba_copy[(result_.proba >= point1) & (result_.proba <= point2)] = ((i+1))
    result_['grade'] = proba_copy
    df_gain = result_.groupby(by=['grade'], sort=True).sum()/(len(result)/10)*100
    plt.plot(df_gain['target'], color='red')
    for xy in zip(df_gain['target'].reset_index().values):
        plt.annotate("%s" % round(xy[0][1],2), xy=xy[0], xytext=(-20, 10), textcoords='offset points') 
    plt.plot(df_gain.index,[sum(result['target'])*100.0/len(result['target'])]*len(df_gain.index), color='blue')
    plt.title('Lift Curve')
    plt.xlabel('Decile')
    plt.ylabel('Bad Rate (%)')
    plt.xticks([1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0])
    fig = plt.gcf()
    fig.set_size_inches(10,8)
    plt.savefig("train.png")
    plt.show()
    return df_gain