from tqdm import tqdm
import numpy as np

def code_to_diff(n, params, scale):
    res = np.zeros(len(params))
    idx = 0
    while n > 0:
        if n & 1:
            res[idx] = 1 if n & 2 else -1
        elif n & 2:
            return None 
        n >>= 2
        idx += 1
    res *= scale
    return res

print('grid sig: def grid(nb, df, params, weights, scale, disp=True):')

def grid(nb, df, params, weights, scale, disp=True):
    init_score = nb.test(df, params, weights, report=False)
    top_score = init_score
    top_weights = np.copy(weights)
   
    lst = range(4 ** len(params))
    if disp:
        lst = tqdm(lst)

    for i in lst:
        diff = code_to_diff(i, params, scale)
        if diff is None:
            continue
        score = nb.test(df, params, weights + diff, report=False)
        if score > top_score:
            top_score = score
            top_weights = np.copy(weights + diff)
    if disp:
        print(f'score after: {top_score}')
        if init_score == top_score:
            print('no improvement ;-;')
    return top_score, top_weights, top_score > init_score

print('igs sig: def iterated_gs(nb, df, params, weights, scale, max_iter=100, save_file=None, disp=True):')

def iterated_gs(nb, df, params, weights, scale=.1, max_iter=100, save_file=None, disp=True):
    score = nb.test(df, params, weights, report=False)
    improving = True
    iters = 0
    desperate = [0.05, 0.2, 0.3, 0.5, 1]
    while improving and iters < max_iter:
        score, weights, improving = grid(nb, df, params, weights, scale, disp)
        if not improving:
            for pls in desperate:
                score, weights, improving = grid(nb, df, params, weights, pls, disp)
                if improving:
                    break
        iters += 1
    print(score)
    if save_file is not None:
        np.save(save_file, weights)
