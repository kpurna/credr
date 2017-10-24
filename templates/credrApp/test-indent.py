from django.http import Http404,HttpResponse, HttpResponseBadRequest
import json

from django.conf import settings
from p3.db import query

import time
from datetime import datetime

def staticCompanies_details(request):
    limit=request.REQUEST.get('limit','25')
    offset=request.REQUEST.get('offset','0') 
    id = request.REQUEST.get('id','')
    client_id = request.REQUEST.get('client_id','')
    company_name = request.REQUEST.get('company_name','')
    head_title = request.REQUEST.get('head_title','')    
    top_content = request.REQUEST.get('top_content','')
    tags = request.REQUEST.get('tags','')
    company_logo_url = request.REQUEST.get('company_logo_url','')
    company_image_url = request.REQUEST.get('company_image_url','')
    url = request.REQUEST.get('url','')
    video_url = request.REQUEST.get('video_url','')
    placement_paper_company_name = request.REQUEST.get('placement_paper_company_name','')
    keyword1 = request.REQUEST.get('keyword1','')
    keyword2 = request.REQUEST.get('keyword2','')
    keyword3 = request.REQUEST.get('keyword3','')
    keyword4 = request.REQUEST.get('keyword4','')
    keyword5 = request.REQUEST.get('keyword5','')
    keyword6 = request.REQUEST.get('keyword6','')
    key_link1 = request.REQUEST.get('key_link1','')
    key_link2 = request.REQUEST.get('key_link2','')
    key_link3 = request.REQUEST.get('key_link3','')
    key_link4 = request.REQUEST.get('key_link4','')
    key_link5 = request.REQUEST.get('key_link5','')
    key_link6 = request.REQUEST.get('key_link6','')
    seo_title = request.REQUEST.get('seo_title','')
    seo_description = request.REQUEST.get('seo_description','')
    seo_keyword = request.REQUEST.get('seo_keyword','')
    created_time = request.REQUEST.get('created_time','')
    last_updated_time = request.REQUEST.get('last_updated_time','')
    status = request.REQUEST.get('status','')
    comment = request.REQUEST.get('comment','')
    company_category = request.REQUEST.get('company_category','')
    verified_status = request.REQUEST.get('verified_status','')
    priority = request.REQUEST.get('priority','')

    where = "";
    
    if(id !=""):
        sql = "SELECT id,client_id,company_name,head_title,top_content,tags,company_logo_url,company_image_url,url,video_url,placement_paper_company_name,keyword1,keyword2,keyword3,keyword4,keyword5,keyword6,key_link1,key_link2,key_link3,key_link4,key_link5,key_link6,seo_title,seo_description, seo_keyword,created_time,last_updated_time,status,comment,company_category,verified_status,priority from fw.static_companies WHERE id= %s"
        param_for_staticCompanies_details=[id]
        result = query(sql,*param_for_staticCompanies_details)
        print result
        result_count = len(result)
        if result_count == 0:
            return HttpResponseBadRequest(content="Id does not exist in database")
        response_map = {}
        response_map['id']=result[0]['id']
        response_map['client_id']=result[0]['client_id']
        response_map['company_name']=result[0]['company_name']
        response_map['head_title']=result[0]['head_title']    
        response_map['top_content']=result[0]['top_content']
        response_map['tags']=result[0]['tags']
        response_map['company_logo_url']=result[0]['company_logo_url']
        response_map['company_image_url']=result[0]['company_image_url']
        response_map['url']=result[0]['url']
        response_map['video_url']=result[0]['video_url']
        response_map['placement_paper_company_name']=result[0]['placement_paper_company_name']
        response_map['keyword1']=result[0]['keyword1']
        response_map['keyword2']=result[0]['keyword2']
        response_map['keyword3'] =result[0]['keyword3']
        response_map['keyword4'] =result[0]['keyword4']
        response_map['keyword5']=result[0]['keyword5']
        response_map['keyword6']=result[0]['keyword6']
        response_map['key_link1']=result[0]['key_link1']
        response_map['key_link2']=result[0]['key_link2']
        response_map['key_link3']=result[0]['key_link3']
        response_map['key_link4']=result[0]['key_link4']
        response_map['key_link5']=result[0]['key_link5']
        response_map['key_link6']=result[0]['key_link6']
        response_map['seo_title']=result[0]['seo_title']
        response_map['seo_description']=result[0]['seo_description']
        response_map['seo_keyword']=result[0]['seo_keyword']
        response_map['created_date']=result[0]['created_time']
        response_map['changed_date']=result[0]['last_updated_time']
        response_map['status']=result[0]['status']
        response_map['comment']=result[0]['comment']
        response_map['company_category']=result[0]['company_category']
        response_map['verified_status']=result[0]['verified_status']
        response_map['priority']=result[0]['priority']       
        response = {'staticCompanies':response_map}     
    else:
        where = "1=1"
        param_for_question_list=[] 
                      
        sql = "SELECT * from p3_questions as cs where "+ where
                   
        results = query(sql,*param_for_staticCompanies_details)     
        final_test_map = []  
        metadata_totalcount=0 
        #result is constructed in the expected format
        for result in results:
            metadata_totalcount=metadata_totalcount+1
            response_map = {}
        response_map['id']=result['id']
        response_map['client_id']=result['client_id']
        response_map['company_name']=result['company_name']
        response_map['head_title']=result['head_title']    
        response_map['top_content']=result['top_content']
        response_map['tags']=result['tags']
        response_map['company_logo_url']=result['company_logo_url']
        response_map['company_image_url']=result['company_image_url']
        response_map['url']=result['url']
        response_map['video_url']=result['video_url']
        response_map['placement_paper_company_name']=result['placement_paper_company_name']
        response_map['keyword1']=result['keyword1']
        response_map['keyword2']=result['keyword2']
        response_map['keyword3'] =result['keyword3']
        response_map['keyword4'] =result['keyword4']
        response_map['keyword5']=result['keyword5']
        response_map['keyword6']=result['keyword6']
        response_map['key_link1']=result['key_link1']
        response_map['key_link2']=result['key_link2']
        response_map['key_link3']=result['key_link3']
        response_map['key_link4']=result['key_link4']
        response_map['key_link5']=result['key_link5']
        response_map['key_link6']=result['key_link6']
        response_map['seo_title']=result['seo_title']
        response_map['seo_description']=result['seo_description']
        response_map['seo_keyword']=result['seo_keyword']
        response_map['created_date']=result['created_time']
        response_map['changed_date']=result['last_updated_time']
        response_map['status']=result['status']
        response_map['comment']=result['comment']
        response_map['company_category']=result['company_category']
        response_map['verified_status']=result['verified_status']
        response_map['priority']=result['priority']       
        response = {'staticCompanies':response_map}              
        final_test_map.append(response_map)
    metadata = {"total_count":metadata_totalcount}
    response = {"metadata":metadata,'questions':final_test_map} 
            
    questions = json.dumps(response, encoding="ISO-8859-1")    
    http_response = HttpResponse(questions,content_type="application/json")
    return http_response