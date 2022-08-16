
import sys, numpy as np, pandas as pd
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QFile, QTextStream, QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QProgressBar
import qdarkstyle
from PyQt5.QtWidgets import *
import requests, os, datetime, pandas as pd, json, numpy as np
class Window2(QtWidgets.QWidget):

    def __init__(self,n,c):
        super().__init__()
        self.init_ui()
        self.c=c
        self.n=n
    def init_ui(self):
        
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.label4 = QtWidgets.QLabel('')
        self.label5 = QtWidgets.QLabel('')
        self.label6 = QtWidgets.QLabel('')
        self.label7 = QtWidgets.QLabel('')

        self.buttonRun = QtWidgets.QPushButton('Run code')
        
        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.buttonRun)
        h_box6 = QtWidgets.QHBoxLayout()
        h_box6.addWidget(self.label4)
        h_box7 = QtWidgets.QHBoxLayout()
        h_box7.addWidget(self.label5)
        h_box8 = QtWidgets.QHBoxLayout()
        h_box8.addWidget(self.pbar)
        v_box = QtWidgets.QVBoxLayout()
 
        v_box.addLayout(h_box6)
        v_box.addLayout(h_box7)
        v_box.addLayout(h_box8)
        v_box.addLayout(h_box)
        self.setLayout(v_box)
        self.setWindowTitle('Update')
        self.setGeometry(300, 150, 100, 100)
        self.buttonRun.clicked.connect(self.click)
        self.show()
    def click(self):
         self.label4.setText('')
         self.label5.setText('')
         n = self.n
         c = self.c
         path = 'path'
         path2='premium'
         data = pd.read_excel('data.xlsx')
         try:

             def tokeen():
                 url = 'http://161.97.136.74:7000/api/v1/auth/token/'
                 payload = 'username=' + n + '&password=' + c
                 headers = {'Content-Type':'application/x-www-form-urlencoded', 
                  'Accept':'application/json', 
                  'Authorization':'Bearer {{token}}'}
                 response = requests.request('POST', url, headers=headers, data=payload)
                 access = response.text[11:len(response.text) - 2]
                 return access

             data = pd.read_excel('data.xlsx')
         except:
             pass
         else:

             def delett(cato, img):
                 url = 'http://161.97.136.74:7000/api/v1/questions/delete/'
                 access = tokeen()
                 payloads = {'category_id':cato,  'question_name':img}
                 files = []
                 headers = {'Authorization': 'Bearer ' + access}
                 response = requests.request('POST', url, headers=headers, data=payloads)
                 print(response.text)

             def verialma():
                 access = tokeen()
                 url = 'http://161.97.136.74:7000/api/v1/questions/categories/'
                 payload = {}
                 headers = {'Accept':'application/json', 
                  'Authorization':'Bearer ' + access}
                 response = requests.request('GET', url, headers=headers, data=payload)
                 data = json.loads(response.text)
                 try:
                     idd = data[(len(data) - 1)]['id']
                     self.label5.setText('Yükleme yapılıyor')
                     self.label4.setText('')
                 except:
                     self.label5.setText('')
                     self.label4.setText('şifre ve kullanıcı adı yanlış')
                 else:
                     return idd

             def uploadd(catog, img, path):
                 idd = verialma()
                 access = tokeen()
                 url = 'http://161.97.136.74:7000/api/v1/questions/upload/'
                 path = path + '/' + catog + '/' + img
                 payload = {'category': idd}
                 files = [
                  (
                   'images', (img, open(path, 'rb'), 'image/jpeg'))]
                 headers = {'Authorization': 'Bearer ' + access}
                 response = requests.request('POST', url, headers=headers, data=payload, files=files)
                 print(response.text)
                 return idd

             def uploadd2(catog, img, path, idd):
                 access = tokeen()
                 url = 'http://161.97.136.74:7000/api/v1/questions/upload/'
                 path = path + '/' + catog + '/' + img
                 payload = {'category': idd}
                 files = [
                  (
                   'images', (img, open(path, 'rb'), 'image/jpeg'))]
                 headers = {'Authorization': 'Bearer ' + access}
                 response = requests.request('POST', url, headers=headers, data=payload, files=files)
                 print(response.text)

             def creatt(result, path,path2):
                 url = 'http://161.97.136.74:7000/api/v1/questions/categories/'
                 idds = []
                 catogeryy = 0
                 self.pbar.setMaximum(len(result))
                 for count, i in enumerate(result):
                     if catogeryy != i[0]:
                         access = tokeen()
                         self.label5.setText('Yükleme yapılıyor')
                         self.label4.setText('')
                         data = dict()
                         if i[3]==1:
                             data['name'] = i[0]
                             data['description'] = i[0]         
                             data['is_premium'] = "true"
                         else:
                             data['name'] = i[0]
                             data['description'] = i[0]
                         headers = {'Content-Type':'application/x-www-form-urlencoded', 
                          'Accept':'application/json', 
                          'HTTP_X_UNIQUE_KEY':'deserunt 1234eds pc', 
                          'Authorization':'Bearer ' + access}
                         response = requests.request('POST', url, headers=headers, data=data)
                         catogeryy = i[0]
                         print(response.text)
                     if i[3]==0:    
                         idd = uploadd(i[0], i[1], path)
                     else:
                         idd = uploadd(i[0], i[1], path2)
                     idds.append(idd)
                     self.pbar.setValue(count + 1)
                 else:
                     return idds

             def creatt2(result, path,path2):
                 url = 'http://161.97.136.74:7000/api/v1/questions/categories/'
                 idds = []
                 access = tokeen()
                 data = dict()
                 if result[3]==1:
                             data['name'] = i[0]
                             data['description'] = i[0]         
                             data['is_premium'] = "true"
                 else:
                             data['name'] = i[0]
                             data['description'] = i[0]
                 headers = {'Content-Type':'application/x-www-form-urlencoded', 
                  'Accept':'application/json', 
                  'HTTP_X_UNIQUE_KEY':'deserunt 1234eds pc', 
                  'Authorization':'Bearer ' + access}
                 response = requests.request('POST', url, headers=headers, data=data)
                 print(response.text)
                 if result[3]==0:    
                         idd = uploadd(result[0], result[1], path)
                 else:
                         idd = uploadd(result[0], result[1], path2)
         
                 idds.append(idd)
                 return idds

         if len(data) == 0:
             catog = os.listdir(path)
             labels = []
             for i in catog:
                 if i != '.DS_Store':
                     labels.append(os.listdir(path + '/' + i))
                 for j in range(len(labels)):
                     for k in labels[j]:
                         if k == '.DS_Store':
                             labels[j].remove('.DS_Store')
                        
             ctimes = []
             for i in range(len(catog)):
                 if catog[i] != '.DS_Store':
                     ctime = []
         
                     for j in labels[i]:
                         if j != '.DS_Store':
                             ctime.append(round(os.path.getctime(path + '/' + catog[i] + '/' + j), 3))
                     ctimes.append(ctime)
             result = []
             for i in range(len(catog)):
                 for j in range(len(labels[i])):
                     result.append([catog[i], labels[i][j], ctimes[i][j],0])
             catog = os.listdir(path2)
             labels2 = []
             for i in catog:
                 if i != '.DS_Store':
                     labels2.append(os.listdir(path2 + '/' + i))
                 for j in range(len(labels2)):
                     for k in labels2[j]:
                         if k == '.DS_Store':
                             labels2[j].remove('.DS_Store')
                        
             ctimes = []
             for i in range(len(catog)):
                 if catog[i] != '.DS_Store':
                     ctime = []
         
                     for j in labels2[i]:
                         if j != '.DS_Store':
                             ctime.append(round(os.path.getctime(path2 + '/' + catog[i] + '/' + j), 3))
                     ctimes.append(ctime)                    
           
             for i in range(len(catog)):
                 for j in range(len(labels2[i])):
                     result.append([catog[i], labels2[i][j], ctimes[i][j],1])
                    
             idds = creatt(result, path,path2)
             idds = pd.DataFrame(idds, columns=['id'])
             df = pd.DataFrame(result, columns=['category', 'img', 'ctime',"premium"])
             Result = pd.concat([df, idds], axis=1)
             Result = Result.set_index('category')
             Result.to_excel('data.xlsx')
             self.label5.setText('Bitti')
     #ilk kayıt yapıldıktan sonra
         else:
             self.label5.setText('Güncelleme yapıyor')
             drops = []
             resultccc=0
             catooggg=0
             catog = os.listdir(path)
             labels = []
             for i in catog:
                 if i != '.DS_Store':
                     labels.append(os.listdir(path + '/' + i))
                 for j in range(len(labels)):
                     for k in labels[j]:
                         if k == '.DS_Store':
                             labels[j].remove('.DS_Store')
                        
             ctimes = []
             for i in range(len(catog)):
                 if catog[i] != '.DS_Store':
                     ctime = []
         
                     for j in labels[i]:
                         if j != '.DS_Store':
                             ctime.append(round(os.path.getctime(path + '/' + catog[i] + '/' + j), 3))
                     ctimes.append(ctime)
             result = []
             for i in range(len(catog)):
                 for j in range(len(labels[i])):
                     result.append([catog[i], labels[i][j], ctimes[i][j],0])
             catog = os.listdir(path2)
             labels2 = []
             for i in catog:
                 if i != '.DS_Store':
                     labels2.append(os.listdir(path2 + '/' + i))
                 for j in range(len(labels2)):
                     for k in labels2[j]:
                         if k == '.DS_Store':
                             labels2[j].remove('.DS_Store')
                        
             ctimes = []
             for i in range(len(catog)):
                 if catog[i] != '.DS_Store':
                     ctime = []
         
                     for j in labels2[i]:
                         if j != '.DS_Store':
                             ctime.append(round(os.path.getctime(path2 + '/' + catog[i] + '/' + j), 3))
                     ctimes.append(ctime)                    
           
             for i in range(len(catog)):
                 for j in range(len(labels2[i])):
                     result.append([catog[i], labels2[i][j], ctimes[i][j],1])
             result2 = data.values.tolist()
             resultc=[]
             for k in result2:
                 resultc.append(k[0])
             for i in result:
                     
             
                     status = 0
                     for count, j in enumerate(result2):
                         if i[0] == j[0] and i[1] == j[1] and i[2] != j[2]:
                             status = 1
                             if i[3]==0:
                                 uploadd2(i[0], i[1], path, result2[resultc.index(i[0])][3])
                             else:
                                 uploadd2(i[0], i[1], path2, result2[resultc.index(i[0])][3])
                             result2[count][2]=    i[2]
                         if i[0] == j[0] and i[1] == j[1] and i[2] == j[2]:
                             status = 1
                             break
                             
                     
                         
                      
                     if status == 0:
                             if i[0] in resultc:
                                 
                                 indes = resultc.index(i[0])
                                 if i[3]==0:
                                     uploadd2(i[0], i[1], path, result2[resultc.index(i[0])][3])
                                 else:
                                     uploadd2(i[0], i[1], path2, result2[resultc.index(i[0])][3])
                                 result2.append([i[0], i[1], i[2],i[3], result2[indes][3]])
                             else:    
                                 idd = creatt2(i, path,path2)
                                 result2.append([i[0], i[1], i[2],i[3], idd])
                                 resultc.append(i[0])
                           

                     
             for count, i in enumerate(result2):
                             status = 0
                             for j in result:
                                 if i[0] == j[0] and i[1] == j[1]:
                                     status = 1
                                     break
             
                             if status==0:  
                                     status3=0
                                     for iiii in result2:
                                         if iiii[0] == i[0]:
                                             idd = iiii[4]
                                             status3=1
                                             break
                                     if status3==1:
                                             delett(idd, i[1])
                                             drops.append(count)
                     
                     
             
                             
                                       
                                       
             if len(drops)  >=0:  
                 result22=[]
                 for i in range(len(result2)):
                    if i in drops:
                        pass
                    else:
                        result22.append(result2[i])
                 result2=result22        
             result2 = pd.DataFrame(result2, columns=['category', 'img', 'ctime',"premium", 'id'])
             result2 = result2.set_index('category')
             result2.to_excel('data.xlsx')
             self.label5.setText('Bitti')
             
class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.w= None 
        self.init_ui()

    def init_ui(self):
        self.label2 = QtWidgets.QLabel('Kullanıcı adı')
        self.label3 = QtWidgets.QLabel('Şifre')

        self.label4 = QtWidgets.QLabel('')
        self.label5 = QtWidgets.QLabel('')
        self.label6 = QtWidgets.QLabel('')
        self.label7 = QtWidgets.QLabel('')
        self.textbox = QLineEdit(self)
        self.textbox2 = QLineEdit(self)
        self.buttonRun = QtWidgets.QPushButton('Giriş')
        h_box4 = QtWidgets.QHBoxLayout()
        h_box4.addWidget(self.label2)
        h_box4.addWidget(self.textbox)
        h_box5 = QtWidgets.QHBoxLayout()
        h_box5.addWidget(self.label3)
        h_box5.addWidget(self.textbox2)
        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.buttonRun)
        h_box6 = QtWidgets.QHBoxLayout()
        h_box6.addWidget(self.label4)
        h_box7 = QtWidgets.QHBoxLayout()
        h_box7.addWidget(self.label5)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box4)
        v_box.addLayout(h_box5)
        v_box.addLayout(h_box6)
        v_box.addLayout(h_box7)

        v_box.addLayout(h_box)
        self.setLayout(v_box)
        self.setWindowTitle('Update')
        self.setGeometry(600, 150, 200, 200)
        self.buttonRun.clicked.connect(self.click)
        self.show()

    def click(self):
        self.label4.setText('')
        self.label5.setText('')
        n = self.textbox.text()
        c = self.textbox2.text()
        path = 'path'
        path2='premium'
        data = pd.read_excel('data.xlsx')
        
        def tokeen(n,c):
                url = 'http://161.97.136.74:7000/api/v1/auth/token/'
                payload = 'username=' + n + '&password=' + c
                headers = {'Content-Type':'application/x-www-form-urlencoded', 
                 'Accept':'application/json', 
                 'Authorization':'Bearer {{token}}'}
                
                response = requests.request('POST', url, headers=headers, data=payload)
                access = response.text[11:len(response.text) - 2]
                if len(access)>100:
                    self.label5.setText('Giriş Başarılı')
                    self.label4.setText('')
                    self.close()
                    self.w = Window2(n,c)
                    self.w.show()
                else:
                    self.label5.setText('Hatalı Giriş')
                    self.label4.setText('')
                return access

            
      
        idd =  tokeen(n,c)
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        pass