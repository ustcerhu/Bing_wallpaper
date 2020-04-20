import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#导入数据
housing=pd.read_csv('C:\\Users\\hu\\OneDrive\\Cal_data\\Github\\wuqiqing-ageron_handson-ml-master\\ageron_handson-ml\\datasets\\housing\\housing.csv')

#图像化看看数据基本特征
housing.hist(bins=50,figsize=(20,15))

# #创建测试集、训练集
# def split_train_test(data,test_ratio):
#     shuffled_indices=np.random.permutation(len(data))  #打乱随机排序的索引
#     test_set_size=int(len(data)*test_ratio)
#     test_indices=shuffled_indices[:test_set_size]  #获取随机打乱的对应比例前的数据集作为测试集
#     train_indices=shuffled_indices[test_set_size:]  #获取随机打乱的对应比例后的数据集作为训练集
#     return data.iloc[train_indices],data.iloc[test_indices]  #返测试集和训练集的数据
#
# train_set,test_set=split_train_test(housing,0.2)  #取20%作为训练集，80%作为测试集，这个方法的弊端是每次运行得到的数据集都不一样
#
# #换个方法产生测试集和数据集
# import hashlib
# def test_set_check(identifier,test_ratio,hash):
#     return hash(np.int64(identifier)).digest()[-1]<256*test_ratio
# def split_train_set_by_id(data,test_ratio,id_column,hash=hashlib.md5):
#     ids=data[id_column]
#     in_test_set=ids.apply(lambda id_:test_set_check(id_,test_ratio,hash))
#     return data.loc[~in_test_set],data.loc[in_test_set]
# housing_with_id=housing.reset_index()
# train_set,test_set=split_train_set_by_id(housing_with_id,0.2,'index')
# housing_with_id['id']=housing['longitude']*1000+housing['latitude']
# train_set,test_set=split_train_set_by_id(housing_with_id,0.2,'id')


#利用sklearn的自带方法更加简便获取测试机和训练集
# from sklearn.model_selection import train_test_split
# train_set,test_set=train_test_split(housing,test_size=0.2,random_state=42)  #random_state=42相当于我们第一种方法中将随机数生成的种子固定，这样不会每次运行都得到不同的随机数组合

#分层取样实践，既要分层，又进行集合划分，比之前的更完善，利用sklearn的工具
housing['income_cat']=np.ceil(housing['median_income']/1.5)  #分档，除以1.5之后取整进行分层
housing['income_cat'].where(housing['income_cat']<5,5.0,inplace=True)  #将大于5的整体替换成5档

from sklearn.model_selection import StratifiedShuffleSplit
split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)
for train_index,test_index in split.split(housing,housing['income_cat']):
    strat_train_set=housing.loc[train_index]
    strat_test_set=housing.loc[test_index]
housing['income_cat'].value_counts()/len(housing)  #不同档位的比例分布

#进行一些可视化分析
#1.地理数据可视化
housing_new=strat_train_set.copy()  #创建训练集副本进行操作
housing_new.plot(kind='scatter',x='longitude',y='latitude')
#增加些参数,让图像显得更加能看出规律性
housing_new.plot(kind='scatter',x='longitude',y='latitude',alpha=0.4,\
                 s=housing_new['population']/100,label='population',\
                 c='median_house_value',cmap=plt.get_cmap('jet'),colorbar=True,)
plt.legend()

#描述数据之间的相关性
corr_matrix=housing_new.corr()
from pandas.plotting import scatter_matrix
attributes=['median_house_value','median_income','total_rooms','housing_median_age']
scatter_matrix(housing_new[attributes],figsize=(12,8),alpha=0.3)
#显示相关系数最高的是输入中位数，单独拿出来画图
housing_new.plot(kind='scatter',x='median_income',y='median_house_value',alpha=0.1)

#实验不同属性的组合获取一些高相关性的参数
housing_new['rooms_per_household']=housing_new['total_rooms']/housing_new['households']
housing_new['bedrooms_per_room']=housing_new['total_bedrooms']/housing_new['total_rooms']
housing_new['population_per_household']=housing_new['population']/housing_new['households']
corr_matrix_new=housing_new.corr()
corr_matrix_new['median_house_value'].sort_values(ascending=False)


#回到干净的数据集，开始机器学习实践

housing1=strat_train_set.drop('median_house_value',axis=1)
housing_labels=strat_train_set['median_house_value'].copy()

#处理缺失数据,用scikit-learn的imputer工具
from sklearn.impute import SimpleImputer
imputer=SimpleImputer(strategy='median')  #使用中位数替代缺失值
housing_num=housing_new.drop('ocean_proximity',axis=1)
imputer.fit(housing_num)  #使用fit方法将imputer实例适配到训练集
#我们无法确认系统启动之后新数据中是否一定不存在缺失值，因此稳妥起见，我们将imputer方法应用于所有的数值属性
#imputer将所有属性计算得到的中位数放在imputer.statistics_属性中



