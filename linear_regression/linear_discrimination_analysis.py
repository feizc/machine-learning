"""
  linear_discrimination_analysis
  线性判别分析
  费政聪
"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, discriminant_analysis,cross_validation

def load_data():
    '''
    加载用于分类问题的数据集

    '''
    iris=datasets.load_iris() # 使用 scikit-learn 自带的 iris 数据集
    X_train=iris.data
    y_train=iris.target
    return cross_validation.train_test_split(X_train, y_train,test_size=0.25,
		random_state=0,stratify=y_train)
def test_LinearDiscriminantAnalysis(*data):
    '''
    测试 LinearDiscriminantAnalysis 的用法

    '''
    X_train,X_test,y_train,y_test=data
    lda = discriminant_analysis.LinearDiscriminantAnalysis()
    lda.fit(X_train, y_train)
    print('Coefficients:%s, intercept %s'%(lda.coef_,lda.intercept_))
    print('Score: %.2f' % lda.score(X_test, y_test))
def plot_LDA(converted_X,y):
    '''
    绘制经过 LDA 转换后的数据

    '''
    from mpl_toolkits.mplot3d import Axes3D
    fig=plt.figure()
    ax=Axes3D(fig)
    colors='rgb'
    markers='o*s'
    for target,color,marker in zip([0,1,2],colors,markers):
        pos=(y==target).ravel()
        X=converted_X[pos,:]
        ax.scatter(X[:,0], X[:,1], X[:,2],color=color,marker=marker,
			label="Label %d"%target)
    ax.legend(loc="best")
    fig.suptitle("Iris After LDA")
    plt.show()
def run_plot_LDA():
    '''
    执行 plot_LDA 。其中数据集来自于 load_data() 函数

    '''
    X_train,X_test,y_train,y_test=load_data()
    X=np.vstack((X_train,X_test))
    Y=np.vstack((y_train.reshape(y_train.size,1),y_test.reshape(y_test.size,1)))
    lda = discriminant_analysis.LinearDiscriminantAnalysis()
    lda.fit(X, Y)
    converted_X=np.dot(X,np.transpose(lda.coef_))+lda.intercept_
    plot_LDA(converted_X,Y)
def test_LinearDiscriminantAnalysis_solver(*data):
    '''
    测试 LinearDiscriminantAnalysis 的预测性能随 solver 参数的影响

    '''
    X_train,X_test,y_train,y_test=data
    solvers=['svd','lsqr','eigen']
    for solver in solvers:
        if(solver=='svd'):
            lda = discriminant_analysis.LinearDiscriminantAnalysis(solver=solver)
        else:
            lda = discriminant_analysis.LinearDiscriminantAnalysis(solver=solver,
			shrinkage=None)
        lda.fit(X_train, y_train)
        print('Score at solver=%s: %.2f' %(solver, lda.score(X_test, y_test)))
def test_LinearDiscriminantAnalysis_shrinkage(*data):
    '''
    测试  LinearDiscriminantAnalysis 的预测性能随 shrinkage 参数的影响

    '''
    X_train,X_test,y_train,y_test=data
    shrinkages=np.linspace(0.0,1.0,num=20)
    scores=[]
    for shrinkage in shrinkages:
        lda = discriminant_analysis.LinearDiscriminantAnalysis(solver='lsqr',
			shrinkage=shrinkage)
        lda.fit(X_train, y_train)
        scores.append(lda.score(X_test, y_test))
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.plot(shrinkages,scores)
    ax.set_xlabel(r"shrinkage")
    ax.set_ylabel(r"score")
    ax.set_ylim(0,1.05)
    ax.set_title("LinearDiscriminantAnalysis")
    plt.show()

if __name__=='__main__':
    X_train,X_test,y_train,y_test=load_data() # 产生用于分类的数据集
    test_LinearDiscriminantAnalysis(X_train,X_test,y_train,y_test) # 调用 test_LinearDiscriminantAnalysis
    # run_plot_LDA() # 调用 run_plot_LDA
    # test_LinearDiscriminantAnalysis_solver(X_train,X_test,y_train,y_test) # 调用 test_LinearDiscriminantAnalysis_solver
    # test_LinearDiscriminantAnalysis_shrinkage(X_train,X_test,y_train,y_test) # 调用 test_LinearDiscriminantAnalysis_shrinkage