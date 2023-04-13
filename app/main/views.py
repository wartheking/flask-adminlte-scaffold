from app import get_logger, get_config
import math
import json
from flask import render_template, redirect, url_for, flash, request,jsonify
from flask_login import login_required, current_user
from app import utils
from app.models import FurnituresData,FurnitureType,FurnitureStyles,FurnitureType2,Organizations
from app.main.forms import FurnituresDataForm
from . import main

logger = get_logger(__name__)
cfg = get_config()
furnitureTypeDic = {}
furnitureTypeDic2 = {}
furnitureStyleDic = {}
organizationsDic = {}
searchHref = ""
act = ""
key = ""
searchT = ""
useSearch = False
furnituresDataForm = None
def init_furnitureTypeDic():
    #装载家具类型
    if len(furnitureTypeDic) < 1:
        testQuery = FurnitureType.select()
        for furnitureType in testQuery:
            chName = furnitureType.typeCHName
            furnitureTypeDic[furnitureType.furnitureType] = chName

def init_furnitureTypeDic2():
    #装载家具类型2
    if len(furnitureTypeDic2) < 1:
        testQuery = FurnitureType2.select()
        for furnitureType in testQuery:
            name = furnitureType.typeCHName
            furType = furnitureType.furnitureType
            furType2 = furnitureType.furnitureType2
            furnitureTypeDic2[(int(furType),int(furType2))] = name

def init_furnitureStyle():
    #装载家具风格
    if len(furnitureStyleDic) < 1:
        testQuery = FurnitureStyles.select()
        for fStyle in testQuery:
            name = fStyle.name
            furnitureStyleDic[fStyle.furnitureStyle] = name

# 通用列表查询
def common_list(DynamicModel, view):
    
    global act
    global key
    global searchT
    global useSearch
    # 接收参数
    act = request.args.get('action')
    id = request.args.get('id')
    key = request.args.get('keyword')
    searchT = request.args.get('searchType')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE

    # 删除操作
    if act == 'del' and id:
        try:
            DynamicModel.get(DynamicModel.id == id).delete_instance()
            flash('删除成功')
        except:
            flash('删除失败')

    init_furnitureTypeDic()
    init_furnitureTypeDic2()
    init_furnitureStyle()
    
   
    try:
        if act == 'ser' and key and searchT:    
            useSearch = True
            if searchT == "furnitureID":
                query = DynamicModel.select().where(DynamicModel.furnitureID.contains(key))
            elif searchT == "furnitureName":
                query = DynamicModel.select().where(DynamicModel.furnitureName.contains(key))
            elif searchT == "furnitureType":
                keyword1 = ""
                for furkey in furnitureTypeDic.keys():
                    if str(furnitureTypeDic[furkey]) == str(key):
                        keyword1 = int(furkey)
                        query = DynamicModel.select().where(DynamicModel.furnitureType == keyword1)
            elif searchT == "furnitureType":
                keyword1 = ""
                for furkey in furnitureTypeDic.keys():
                    if str(furnitureTypeDic[furkey]) == str(key):
                        keyword1 = int(furkey)
                        query = DynamicModel.select().where(DynamicModel.furnitureType == keyword1)
            elif searchT == "furnitureType2":
                keyword1 = ""
                for furkey in furnitureTypeDic2.keys():
                    if str(furnitureTypeDic2[furkey]) == str(key):
                        keyword1 = furkey[1]
                        query = DynamicModel.select().where(DynamicModel.furnitureType2 == keyword1)
            elif searchT == "furnitureStyle":
                keyword1 = ""
                for furkey in furnitureStyleDic.keys():
                    if str(key) in str(furnitureStyleDic[furkey]):
                        keyword1 = int(furkey)
                        query = DynamicModel.select().where(DynamicModel.furnitureStyle == keyword1)
            elif searchT == "brand":
                query = DynamicModel.select().where(DynamicModel.brand.contains(key))
            elif searchT == "furnitureCraft":
                query = DynamicModel.select().where(DynamicModel.furnitureCraft.contains(key))
            elif searchT == "furnitureColor":
                query = DynamicModel.select().where(DynamicModel.furnitureColor.contains(key))
            elif searchT == "Organization":
                newKey = ""
                for org in organizationsDic:
                    if key in organizationsDic[org]:
                        newKey =  org
                query = DynamicModel.select().where(DynamicModel.organization.contains(newKey))
        else:
            useSearch = False
            query = DynamicModel.select()


        total_count = query.count()

        # 处理分页
        if page: query = query.paginate(page, length)
        result = utils.query_to_list(query)
       
        if len(result) < 1:
            flash('没找到符合类型模型')

        if len(organizationsDic) < 1:
            organizationQuery = Organizations.select();
            organizationResult = utils.query_to_list(organizationQuery)
            for org in organizationResult:
                organizationsDic[str(org["organizationID"])] = org["organizationName"]

            for orga in organizationsDic:
                print(orga)
                print(organizationsDic[orga])
        result1 = []
        for re in result:
            typeKey = (int(re['furnitureType']),int(re['furnitureType2']))
            re['furnitureType2'] = furnitureTypeDic2[typeKey]
            re['furnitureType'] = furnitureTypeDic[re['furnitureType']]
            re['furnitureStyle'] = furnitureStyleDic[re['furnitureStyle']]
            result1.append(re)
        
        
        title = "模型查找(" + str(searchT) + ":" + str(key) + ")"
        if key == "":
            title = "模型查找(全部)"
        
        
        dict = {'content': result1, 'title':title, 'total_count': total_count,
                'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
        return render_template(view, form=dict, current_user=current_user,orDic = organizationsDic)
    except Exception as e:
        flash(e)
        flash('查询失败')

def to_int(name):
    return int(name)




# 通用单模型查询&新增&修改
def common_edit(DynamicModel, form, view):
    id = request.args.get('id', '')
    if id:
        # 查询
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            model.furnitureType = str(model.furnitureType)
            utils.model_to_form(model, form)

        # 修改
        if request.method == 'POST':
            if form.validate_on_submit():
                for f in form:
                    print(f)
                    if f.label.text == "家具类型2":
                        floatData = float(f.data)
                        f.data = int(round(floatData % 1 * 100))
                utils.form_to_model(form, model)
                model.save()
                flash('修改成功')
            else:
                print("form.errorsform.errorsform.errorsform.errorsform.errorsform.errors:" + str(form.errors))
                utils.flash_errors(form)
    else:
        # 新增
        if form.validate_on_submit():
            model = DynamicModel()
            utils.form_to_model(form, model)
            model.save()
            flash('保存成功')
        else:
            utils.flash_errors(form)

    furType = 0
    furType2 = 0
    for f in form:
        if f.label.text == "家具类型1":
            furType = f.data
        if f.label.text == "家具类型2":
            if not f.data:
                furType2 = 0
            else:
                furType2 = f.data
            f.data = str("{:.2f}".format(int(furType) + int(furType2) * 0.01))
    global act
    global key
    global searchT
    global useSearch
    notifylist_url = url_for('main.notifylist', action=act, keyword=key, searchType=searchT) if useSearch else url_for('main.notifylist')
    
    
    return render_template(view, form=form, current_user=current_user,notifylist_url = notifylist_url,orDic = organizationsDic)

#更新选项
@main.route('/get_updated_choices/<furnitureType1>')
def get_updated_choices(furnitureType1):
    fTypeDic2 = {}
    for fff in furnitureTypeDic2.keys():
        if int(fff[0]) == int(furnitureType1):
            fTypeDic2["{:.2f}".format(int(fff[0]) + int(fff[1]) * 0.01)] = furnitureTypeDic2[fff];
    furnituresDataForm.update_furnitureType2_choices(fTypeDic2)
    # for f in fTypeDic2:
    #     print("key:" + str(f[0]) + "-------value:" + str(f[1]))
    return jsonify(choices=fTypeDic2)

# 根目录跳转
@main.route('/', methods=['GET'])
@login_required
def root():
    return redirect(url_for('main.index'))


# 首页
@main.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', current_user=current_user)


# 通知方式查询
@main.route('/notifylist', methods=['GET', 'POST'])
@login_required
def notifylist():
    return common_list(FurnituresData, 'notifylist.html')


# 通知方式配置
@main.route('/notifyedit', methods=['GET', 'POST'])
@login_required
def notifyedit():
    fTypeDic = {}
    for ff in furnitureTypeDic.keys():
        fTypeDic[str(ff)] = furnitureTypeDic[ff]
    fTypeDic2 = {}
    id = request.args.get('id', '')
    model = FurnituresData.get(FurnituresData.id == id)
    for fff in furnitureTypeDic2.keys():
        if int(fff[0]) == model.furnitureType:
            fTypeDic2["{:.2f}".format(int(fff[0]) + int(fff[1]) * 0.01)] = furnitureTypeDic2[fff]
    global furnituresDataForm
    furnituresDataForm = FurnituresDataForm(fTypeDic,fTypeDic2)
    
    return common_edit(FurnituresData, furnituresDataForm, 'notifyedit.html')
