from model.DB import DB
from sample_data import products
import os
import json

class file_db(DB):

    def get_users_column_names(self):
        return super().get_users_column_names()

    def get_product_column_names(self):
        with open("./src/model/products.py","rb") as f:
            file = f.read().decode()
            file = file.replace("products = ","").replace(" ","")
            return json.loads(file.split("\r\n")[1][:-1]).keys()

    def has_data(self):
        with open("./src/model/products.py","rb") as f:
            file = f.read().decode() 
            return not file == "products = []"
        
    def fill(self):
        with open("./src/model/products.py","r+b") as f:
            contents = "products = [\r\n"
            for i,product in enumerate(products):
                content = '{'+'"ID":{},'.format(i)
                for x,item in enumerate(product.items()):
                    value = '"{}"'.format(item[1]) if type(item[1]) == str else item[1]
                    if x < len(product.items()) -1:
                        content += '"{}":{},'.format(item[0],value)
                    else:
                        content += '"{}":{}'.format(item[0],value) + "}"
                if i != len(products)-1:
                    contents+=content +",\r\n"
                else:
                    contents+=content +"\r\n"
            contents+="]"
            f.write(contents.encode())

    def get_product_by_name(self,name):
        
        with open("./src/model/products.py","rb") as f:
            file = f.read().decode()
            file = file.replace("products = ","")
            lines = file.split("\r\n")[1:-1]
            obj = None
            for i,line in enumerate(lines):
        
                if i != len(lines) -1:
                    obj = json.loads(line[:-1])
                else:
                    obj = json.loads(line)
                if obj["name"] == name:
                    return obj
            return None

    def get_product_by_id(self,id):
        with open("./src/model/products.py","r+b") as f:
            file = f.read().decode()
            file = file.replace("products = ","")
            lines = file.split("\r\n")[1:-1]
            obj = None
            for i,line in enumerate(lines):
                if i != len(lines) -1:
                    obj = json.loads(line[:-1])
                else:
                    print(line)
                    obj = json.loads(line)
                print(obj)
                if obj["ID"] == id:
                    return obj
            return None
    
    def get_products(self):
        with open("./src/model/products.py","rb") as f:
            file = f.read().decode()
            file = file.replace("products = ","")
            lines = file.split("\r\n")[1:-1]
            lst = []
            for i,line in enumerate(lines):
                if i != len(lines) -1:
                    lst.append(json.loads(line[:-1]))
                else:
                    lst.append(json.loads(line))
            return lst
    
    def update_product_by_id(self,id,new_product):
        #only update objects that are different
        
        content= ""
        with open("./src/model/products.py","rb") as f:
            file = f.read().decode()
            lines = file.split("\r\n")[1:-1]
            product_index = [i for i,item in enumerate(lines) if int(item[item.find('"ID":')+5]) == id][0]

            old_product = json.loads(lines[product_index]) if lines[product_index][-1] != "," else json.loads(lines[product_index][:-1])
            dictstring = ""

            for i,item in enumerate(old_product.items()):
                if item[0] == "ID":
                   dictstring+= "{"+'"ID":{},'.format(id)
                   continue
                #if key is in new product use that value else use the one from the old product
                elif item[0] in new_product.keys():
                    value = '"{}"'.format(new_product[item[0]]) if type(new_product[item[0]]) == str else new_product[item[0]]
                else:
                    value = '"{}"'.format(item[1]) if type(item[1]) == str else item[1]
                print("Value is {}".format(value))
                if i < len(old_product) -1:
                    print("not last")
                    dictstring += '"{}":{},'.format(item[0],value)
                else:
                    print("Values is last")
                    dictstring += '"{}":{}'.format(item[0],value) + "}"
            
            print(dictstring)

            if product_index < len(lines) -1:
                dictstring+=","
            #product = json.loads(lines[product_index]) if lines[product_index][-1] !="," else json.loads(lines[product_index][:-1])
            lines[product_index] = dictstring
            content = "products = [\r\n"+"\r\n".join(lines) +"\r\n]"
        with open("./src/model/products.py","wb") as f:
            f.write(content.encode())
    
    def delete_product_by_id(self,id):
        content= ""
        with open("./src/model/products.py","rb") as f:
            file = f.read().decode()
            lines = file.split("\r\n")[1:-1]
            product_index = [i for i,item in enumerate(lines) if int(item[item.find('"ID":')+5]) == id][0]

            product = lines[product_index]
            if product_index == len(lines)-1:
                del lines[product_index]
                lines[-1] = lines[-1][:-1]
            else:
                del lines[product_index]
   
            content = "products = [\r\n"+"\r\n".join(lines) +"\r\n]"
        with open("./src/model/products.py","wb") as f:
            f.write(content.encode())
        return product

    def add_product(self,product):
        content= ""
        id = None
        with open("./src/model/products.py","rb") as f:
            file = f.read().decode()
            lines = file.split("\r\n")[1:-1]
            print(lines[-1])
            id = json.loads(lines[-1])["ID"]+1
            print("new object id is {}".format(id))
            lines[-1] += ","
            dictstring = "{"+'"ID":{},'.format(id)
            for i,item in enumerate(product.items()):
                value = '"{}"'.format(item[1]) if type(item[1]) == str else item[1]
                if i < len(product) -1:
                    dictstring+='"{}":{},'.format(item[0],value)
                else:
                    dictstring+='"{}":{}'.format(item[0],value) + "}"
            lines.append(dictstring)
            print(lines)
            content = "products = [\r\n"+"\r\n".join(lines) +"\r\n]"
        with open("./src/model/products.py","wb") as f:
            f.write(content.encode())
        return id

            


