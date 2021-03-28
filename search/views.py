from django.shortcuts import render, redirect
from .forms import SearchForm

import pandas as pd


def home(request):
    if request.method == 'GET':
        return render(request, 'search/search.html', {'form': SearchForm})
    sub = SearchForm()
    if request.method == 'POST':
        try:
            sub = SearchForm(request.POST)
            if sub.is_valid():
                term = sub.cleaned_data['isbn']
                return redirect('search:searchresult')
        except Exception as e:
            return render(request, 'search/search.html',
                          {'form': sub, 'error': 'Invalid Drug/Drug Not found, Please try again.'})
        return render(request, 'search/search.html', {'form': SearchForm})


def searchresult(request):
    string = request.POST.get('search')
    # PMBJP
    df = pd.read_excel('search/Product.xlsx')
    print("Data-frame loaded")
    df = df.rename(
        columns={'Drug Code': 'Drug_Code', 'Generic Name of the Medicine': 'Generic_Name', 'Unit Size': 'Unit_Size',
                 'Therapeutic Category': 'Therapeutic_Category'})
    print(request.POST.get('search'))
    drug_name = string
    df2 = df.loc[df['Generic_Name'].str.contains(drug_name, na=False), ['Generic_Name', 'MRP']]
    generic_names_list = df2['Generic_Name'].to_list()
    df2['MRP'] = df2['MRP'].astype(str)
    df2['MRP'] = df2['MRP'].str.replace(r'\n0', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n1', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n2', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n3', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n4', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n5', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n6', '')

    MRP_list = df2['MRP'].map(float).to_list()
    print(MRP_list)
    mylist = zip(generic_names_list, MRP_list)
    if not MRP_list:
        minName = 'N/A'
        minPrice = 'N/A'
    else:
        temp = min(MRP_list)
        res = [i for i, j in enumerate(MRP_list) if j == temp]
        minName = generic_names_list[res[0]]
        minPrice = MRP_list[res[0]]

    # Medicine Database
    df_brand = pd.read_excel('search/Sample.xlsx')

    drug_name = string
    df3 = df_brand.loc[
        df_brand['Salt'].str.contains(drug_name, na=False), ['Medicine Name', 'Salt', 'Manufacturer', 'MRP']]

    names_list = df3['Medicine Name'].to_list()
    manufacturer_list = df3['Manufacturer'].to_list()
    MRP_list1 = df3['MRP'].map(float).to_list()

    mylist1 = zip(names_list, manufacturer_list, MRP_list1)

    if not MRP_list1:
        minName1 = 'N/A'
        minPrice1 = 'N/A'
    else:
        temp = min(MRP_list1)
        res = [i for i, j in enumerate(MRP_list1) if j == temp]
        minName0 = names_list[res[0]]
        minName2 = manufacturer_list[res[0]]
        minName1 = minName0 + " " + minName2
        minPrice1 = MRP_list1[res[0]]

    if minPrice == 'N/A' or minPrice1 == 'N/A':
        bestname = 'N/A'
        bestsection = 'Data not sufficient'
        bestprice = 'N/A'
        savings = 0

    elif minPrice1 > minPrice:
        bestname = minName
        bestsection = 'Jan Aushadhi'
        bestprice = minPrice
        savings = ((minPrice1 - minPrice) / minPrice) * 100
        savings = format(savings, '.2f')



    else:
        bestname = minName1
        bestsection = 'Medicine Database'
        bestprice = minPrice1
        savings = ((minPrice - minPrice1) / minPrice1) * 100
        savings = format(savings, '.2f')

    data = {
        'list1': generic_names_list,
        'list2': MRP_list,
        'mylist': mylist,
        'minName': minName,
        'minPrice': minPrice,

        'list3': names_list,
        'list4': manufacturer_list,
        'list5': MRP_list1,
        'minName1': minName1,
        'minPrice1': minPrice1,
        'mylist1': mylist1,

        'bestname': bestname,
        'bestprice': bestprice,
        'bestsection': bestsection,
        'savings': savings,
    }
    return render(request, 'search/show.html', data)
