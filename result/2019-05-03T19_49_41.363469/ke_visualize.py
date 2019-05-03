import matplotlib
matplotlib.use('Agg')
import pickle
import matplotlib.pyplot as plt
fileName='0_1.pickle'
with open ('0_1.pickle','rb') as f:
    thaw=pickle.load(f)
    vol1=thaw['results']['r_v_list'][0][1]
    vol2=thaw['results']['r_v_list'][1][1]
    t=thaw['results']['t']
    plt.plot(t,vol1)
#    plt.plot(t,vol2)
    plt.savefig('result.png')
