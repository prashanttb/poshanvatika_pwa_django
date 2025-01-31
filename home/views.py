from cmath import log
from django.core.exceptions import TooManyFieldsSent
from django.shortcuts import render
from .forms import CreateUserForm
import re
# from django.core.files import 
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import base64
import time
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


#login dependacies
from django.contrib.auth import login, authenticate #add this
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UploadPictureForm, UploadWellPictureForm,BasicPoshanForm
from .models import  UploadWellPictureModel, UploadPictureModel,PoshanInformation,PoshanFormInformation,BasicPoshanModel,CensusTable,AhmedSchoolForm
# Create your views here.
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
#for rendering the data from database 

# #compress image
# from io import BytesIO
# from PIL import Image
# from django.core.files.uploadedfile import InMemoryUploadedFile

def viewVatikas(request):
    wells = UploadWellPictureModel.objects.all()
    vatikas = UploadPictureModel.objects.all()
    vatikas1 = PoshanFormInformation.objects.all()
    vatikas2 = UploadPictureModel.objects.filter(type='AFIF')
    selfcons = PoshanFormInformation.objects.filter(level_nutri_garden='for_self_consumption',nutri_garden_scale ='Only for vegetables and fruits, Backyard Poultry')
    sellsurp = PoshanFormInformation.objects.filter(level_nutri_garden='selling_surplus')
    context = {'vatikas1': vatikas1,'vatikas2': vatikas2, 'vatikas':vatikas,'selfcons':selfcons,'sellsurp':sellsurp}
    # context = {'wells': wells, 'mylist':mylist}
    return render(request, 'home/viewVatikas.html', context )
    # return render(request, 'map/map.html', context)

# def viewVatikas(request):
#     # wells = UploadWellPictureModel.objects.all()
#     vatikas = UploadPictureModel.objects.all()
#     # vatikas1 = PoshanInformation.objects.all()
#     # vatikas1 = BasicPoshanModel.objects.all()
#     # selfcons = PoshanInformation.objects.filter(level_nutri_garden='for_self_consumption',nutri_garden_scale ='Only for vegetables and fruits, Backyard Poultry')
#     # sellsurp = PoshanInformation.objects.filter(level_nutri_garden='selling_surplus')
    
    # context = {'vatikas1': vatikas1}
    #  context = {'vatikas1': vatikas1, 'vatikas':vatikas,'selfcons':selfcons,'sellsurp':sellsurp} 
    # {'selfcons':selfcons,'sellsurp':sellsurp}
    # context = {'wells': wells, 'mylist':mylist}
    return render(request, 'home/viewVatikas.html', context )
    #return render(request, 'map/map.html', context)

def viewWells(request):
    wells = UploadWellPictureModel.objects.all()
    context = {'wells': wells}
    return render(request, 'home/viewWells.html',context)

def captwellpic(request):
    form = UploadWellPictureForm()
    global datauri
    if request.is_ajax():
        datauri = request.POST['picture']
    
    if request.method == 'POST' and not request.is_ajax():
        form = UploadWellPictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        name = request.POST.get('name')
        well_nm = request.POST.get('well_nm')
        radius = request.POST.get('radius')
        depth = request.POST.get('depth')
        level = request.POST.get('level')
        village = request.POST.get('village')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        try:
            imgstr = re.search(r'base64,(.*)', datauri).group(1)
            data = ContentFile(base64.b64decode(imgstr))
            myfile = "WellPics/profile-"+time.strftime("%Y%m%d-%H%M%S")+".png"
            fs = FileSystemStorage()
            filename = fs.save(myfile, data)
            picLocation = UploadWellPictureModel.objects.create(picture=filename, name=name, well_nm=well_nm, radius=radius, depth=depth, level=level, village=village, district=district, state=state,pincode=pincode, lat=lat, lng=lng)
            picLocation.save()
            datauri= False
            del datauri
        except NameError:
            print("Image is not captured")
    else:
        form = UploadWellPictureForm()
    return render(request,'home/captureWellPic.html',{})

# def uploadwellpic(request):
#     data = dict()
#     if "GET" == request.method:
#         return render(request,'home/uploadWellPic.html',{})
    
#     # process POST request
#     files = request.FILES  # multivalued dict
#     image = files.get("picture")
    
#     # compress the image here and then save it
#     i = Image.open(image)
#     thumb_io = BytesIO()
#     i.save(thumb_io, format='JPEG', quality=80)
#     inmemory_uploaded_file = InMemoryUploadedFile(thumb_io, None, 'foo.jpeg', 
#                                               'image/jpeg', thumb_io.tell(), None)

#     instance = UploadWellPictureModel()
#     instance.image = inmemory_uploaded_file
#     instance.save()
#     return render(request,'home/uploadWellPic.html',{})

def uploadwellpic(request):
    if request.method == 'POST':
        form = UploadWellPictureForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.save()
            messages.success(request, "Registration successful." )
            print("data is saved.")
            return redirect('/captwellpic')
    else:
        form = UploadWellPictureForm()
    return render(request,'home/uploadWellPic.html',{})

def captvatikapic(request):
    form = UploadPictureForm()
    global datauri
    if request.is_ajax():
        datauri = request.POST['picture']
    
    if request.method == 'POST' and not request.is_ajax():
        form = UploadPictureForm(request.POST, request.FILES)
        # if form.is_valid():
        #     form.save()
        name = request.POST.get('name')
        # nutri_nm = request.POST.get('nutri_nm')
        # area = request.POST.get('area')
        village = request.POST.get('village')
        # district = request.POST.get('district')
        state = request.POST.get('state')
        # pincode = request.POST.get('pincode')
        # lat = request.POST.get('lat')
        # lng = request.POST.get('lng')
        organization= request.POST.get('organization')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        self_made=request.POST.get('self_made')
        local_ngo = request.POST.get('local_ngo')
        external_support = request.POST.get('external_support')
        community_level= request.POST.get('community_level')
        school_level = request.POST.get('school_level')
        anganwadi = request.POST.get('anganwadi')
        others_nutri =request.POST.get('other_nutri')
        self_consumption=request.POST.get('self_consumption')
        selling_surplus = request.POST.get('selling_surplus')
        surplus_addition = request.POST.get('surplus_addition')
        others_level= request.POST.get('other_level')
        vegetable = request.POST.get('vegetable')
        backyard_poultry= request.POST.get('backyard_poultary')
        backyard_fishery =request.POST.get('backyard_fishery')
        others_scale =request.POST.get('other_scale')
        surplus = request.POST.get('surplus')
        income =request.POST.get('income') 
        one_to_fourthousand_sq= request.POST.get('one_to_fourthousand')
        seed_ngo = request.POST.get('seed_ngo')
        seasonal_vegetable = request.POST.get('seasonal_vegetable')
        fruitsgrown=request.POST.get('fruitgrown')
        dailyfruit=request.POST.get('dailyfruit')
        indigeous=request.POST.get('indigeous')
        open_cultivation= request.POST.get('open_cultivation')
        open_cultivation_multilayer= request.POST.get('open_cultivation_multilayer')
        protectcultivation_shed_net= request.POST.get('protectcultivation_shed_net')
        protectcultivation_shed_polyhouse=request.POST.get('protectcultivation_shed_polyhouse')
        cultivation_others = request.POST.get('cultivation_others')
        month= request.POST.get('month')
        well= request.POST.get('well')
        canel= request.POST.get('canel')
        bore_well=request.POST.get('bore_well')
        river =request.POST.get('river')
        source_water= request.POST.get('source_water')
        school_name=request.POST.get('school_name')
        any_weekly_class=request.POST.get('any_weekly_class')
        weekly=request.POST.get('weekly')
        any_innovative=request.POST.get('any_innovative')
        mid_day_meal = request.POST.get('mid_day_meal')
        surplus_selling= request.POST.get('surplus_selling')
        openfield_science_lab= request.POST.get('openfield_science_lab')
        hot_cooked_meal = request.POST.get('hot_cooked_meal')
        school_child = request.POST.get('school_child')
        school_scale = request.POST.get('school_scale')
        type=request.POST.get('type')

        try:
            imgstr = re.search(r'base64,(.*)', datauri).group(1)
            data = ContentFile(base64.b64decode(imgstr))
            myfile = "VatikaPics/profile-"+time.strftime("%Y%m%d-%H%M%S")+".png"
            fs = FileSystemStorage()
            filename = fs.save(myfile, data)
            # picLocation = UploadPictureModel.objects.create(picture=filename, name=name, nutri_nm=nutri_nm, area=area, village=village, district=district, state=state,pincode=pincode, lat=lat, lng=lng)
            picLocation = UploadPictureModel.objects.create(picture=filename,organization=organization,district=district,pincode=pincode,lat=lat,lng=lng,self_made=self_made,
                               local_ngo=local_ngo,external_support=external_support,
                               community_level=community_level,school_level=school_level,anganwadi=anganwadi,others_nutri=others_nutri,
                               self_consumption=self_consumption,selling_surplus=selling_surplus,surplus_addition=surplus_addition,
                               others_level=others_level,vegetable=vegetable,backyard_poultry=backyard_poultry,backyard_fishery=backyard_fishery,
                               others_scale=others_scale,surplus=surplus,income=income,one_to_fourthousand_sq=one_to_fourthousand_sq,
                               seed_ngo=seed_ngo,seasonal_vegetable=seasonal_vegetable,fruitsgrown=fruitsgrown,dailyfruit=dailyfruit,indigeous=indigeous,
                               open_cultivation=open_cultivation,open_cultivation_multilayer=open_cultivation_multilayer,
                               openfield_science_lab=openfield_science_lab,protectcultivation_shed_net=protectcultivation_shed_net,protectcultivation_shed_polyhouse=protectcultivation_shed_polyhouse,
                               cultivation_others=cultivation_others,month=month,well=well,canel=canel,bore_well=bore_well,river=river,
                               source_water=source_water,school_name=school_name,any_weekly_class=any_weekly_class,
                               weekly=weekly,any_innovative=any_innovative,mid_day_meal=mid_day_meal,surplus_selling=surplus_selling,
                               hot_cooked_meal=hot_cooked_meal,school_child=school_child,school_scale=school_scale,village=village,state=state,name=name,type=type)
            picLocation.save()
            datauri = False
            del datauri
        except NameError:
            print("Image is not captured")
    else:
        form = UploadPictureForm()
    return render(request,'home/captureVatikaPic.html',{})

    
def uploadvatikapic(request):
    if request.method == 'POST':
        form = UploadPictureForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.save()
            print("data is saved.")
            return redirect('/captvatikapic')
    else:
        form = UploadPictureForm()
    return render(request,"home/uploadVatikaPic.html",{'form': form})


def contact(request):
    return render(request,"home/contact.html",{})

def nurition(request):
    return render(request,"forms/nutritiongarden_info.html",{})

# def nutri(request):
#     return render(request,"forms/poshan.html",{})
def nutri(request):
    if request.method == 'POST':
        form = BasicPoshanForm(request.POST)
        # if form.is_valid():
        #     instance = form.save()
        #     instance.user = request.user
        #     instance.save()
        organization= request.POST.get('organization')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        self_made=request.POST.get('self_made')
        local_ngo = request.POST.get('local_ngo')
        external_support = request.POST.get('external_support')
        community_level= request.POST.get('community_level')
        school_level = request.POST.get('school_level')
        anganwadi = request.POST.get('anganwadi')
        others_nutri =request.POST.get('other_nutri')
        self_consumption=request.POST.get('self_consumption')
        selling_surplus = request.POST.get('selling_surplus')
        surplus_addition = request.POST.get('surplus_addition')
        others_level= request.POST.get('other_level')
        vegetable = request.POST.get('vegetable')
        backyard_poultry= request.POST.get('backyard_poultary')
        backyard_fishery =request.POST.get('backyard_fishery')
        others_scale =request.POST.get('other_scale')
        surplus = request.POST.get('surplus')
        income =request.POST.get('income') 
        one_to_fourthousand_sq= request.POST.get('one_to_fourthousand')
        seed_ngo = request.POST.get('seed_ngo')
        seasonal_vegetable = request.POST.get('seasonal_vegetable')
        fruitsgrown=request.POST.get('fruitgrown')
        dailyfruit=request.POST.get('dailyfruit')
        indigeous=request.POST.get('indigeous')
        open_cultivation= request.POST.get('open_cultivation')
        open_cultivation_multilayer= request.POST.get('open_cultivation_multilayer')
        protectcultivation_shed_net= request.POST.get('protectcultivation_shed_net')
        protectcultivation_shed_polyhouse=request.POST.get('protectcultivation_shed_polyhouse')
        cultivation_others = request.POST.get('cultivation_others')
        month= request.POST.get('month')
        well= request.POST.get('well')
        canel= request.POST.get('canel')
        bore_well=request.POST.get('bore_well')
        river =request.POST.get('river')
        source_water= request.POST.get('source_water')
        school_name=request.POST.get('school_name')
        any_weekly_class=request.POST.get('any_weekly_class')
        weekly=request.POST.get('weekly')
        any_innovative=request.POST.get('any_innovative')
        mid_day_meal = request.POST.get('mid_day_meal')
        surplus_selling= request.POST.get('surplus_selling')
        openfield_science_lab= request.POST.get('openfield_science_lab')
        hot_cooked_meal = request.POST.get('hot_cooked_meal')
        school_child = request.POST.get('school_child')
        school_scale = request.POST.get('school_scale')
        nutri=BasicPoshanModel(organization=organization,district=district,pincode=pincode,lat=lat,lng=lng,self_made=self_made,
                               local_ngo=local_ngo,external_support=external_support,
                               community_level=community_level,school_level=school_level,anganwadi=anganwadi,others_nutri=others_nutri,
                               self_consumption=self_consumption,selling_surplus=selling_surplus,surplus_addition=surplus_addition,
                               others_level=others_level,vegetable=vegetable,backyard_poultry=backyard_poultry,backyard_fishery=backyard_fishery,
                               others_scale=others_scale,surplus=surplus,income=income,one_to_fourthousand_sq=one_to_fourthousand_sq,
                               seed_ngo=seed_ngo,seasonal_vegetable=seasonal_vegetable,fruitsgrown=fruitsgrown,dailyfruit=dailyfruit,indigeous=indigeous,
                               open_cultivation=open_cultivation,open_cultivation_multilayer=open_cultivation_multilayer,
                               openfield_science_lab=openfield_science_lab,protectcultivation_shed_net=protectcultivation_shed_net,protectcultivation_shed_polyhouse=protectcultivation_shed_polyhouse,
                               cultivation_others=cultivation_others,month=month,well=well,canel=canel,bore_well=bore_well,river=river,
                               source_water=source_water,school_name=school_name,any_weekly_class=any_weekly_class,
                               weekly=weekly,any_innovative=any_innovative,mid_day_meal=mid_day_meal,surplus_selling=surplus_selling,
                               hot_cooked_meal=hot_cooked_meal,school_child=school_child,school_scale=school_scale)
        nutri.save()
        print("data is saved.")
        return redirect('/')
    else:
        form = BasicPoshanForm()
    return render(request,'forms/poshan.html',{'form':form})
def about(request):
    return render(request,"home/about.html",{})

def myPoshan(request):
    return render(request,"home/myPoshan.html",{})
def treecensus(request):
    tree = CensusTable.objects.all()
    tree_satara = CensusTable.objects.filter(name_of_the_ulb='Satara Municipal Council')
    tree_natepute = CensusTable.objects.filter(name_of_the_ulb='Natepute')
    tree_count = CensusTable.objects.count()
    tree_count_satara = CensusTable.objects.filter(name_of_the_ulb='Satara Municipal Council').count()
    tree_count_natepute = CensusTable.objects.filter(name_of_the_ulb='Natepute').count()
    context = {'tree':tree,'tree_count':tree_count,'tree_count_satara':tree_count_satara,'tree_count_natepute':tree_count_natepute,'tree_satara':tree_satara,'tree_natepute':tree_natepute}
    return render(request,"home/treecensus.html",context)
# def treecharts(request):
#     return render(request,"home/tree_census_charts.html",{})

def treecharts(request):
    census_table_csv_data = CensusTable.objects.all()
    


    df = pd.DataFrame(census_table_csv_data.values())
    
    # print(df.columns)
    # fig = px.histogram(df, x = 'name_of_the_ulb')
    # plt.xlabel('Number of Trees')
    # plt.ylabel('Cities')
    # # fig.write_image('static/charts/tree-city.png')
    # plt.close()
    
    
    # fig = px.histogram(df[df['tree_type']=='Indegenious'], x = 'name_of_the_ulb')
    # plt.xlabel('Number of Indegenious Trees')
    # plt.ylabel('Cities')
    # fig.write_image('static/charts/indegenious-city.png')
    # plt.close()
    
    # fig = px.bar(df, x='tree_common_name', y= 'total_area_in_sq_kms_under_all_trees')
    # plt.xlabel('Common Name of the tree')
    # plt.ylabel('Total are in sq kms under all tree')
    # plt.xticks(rotation=40)
    # fig.write_image('static/charts/tree-area.png')
    # plt.close()

    no_of_heritage_trees = len(df[df['current_tree_age'] >= 50])
    no_of_newly_planted_trees = len(df[df['current_tree_age'] <= 25])
    total_area_under_indegenious_trees = sum(df['total_area_in_sq_kms_under_native_indegeniuos_trees'].tolist())
    total_area_under_all_trees = sum(df['total_area_in_sq_kms_under_all_trees'].tolist())
    trees_under_govt_land = sum(df[df['tree_ownership_plantation_initiated_by'] == 'Government']['total_area_in_sq_kms_under_all_trees'].tolist())
    trees_under_private_land = sum(df[df['tree_ownership_plantation_initiated_by'] == 'Private']['total_area_in_sq_kms_under_all_trees'].tolist())
    trees_under_other_land = sum(df[df['tree_ownership_plantation_initiated_by'] == 'Others']['total_area_in_sq_kms_under_all_trees'].tolist())

    print(no_of_heritage_trees)
    print(no_of_newly_planted_trees)
    print(total_area_under_indegenious_trees)
    print(total_area_under_all_trees)
    print(trees_under_govt_land)
    print(trees_under_private_land)
    print(trees_under_other_land)

    total_trees = CensusTable.objects.all().count()
    total_indegenious_trees = CensusTable.objects.filter(tree_type='Indegenious').count()
    govt_trees = CensusTable.objects.filter(tree_ownership_plantation_initiated_by='Government').count()
    private_trees = CensusTable.objects.filter(tree_ownership_plantation_initiated_by='Private').count()
    other_trees = CensusTable.objects.filter(tree_ownership_plantation_initiated_by='Other').count()

    satara_total_trees = CensusTable.objects.filter(name_of_the_ulb='Satara Municipal Council').count()
    satara_total_indegenious_trees = CensusTable.objects.filter(name_of_the_ulb='Satara Municipal Council',tree_type='Indegenious').count()
    satara_govt_trees = CensusTable.objects.filter(name_of_the_ulb='Satara Municipal Council',tree_ownership_plantation_initiated_by='Government').count()
    satara_private_trees = CensusTable.objects.filter(name_of_the_ulb='Satara Municipal Council',tree_ownership_plantation_initiated_by='Private').count()
    satara_other_trees = CensusTable.objects.filter(name_of_the_ulb='Satara Municipal Council',tree_ownership_plantation_initiated_by='Other').count()

    natepute_total_trees = CensusTable.objects.filter(name_of_the_ulb='Natepute').count()
    natepute_total_indegenious_trees = CensusTable.objects.filter(name_of_the_ulb='Natepute',tree_type='Indegenious').count()
    natepute_govt_trees = CensusTable.objects.filter(name_of_the_ulb='Natepute',tree_ownership_plantation_initiated_by='Government').count()
    natepute_private_trees = CensusTable.objects.filter(name_of_the_ulb='Natepute',tree_ownership_plantation_initiated_by='Private').count()
    natepute_other_trees = CensusTable.objects.filter(name_of_the_ulb='Natepute',tree_ownership_plantation_initiated_by='Other').count()




    context = {
        'heritage_trees' : no_of_heritage_trees,
        'newly_planted_trees' : no_of_newly_planted_trees,
        'area_under_indegenious_trees' : total_area_under_indegenious_trees,
        'area_under_all_trees' : total_area_under_all_trees,
        'govt_land_trees' : trees_under_govt_land,
        'private_land_trees' : trees_under_private_land,
        'other_land_trees' : trees_under_other_land,
        'total_trees':total_trees,
        'total_indegenious_trees':total_indegenious_trees,
        'govt_trees':govt_trees,
        'private_trees':private_trees,
        'other_trees':other_trees,
        'satara_total_trees':satara_total_trees,
        'satara_total_indegenious_trees':satara_total_indegenious_trees,
        'satara_govt_trees':satara_govt_trees,
        'satara_private_trees':satara_private_trees,
        'satara_other_trees':satara_other_trees,
        'natepute_total_trees':natepute_total_trees,
        'natepute_total_indegenious_trees':natepute_total_indegenious_trees,
        'natepute_govt_trees':natepute_govt_trees,
        'natepute_private_trees':natepute_private_trees,
        'natepute_other_trees':natepute_other_trees

        }

    return render(request,'home/tree_census_charts.html', context)

def ahmednagar_schools(request):
    ahmed_sch = AhmedSchoolForm.objects.all()
    context = {'ahmed_sch':ahmed_sch}
    return render(request,"home/ahmednagar_schools.html",context)

def ahmed_sch_form(request):
    form = AhmedSchoolForm()
    if request.method == 'POST':
        form = AhmedSchoolForm(request.POST, request.FILES)
        # if form.is_valid():
        #     form.save()
        # name = request.POST.get('name')
        # form = CoalForm(request.POST, request.FILES)
        school_name = request.POST.get('school_name')
        lat=request.POST.get('lat')
        lng=request.POST.get('lng')
        ahmed_sch = AhmedSchoolForm.objects.create(school_name = school_name,lat=lat,lng=lng)
        ahmed_sch.save()
        messages.info(request, _(u'Your data is submitted successfully!'))
        # return HttpResponseRedirect(request.path_info)
        return redirect('/ahmed_sch_form')
           
    else:
        form = AhmedSchoolForm()
    return render(request,'home/ahmed_sch_form.html',{})


def basic(request):
    return render(request,"forms/basic_forms.html",{})

def news(request):
    return render(request,"home/news.html",{})
def howto(request):
    return render(request,"home/How-to.html",{})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, "You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="home/login.html", context={"login_form":form})


def logout(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')


def register_request(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for " + user)
            return redirect('login')
    context = {'form':form}
    return render(request, "home/register.html", context)