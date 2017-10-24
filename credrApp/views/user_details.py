from django.http import Http404,HttpResponse, HttpResponseBadRequest
import json
from django.conf import settings
from credrApp.db import query
import time
from datetime import datetime
import decimal, simplejson

class DecimalJSONEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalJSONEncoder, self).default(o)

# def user_details(request):

#     limit=request.REQUEST.get('limit','25')
#     offset=request.REQUEST.get('offset','0') 
#     id = request.REQUEST.get('id','')
#     name = request.REQUEST.get('name','')
#     email_id = request.REQUEST.get('email_id','')
#     status=request.REQUEST.get('status','')
#     where = "";     
#     if(id !=""):
#         sql = "SELECT * from user WHERE id= %s "
#         param_for_user_details=[id]    
#         result = query(sql,*param_for_user_details)      
#         result_count = len(result)
#         if result_count == 0:
#             return HttpResponseBadRequest(content="Id does not exist in database")    
#         response_map = {}
#         response_map['id']=result[0]['id']
#         response_map['name']=result[0]['name']
#         response_map['status']=result[0]['status']
#         response_map['email_id']=result[0]['email_id']
#         try:
#             response_map['created_date']=datetime.fromtimestamp(result[0]['created_date']).strftime('%d-%m-%Y')
#         except:
#             response_map['created_date']="NA" 
#         try:
#             response_map['last_login']=datetime.fromtimestamp(result[0]['last_login']).strftime('%d-%m-%Y')
#         except:
#             response_map['last_login']="NA"         
#         response = {'data':response_map}     
#     else:
#         where = "1=1"
#         param_for_user_list=[] 
#         if(name !=""):           
#             name = "%"+name+"%"
#             where += " and UPPER(u.name) like (%s)"
#             param_for_user_list.append(name)

#         if(email_id !=""):
#             email_id = "%"+email_id+"%"
#             where += " and UPPER(u.email_id) like (%s)"
#             param_for_user_list.append(email_id)
        
#         if(status !=""):
#             where += " and u.status like %s"
#             param_for_user_list.append(status)                   
#         sql = "SELECT * from user as u where "+ where+" ORDER BY u.id  DESC"                  
#         results = query(sql,*param_for_user_list)     
#         final_test_map = []  
#         metadata_totalcount=0 
#         #result is constructed in the expected format
#         for result in results:
#             metadata_totalcount=metadata_totalcount+1
#             response_map = {}
#             response_map['id']=result['id']
#             response_map['name']=result['name']
#             response_map['status']=result['status']
#             response_map['email_id']=result['email_id']                                                                                        
#             final_test_map.append(response_map)       
#         metadata = {"total_count":metadata_totalcount}
#         response = {"metadata":metadata,'data':final_test_map}        
#     data = json.dumps(response, encoding="ISO-8859-1")    
#     http_response = HttpResponse(data,content_type="application/json")
#     return http_response

def invoice_details(request):
    # import pdb; pdb.set_trace();
    # path = str(request.path)
    # id_from_url = path.split('/')
    # id = id_from_url[3]
    if(request.method == "POST"):
        post_data = json.loads(request.body)
        limit=post_data.get('limit','25')
        offset=post_data.get('offset','0') 
        id = post_data.get('id','')
        customer=post_data.get('customer','')
        if(id == ''):
            date = datetime.now()
            total_quantity = 0
            total_amount = 0
            if customer == '':
                return HttpResponseBadRequest(content="Please send valid Json with customer name")
            sql = "SELECT auto_increment FROM INFORMATION_SCHEMA.TABLES WHERE table_name = 'invoice'"
            param_for_invoice_details = []
            max_id_result = query(sql,*param_for_invoice_details)
            id = int(max_id_result[0]['auto_increment'])
            insert_qry_execute="insert into invoice (invoice_id,customer, date, total_quantity, total_amount) values(%s,%s,%s,%s,%s)"
            query(insert_qry_execute, id, customer, date, total_quantity, total_amount)
            transaction = post_data.get('transactions','0')
            if transaction != 0:
                for trans in transaction:
                    transactions_list = {}
                    transactions_list['product'] = trans['product']
                    transactions_list['quantity'] = trans['quantity']
                    transactions_list['price'] = str(trans['price'])
                    line_total = int(trans['quantity'])*int(trans['price'])
                    transactions_list['line_total'] = str(line_total)
                    insert_trans_qry_execute="insert into invoice_transactions (invoice_id,product,quantity,price, line_total) values(%s,%s,%s,%s,%s)"
                    query(insert_trans_qry_execute,id, transactions_list['product'], transactions_list['quantity'], transactions_list['price'], transactions_list['line_total'])
            update_quantity_total_sql="select sum(quantity) as quantity, sum(line_total) as total from invoice_transactions where invoice_id = %s"
            parm_update_quantity_total_sql = [id]
            update_query_result = query(update_quantity_total_sql,*parm_update_quantity_total_sql)
            update_total_quantity = str(update_query_result[0]['quantity'])
            update_total_amount = str(update_query_result[0]['total'])
            update_qry_execute="update invoice set total_quantity = %s, total_amount = %s where invoice_id = %s"
            parm_update_qry = [update_total_quantity, update_total_amount, id]
            update_query_in_invoice = query(update_qry_execute,*parm_update_qry)
            response = {"msg": "created a customer successfully"} 
            data = simplejson.dumps(response, cls=DecimalJSONEncoder)
            http_response = HttpResponse(data,content_type="application/json")
            return http_response    
        elif id != '' and request.method== 'POST':
            sql = "SELECT * from invoice WHERE invoice_id= %s "
            param_for_invoice_details=[id]    
            result = query(sql,*param_for_invoice_details)
            result_count = len(result)
            if result_count == 0:
                return HttpResponseBadRequest(content="Id already used")
        else:    
            sql = "SELECT * from invoice WHERE invoice_id= %s "
            param_for_invoice_details=[id]    
            result = query(sql,*param_for_invoice_details)
            result_count = len(result)
            trans_sql = "SELECT * from invoice_transactions WHERE invoice_id= %s "
            param_for_invoice_trans_details=[id]    
            trans_result = query(trans_sql,*param_for_invoice_trans_details)
            trans_result_count = len(result)
            transactions = []
            if result_count == 0:
                return HttpResponseBadRequest(content="Id already used")
            if trans_result_count == 0:
                transactions = []
            else:
                for trans in trans_result:
                    transactions_list = {}
                    transactions_list['id'] = trans['id']
                    transactions_list['product'] = trans['product']
                    transactions_list['quantity'] = trans['quantity']
                    transactions_list['price'] = str(trans['price'])
                    transactions_list['line_total'] = str(trans['line_total'])
                    transactions.append(transactions_list)
            response_map = {}
            response_map['invoice_id']=result[0]['invoice_id']
            response_map['customer']=customer
            response_map['date']=str(result[0]['date'])
            response_map['transactions'] = transactions
            response_map['total_quantity']=str(result[0]['total_quantity'])
            response_map['total_amount']=str(result[0]['total_amount'])
            response = {'data':response_map}
            data = simplejson.dumps(response, cls=DecimalJSONEncoder)
            http_response = HttpResponse(data,content_type="application/json")
            return http_response
    elif(request.method == "DELETE"):
        post_data = json.loads(request.body)
        limit=post_data.get('limit','25')
        offset=post_data.get('offset','0') 
        id = post_data.get('id','')

        if(id != ''):
            sql = "SELECT * from invoice WHERE invoice_id= %s "
            param_for_invoice_details=[id]    
            result = query(sql,*param_for_invoice_details)
            if len(result) == 0:
                return HttpResponseBadRequest(content="Id does not exist in database")
            delete_trans_query_sql = "DELETE from invoice_transactions WHERE invoice_id= %s "
            param_for_invoice_trans_details=[id]
            trans_result = query(delete_trans_query_sql,*param_for_invoice_trans_details)
            delete_query_sql = "DELETE from invoice WHERE invoice_id= %s "
            param_for_invoice_details=[id]    
            result = query(delete_query_sql,*param_for_invoice_details)
            response = {"msg": "deleted successfully"} 
            data = json.dumps(response, encoding="ISO-8859-1")    
            http_response = HttpResponse(data,content_type="application/json")
            return http_response
        else:
            response = {"msg": "Requested id doesn't exist"} 
            data = json.dumps(response, encoding="ISO-8859-1")    
            http_response = HttpResponse(data,content_type="application/json")
            return http_response
    elif(request.method == "PUT"):
        post_data = json.loads(request.body)
        limit=post_data.get('limit','25')
        offset=post_data.get('offset','0') 
        customer=post_data.get('customer','')
        id = post_data.get('id','')
        if id == '':
            return HttpResponseBadRequest(content="Id does not exist in Input json")
        else:
            datacheck_sql = "SELECT count(*) as count from invoice WHERE invoice_id= %s "
            params_datacheck_sql=[id]    
            datacheck_result = query(datacheck_sql,*params_datacheck_sql)
            if datacheck_result[0]['count'] == 0:
                return HttpResponseBadRequest(content="Id does not exist in DB")
            if customer != '':
                update_qry_execute="update invoice set customer = %s where invoice_id = %s"
                query(update_qry_execute, customer, id)
            transaction = post_data.get('transactions', [])
            print len(transaction)
            if len(transaction) != 0:
                for trans in transaction:
                    transactions_list = {}
                    transactions_list['id'] = trans.get('id','')
                    transactions_list['product'] = trans['product']
                    transactions_list['quantity'] = trans['quantity']
                    transactions_list['price'] = str(trans['price'])
                    line_total = int(trans['quantity'])*int(trans['price'])
                    transactions_list['line_total'] = line_total
                    if (transactions_list['id'] == ''):
                        insert_trans_qry_execute="insert into invoice_transactions (invoice_id,product,quantity,price, line_total) values(%s,%s,%s,%s,%s)"
                        query(insert_trans_qry_execute, id, transactions_list['product'], transactions_list['quantity'], transactions_list['price'], transactions_list['line_total'])
                    else:
                        update_qry_execute="update invoice_transactions set product = %s, quantity = %s, price = %s, line_total =%s where invoice_id = %s and id = %s"
                        query(update_qry_execute, transactions_list['product'], transactions_list['quantity'], transactions_list['price'], transactions_list['line_total'], id, transactions_list['id'])
            else:
                delete_trans_query_sql = "DELETE from invoice_transactions WHERE invoice_id= %s "
                param_for_invoice_trans_details=[id]
                trans_result = query(delete_trans_query_sql,*param_for_invoice_trans_details)
                delete_query_sql = "DELETE from invoice WHERE invoice_id= %s "
                param_for_invoice_details=[id]    
                result = query(delete_query_sql,*param_for_invoice_details)
                # response = {"msg": "deleted successfully"} 
                # data = json.dumps(response, encoding="ISO-8859-1")    
                # http_response = HttpResponse(data,content_type="application/json")
                # return http_response
        update_quantity_total_sql="select sum(quantity) as quantity, sum(line_total) as total from invoice_transactions where invoice_id = %s"
        parm_update_quantity_total_sql = [id]
        update_query_result = query(update_quantity_total_sql,*parm_update_quantity_total_sql)
        if(update_query_result[0]['quantity'] != None and update_query_result[0]['total'] != None):
            update_total_quantity = str(update_query_result[0]['quantity'])
            update_total_amount = str(update_query_result[0]['total'])
            update_qry_execute="update invoice set total_quantity = %s, total_amount = %s where invoice_id = %s"
            parm_update_qry = [update_total_quantity, update_total_amount, id]
            update_query_in_invoice = query(update_qry_execute,*parm_update_qry)
        response = {"msg": "updated customer successfully"} 
        data = simplejson.dumps(response, cls=DecimalJSONEncoder)
        http_response = HttpResponse(data,content_type="application/json")
        return http_response 
    else:    
        where = "1=1"
        param_for_user_list=[] 
        sql = "SELECT * from invoice where "+ where+" ORDER BY invoice_id  DESC"                  
        results = query(sql,*param_for_user_list)
        final_test_map = []  
        metadata_totalcount=0 
        #result is constructed in the expected format
        for result in results:
            transactions = []
            metadata_totalcount=metadata_totalcount+1
            response_map = {}
            response_map['invoice_id']=result['invoice_id']
            trans_sql = "SELECT * from invoice_transactions WHERE invoice_id= %s "
            param_for_invoice_trans_details=[result['invoice_id']]    
            trans_result = query(trans_sql,*param_for_invoice_trans_details)
            trans_result_count = len(result)
            if trans_result_count == 0:
                transactions = []
            else:
                for trans in trans_result:
                    transactions_list = {}
                    transactions_list['id'] = trans['id']
                    transactions_list['product'] = trans['product']
                    transactions_list['quantity'] = trans['quantity']
                    transactions_list['price'] = str(trans['price'])
                    transactions_list['line_total'] = str(trans['line_total'])
                    transactions.append(transactions_list)    
            response_map['customer']=result['customer']
            response_map['date']=str(result['date'])
            response_map['transactions'] = transactions
            response_map['total_quantity']=result['total_quantity']
            response_map['total_amount']=str(result['total_amount'])                                                                                        
            final_test_map.append(response_map)       
        metadata = {"total_count":metadata_totalcount}
        response = {"metadata":metadata,'data':final_test_map}        
        data = simplejson.dumps(response, cls=DecimalJSONEncoder)
        http_response = HttpResponse(data,content_type="application/json")
        return http_response

def invoice_details_with_id(request, id=None):
    where = "";     
    if(id != None):
        sql = "SELECT * from invoice WHERE invoice_id= %s "
        param_for_invoice_details=[id]    
        result = query(sql,*param_for_invoice_details)
        result_count = len(result)
        trans_sql = "SELECT * from invoice_transactions WHERE invoice_id= %s "
        param_for_invoice_trans_details=[id]    
        trans_result = query(trans_sql,*param_for_invoice_trans_details)
        trans_result_count = len(result)
        transactions = []
        if result_count == 0:
            return HttpResponseBadRequest(content="Id does not exist in database")
        if trans_result_count == 0:
            transactions = []
        else:
            for trans in trans_result:
                transactions_list = {}
                transactions_list['id'] = trans['id']
                transactions_list['product'] = trans['product']
                transactions_list['quantity'] = trans['quantity']
                transactions_list['price'] = str(trans['price'])
                transactions_list['line_total'] = str(trans['line_total'])
                transactions.append(transactions_list)
        response_map = {}
        response_map['invoice_id']=result[0]['invoice_id']
        response_map['customer']=result[0]['customer']
        response_map['date']=str(result[0]['date'])
        response_map['transactions'] = transactions
        response_map['total_quantity']=result[0]['total_quantity']
        response_map['total_amount']=str(result[0]['total_amount'])
        response = {'data':response_map}     
    else:
        where = "1=1"
        param_for_user_list=[] 
        sql = "SELECT * from invoice where "+ where+" ORDER BY invoice_id  DESC"                  
        results = query(sql,*param_for_user_list)
        final_test_map = []  
        metadata_totalcount=0 

        #result is constructed in the expected format
        for result in results:
            transactions = []
            metadata_totalcount=metadata_totalcount+1
            response_map = {}
            response_map['invoice_id']=result['invoice_id']
            trans_sql = "SELECT * from invoice_transactions WHERE invoice_id= %s "
            param_for_invoice_trans_details=[result['invoice_id']]    
            trans_result = query(trans_sql,*param_for_invoice_trans_details)
            trans_result_count = len(result)
            if trans_result_count == 0:
                transactions = []
            else:
                for trans in trans_result:
                    transactions_list = {}
                    transactions_list['id'] = trans['id']
                    transactions_list['product'] = trans['product']
                    transactions_list['quantity'] = trans['quantity']
                    transactions_list['price'] = str(trans['price'])
                    transactions_list['line_total'] = str(trans['line_total'])
                    transactions.append(transactions_list)    
            response_map['customer']=result['customer']
            response_map['date']=str(result['date'])
            response_map['transactions'] = transactions
            response_map['total_quantity']=result['total_quantity']
            response_map['total_amount']=str(result['total_amount'])
            final_test_map.append(response_map)       
        metadata = {"total_count":metadata_totalcount}
        response = {"metadata":metadata,'data':final_test_map}        
    data = simplejson.dumps(response, cls=DecimalJSONEncoder)
    http_response = HttpResponse(data,content_type="application/json")
    return http_response
