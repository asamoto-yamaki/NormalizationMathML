# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys

#モードの設定
mode = sys.argv[1]

#HTMLファイルの読み込み


#ファイル入力の場合
if mode == "file" :
    inputfile = sys.argv[2]
    f = open(inputfile, mode="r")
    soup = BeautifulSoup(f, "html.parser")
    f.close()

#URL入力の場合
elif mode == "url":
    url = sys.argv[2]
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

#MathML部分を抽出
mathlist = soup.find_all('math')

#miタグとテキスト部分を抽出
list_mi = soup.find_all('mi')
list_mi_text = [tag.text for tag in soup('mi')]
#mnタグを抽出
list_mn = soup.find_all('mn')
#msubタグを抽出
list_msub = soup.find_all('msub')
#msupタグを抽出
list_msup = soup.find_all('msup')
#mfencedタグを抽出
list_mfenced = soup.find_all('mfenced')

#変換が必要な箇所のリスト
list_mi_henkan = []
list_af_or_it = []
list_af_or_zahyou = []
list_ip = []
list_ic = []
list_ic_mn = []
list_e = []
list_tenchi = []
list_d = []
#同じルールを適用できる箇所が何箇所あるかを格納するリスト
list_mi_henkan_num = []
list_af_or_it_num = []
list_af_or_zahyou_num = []
list_ip_num = []
list_ic_num = []
list_ic_mn_num = []
list_e_num = []
list_tenchi_num = []
list_d_num = []
#同じルールを適用できる箇所を並び替えた配列
rule_mi_arrange = []
list_mi_henkan_arrange = []
str_mi_henkan_arrange = ""
rule_mi_multi_arrange = []
rule_mi_multi_arrange2 = []
rule_af_or_it_arrange = []
rule_af_or_zahyou_arrange = []
rule_ip_arrange = []
rule_ic_arrange = []
rule_ic_mn_arrange = []

#変数の変換が必要な箇所を抽出
for mi_text in list_mi_text:
    if len(mi_text) > 1:
        if len(list_mi_henkan) == 0:
            list_mi_henkan.append(mi_text)
            list_mi_henkan_num.append(1)
        else:
            find = 0
            #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
            for j in range(len(list_mi_henkan)):
                if list_mi_henkan[j] == mi_text:
                    list_mi_henkan_num[j] += 1
                    find = 1
                    break
            if find == 0:
                list_mi_henkan.append(mi_text)
                list_mi_henkan_num.append(1)
    
#見えない演算子の挿入が必要な箇所を抽出
#InvisibleTimesかApplyFunctionの挿入箇所抽出
list_af_or_it = []
list_af_or_zahyou = []
list_mi_af = ["sin","cos","tan","sec","cosec","cot","log"]
for mi in list_mi:
    list_child_mfenced = []
    list_next_mi = [tag for tag in mi.next_siblings] #同じ階層の後ろのタグを取得
    list_next_mi = [i for i in list_next_mi if i != '\n'] #改行を削除
    #print(mi)
    #print('list_next_mi')
    #print(list_next_mi)
    #print('\n')
    #print(list_next_mi)
    
    #ネイピア数e
    if(mi.text == 'e'):
        if len(list_e) == 0:
            list_e.append(mi)
            list_e_num.append(1)
        else:
            list_e_num[0] += 1
            
    #微分
    if(mi.text == 'd'):
        find = 0
        element = str(mi)+str(list_next_mi[0])
        if len(list_d) == 0:
            list_d.append(element)
            list_d_num.append(1)
        else:
            #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
            for j in range(len(list_d)):
                if list_d[j] == element:
                    list_d_num[j] += 1
                    find = 1
                    break
            if find == 0:
                list_d.append(element)
                list_d_num.append(1)
            
    #miがsinなどかどうかチェック
    mi_af_true = 0
    for mi_af in list_mi_af:
        if mi.text ==mi_af:
            mi_af_true = 1
            
    if len(list_next_mi) != 0:
        element = str(mi)
        for next_mi in list_next_mi:
            element += str(next_mi)
        element = element.replace('\n','')
        #行列の成分の場合は除外
        if mi.parent.name != 'msub' and mi.parent.parent.name != 'msub':
            #mrowが使われていたら省く
            if list_next_mi[0].name == 'mrow':
                list_next_mi_not_mrow = list_next_mi[0].contents #mrowの子のタグを取得
                list_next_mi_not_mrow = [i for i in list_next_mi_not_mrow if i != '\n'] #改行を削除
            else:
                list_next_mi_not_mrow = list_next_mi #miの兄弟
    
            #関数か乗算（三角関数、底が記述されていない対数関数logの場合）
            if mi.parent.name != 'mfenced' and list_next_mi_not_mrow[0].name == 'mi' and mi_af_true == 1:
                find = 0
                if len(list_af_or_it) == 0:
                    list_af_or_it.append(element)
                    list_af_or_it_num.append(1)
                else:
                    #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                    for j in range(len(list_af_or_it)):
                        if list_af_or_it[j] == element:
                            list_af_or_it_num[j] += 1
                            find = 1
                            break
                    if find == 0:
                        list_af_or_it.append(element)
                        list_af_or_it_num.append(1)
            
            elif list_next_mi_not_mrow[0].name == 'mfenced':
                list_child_mfenced = list_next_mi_not_mrow[0].contents #子のタグを取得
                list_child_mfenced = [i for i in list_child_mfenced if i != '\n'] #改行を削除
                #print('list_child_mfenced')
                #print('\n')
                #if len(list_child_mfenced) != 0:
                #関数か座標
                if len(list_child_mfenced) > 1:
                    #print('\n')
                    #print(list_next_mi_not_mrow[0])
                    find = 0
                    if len(list_af_or_zahyou) == 0:
                        list_af_or_zahyou.append(element)
                        list_af_or_zahyou_num.append(1)
                    else:
                        #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                        for j in range(len(list_af_or_zahyou)):
                            if list_af_or_zahyou[j] == element:
                                list_af_or_zahyou_num[j] += 1
                                find = 1
                                break
                        if find == 0:
                            list_af_or_zahyou.append(element)
                            list_af_or_zahyou_num.append(1)
                #関数か乗算
                elif len(list_child_mfenced) == 1:
                    #print('\n')
                    #print(list_next_mi_not_mrow[0])
                    find = 0
                    if len(list_af_or_it) == 0:
                        list_af_or_it.append(element)
                        list_af_or_it_num.append(1)
                    else:
                        #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                        for j in range(len(list_af_or_it)):
                            if list_af_or_it[j] == element:
                                list_af_or_it_num[j] += 1
                                find = 1
                                break
                        if find == 0:
                            list_af_or_it.append(element)
                            list_af_or_it_num.append(1)
            elif list_next_mi_not_mrow[0].name =='mo' and list_next_mi_not_mrow[0].text =='(' and list_next_mi_not_mrow[-1].name =='mo' and list_next_mi_not_mrow[-1].text ==')':
                af_or_zahyou_true = 0
                for j in range(1,len(list_next_mi_not_mrow)):
                    str_mo = ''
                    #関数か座標
                    if list_next_mi_not_mrow[j].name == 'mo' and list_next_mi_not_mrow[j].text ==',':
                        af_or_zahyou_true = 1
                        for next_mi in list_next_mi_not_mrow:
                            str_mo += str(next_mi)
                        element = str(mi) + str_mo
                        find = 0
                        if len(list_af_or_zahyou) == 0:
                            list_af_or_zahyou.append(element)
                            list_af_or_zahyou_num.append(1)
                        else:
                            #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                            for j in range(len(list_af_or_zahyou)):
                                if list_af_or_zahyou[j] == element:
                                    list_af_or_zahyou_num[j] += 1
                                    find = 1
                                    break
                            if find == 0:
                                list_af_or_zahyou.append(element)
                                list_af_or_zahyou_num.append(1)
                        break
                #関数か乗算
                if af_or_zahyou_true == 0:
                    find = 0
                    if len(list_af_or_it) == 0:
                        list_af_or_it.append(element)
                        list_af_or_it_num.append(1)
                    else:
                        #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                        for j in range(len(list_af_or_it)):
                            if list_af_or_it[j] == element:
                                list_af_or_it_num[j] += 1
                                find = 1
                                break
                        if find == 0:
                            list_af_or_it.append(element)
                            list_af_or_it_num.append(1)
        #関数か乗算（底が記述されている対数関数logの場合）
        list_next_msub = [tag for tag in mi.parent.next_siblings] #同じ階層の後ろのタグを取得
        list_next_msub = [i for i in list_next_msub if i != '\n'] #改行を削除
        if mi.text == 'log' and mi.parent.name == 'msub' and len(list_next_msub) > 0:
            element = str(mi.parent)
            element += str(list_next_msub[0])
            element = element.replace('\n','')
            
            find = 0
            if len(list_af_or_it) == 0:
                list_af_or_it.append(element)
                list_af_or_it_num.append(1)
            else:
                #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                for j in range(len(list_af_or_it)):
                    if list_af_or_it[j] == element:
                        list_af_or_it_num[j] += 1
                        find = 1
                        break
                if find == 0:
                    list_af_or_it.append(element)
                    list_af_or_it_num.append(1)
                    
#mfencedの後にmo以外のいずれかがある場合はInvisibleTimesを挿入
#for mrow in list_mrow:
#    list_next_mrow = [tag for tag in mrow.next_siblings] #同じ階層の後ろのタグを取得
#    list_next_mrow = [i for i in list_next_mrow if i != '\n'] #改行を削除
#    if list_next_mrow[0] != 'mo'
#
                    
              
#InvisiblePlusの挿入箇所抽出
for mn in list_mn:
    list_next_mn = [tag for tag in mn.next_siblings] #同じ階層の後ろのタグを取得
    list_next_mn = [i for i in list_next_mn if i != '\n'] #改行を削除
    if len(list_next_mn) > 0:
        if list_next_mn[0].name == 'mfrac':
            element = str(mn) + str(list_next_mn[0]).replace('\n','')
            find = 0
            if len(list_ip) == 0:
                list_ip.append(element)
                list_ip_num.append(1)
            else:
                #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                for j in range(len(list_ip)):
                    if list_ip[j] == element:
                        list_ip_num[j] += 1
                        find = 1
                        break
                if find == 0:
                    list_ip.append(element)
                    list_ip_num.append(1)
                    
#InvisibleCommaの挿入箇所抽出
for msub in list_msub:
    list_child_msub = msub.contents #子のタグを取得
    list_child_msub = [i for i in list_child_msub if i != '\n'] #改行を削除
    #print(list_child_msub)
    if list_child_msub[1].name == 'mrow':
        list_child_mrow = list_child_msub[1].contents #子のタグを取得
        list_child_mrow = [i for i in list_child_mrow if i != '\n'] #改行を削除
        #mrowの要素が2つの場合または、1つかつ2文字以上のmnの場合（miの場合は変数の変換で処理されるので無視）
        if len(list_child_mrow) == 2 or (len(list_child_mrow) == 1 and len(list_child_mrow[0].string) > 1 and list_child_mrow[0].name == 'mn'):
            element = str(msub).replace('\n','')
            find = 0
            #InvisibleCommaを挿入するかどうか
            if len(list_ic) == 0:
                list_ic.append(element)
                list_ic_num.append(1)
            else:
                #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                for j in range(len(list_ic)):
                    if list_ic[j] == element:
                        list_ic_num[j] += 1
                        find = 1
                        break
                if find == 0:
                    list_ic.append(element)
                    list_ic_num.append(1)
                    
            #mrowの要素が1つかつ３文字以上のmnの場合
            if len(list_child_mrow) == 1 and len(list_child_mrow[0].string) > 2 and list_child_mrow[0].name == 'mn':
                element = list_child_mrow[0].string.replace('\n','')
                find = 0
                if len(list_ic_mn) == 0:
                    list_ic_mn.append(element)
                    list_ic_mn_num.append(1)
                else:
                    #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                    for j in range(len(list_ic_mn)):
                        if list_ic_mn[j] == element:
                            list_ic_mn_num[j] += 1
                            find = 1
                            break
                    if find == 0:
                        list_ic_mn.append(element)
                        list_ic_mn_num.append(1)
            else:
                list_ic_mn.append(0)
                list_ic_mn_num.append(0)
                
#転置行列
for msup in list_msup:
    list_child_msup = msup.contents #子のタグを取得
    list_child_msup = [i for i in list_child_msup if i != '\n'] #改行を削除
    #t乗だったら
    if len(list_child_msup) == 2 and list_child_msup[1].name == 'mi' and (list_child_msup[1].string == 't' or list_child_msup[1].string == 'T'):
        element = msup
        find = 0
        if len(list_tenchi) == 0:
            list_tenchi.append(element)
            list_tenchi_num.append(1)
        else:
            #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
            for j in range(len(list_tenchi)):
                if list_tenchi[j] == element:
                    list_tenchi_num[j] += 1
                    find = 1
                    break
            if find == 0:
                list_tenchi.append(element)
                list_tenchi_num.append(1)
        
print(str(list_mi_henkan).replace("'",""))
print(str(list_mi_henkan_num).replace("'",""))
print(str(list_af_or_it).replace("'",""))
print(str(list_af_or_it_num).replace("'",""))
print(str(list_af_or_zahyou).replace("'",""))
print(str(list_af_or_zahyou_num).replace("'",""))
print(str(list_ip).replace("'",""))
print(str(list_ip_num).replace("'",""))
print(str(list_ic).replace("'",""))
print(str(list_ic_num).replace("'",""))
print(str(list_ic_mn).replace("'",""))
print(str(list_ic_mn_num).replace("'",""))
print(str(list_e).replace("'",""))
print(str(list_e_num).replace("'",""))
print(str(list_tenchi).replace("'",""))
print(str(list_tenchi_num).replace("'",""))
print(str(list_d).replace("'",""))
print(str(list_d_num).replace("'",""))



