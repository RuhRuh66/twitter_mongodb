# 位置情報を持っているツイートの割合
num_not_geo = tweetdata.find({'coordinates':None,'spam':None},{'_id':1, 'coordinates':1}).count()
num_geo = tweetdata.find({'coordinates':{"$ne":None},'spam':None},{'_id':1, 'coordinates':1}).count()

print "num_not_geo",num_not_geo
print "num_geo", num_geo
print "%.3f"%(num_geo / float(num_geo+num_not_geo) * 100),"%"

# 位置情報
loc_data = np.array([[d['coordinates']['coordinates'][1],d['coordinates']['coordinates'][0]]\
           for d in tweetdata.find({'coordinates':{"$ne":None},'spam':None},{'_id':1, 'coordinates':1})])

lat = loc_data[:,0]  # 緯度
lon = loc_data[:,1]  # 経度 

xlim_min = [np.min(lon)*.9,120,139]
xlim_max = [np.max(lon)*1.1,150,140.5]
ylim_min = [np.min(lat)*.9,20,35.1]
ylim_max = [np.max(lat)*1.1,50,36.1]

for x1,x2,y1,y2 in zip(xlim_min,xlim_max,ylim_min,ylim_max):
    plt.figure(figsize=(10,10))
    plt.xlim(x1,x2)
    plt.ylim(y1,y2)
    plt.scatter(lon, lat, s=20, alpha=0.4, c='b')
    
#--------------------------------------------------
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

ar = np.arange

enlarge = [1,2,4,8,16,32]
w_list = [15000000./(i) for i in enlarge]
h_list = [9000000./(i) for i in enlarge]

xlim_min = [-142,  80,  120,  135,   139]
xlim_max = [ 192, 160,  150,  142,   141]
ylim_min = [ -45,   0,   20,   33,    35]
ylim_max = [  75,  50,   50,   37,  36.2]
ss       = [ 0.7, 0.3,  0.1, 0.03, 0.005]

for i, s in zip(ar(len(xlim_min)),ss):
    
    m = Basemap(projection='merc',llcrnrlat=ylim_min[i] ,urcrnrlat=ylim_max[i] ,\
            llcrnrlon=xlim_min[i],urcrnrlon=xlim_max[i] ,lat_ts=20, resolution='c')
    plt.figure(figsize=(13,13))

    m.plot(lon,lat,'ro')
    m.bluemarble()

    for x, y in zip(lon,lat):
        m.tissot(x,  y, s,100,facecolor='red',zorder=100,alpha=0.4)

    plt.show()
    plt.savefig('plot_map_%s.png'%(str(i)))

