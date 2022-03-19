# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import os

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
    
else:
    print(mode)

#ログファイル作成
logfile = os.path.dirname(os.path.abspath(__file__)) + "/log.txt"

#変換ルールを引数で受け取る
rule_mi = sys.argv[3]
#rule_mi_multi = sys.argv[4]
#rule_mi_multi = [[0,1,3]] #変数の組み合わせルール
rule_mi_multi = sys.argv[4] #変数の組み合わせルール
rule_af_or_it = sys.argv[5]
rule_af_or_zahyou = sys.argv[6]
rule_ip = sys.argv[7]
rule_ic = sys.argv[8]
rule_ic_mn = sys.argv[9]
rule_e = sys.argv[10]
rule_tenchi = sys.argv[11]
rule_d = sys.argv[12]

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

#同じルールを適用できる箇所を並び替えた配列
rule_mi_arrange = []
rule_mi_multi_arrange = []
rule_mi_multi_arrange2 = []
rule_af_or_it_arrange = []
rule_af_or_zahyou_arrange = []
rule_ip_arrange = []
rule_ic_arrange = []
rule_ic_mn_arrange = []
rule_tenchi_arrange = []
rule_d_arrange = []
counter = -1

#並び替えをしたリスト
list_mi_henkan_arrange = []
str_mi_henkan_arrange = ""
list_af_or_it_arrange = []
str_af_or_it_arrange = ""
list_af_or_zahyou_arrange = []
str_af_or_zahyou_arrange = ""
list_ip_arrange = []
str_ip_arrange = ""
list_ic_arrange = []
str_ic_arrange = ""
list_ic_mn_arrange = []
str_ic_mn_arrange = ""
list_tenchi_arrange = []
str_tenchi_arrange = ""
list_d_arrange = []
str_d_arrange = ""


#並び替えを行う用のカウンター
counter_mi = 0
counter_af_or_it = 0
counter_af_or_zahyou = 0
counter_ip = 0
counter_ic = 0
counter_ic_mn = 0
counter_tenchi = 0
counter_d = 0

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
#moタグを抽出
list_mn = soup.find_all('mo')
            
#変数の変換が必要な箇所を抽出
for mi_text in list_mi_text:
    if len(mi_text) > 1:
        counter_mi += 1
        if len(list_mi_henkan) == 0:
            list_mi_henkan.append(mi_text)
            list_mi_henkan_arrange.append(str(counter_mi))
        else:
            find = 0
            #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
            for j in range(len(list_mi_henkan)):
                if list_mi_henkan[j] == mi_text:
                    list_mi_henkan_arrange[j] +=(str(counter_mi))
                    find = 1
                    break
            if find == 0:
                list_mi_henkan.append(mi_text)
                list_mi_henkan_arrange.append(str(counter_mi))
                
#同じ変換ルールを適用できる箇所がまとまっていたのを本来の順番に戻す
for mi_henkan_arrange in list_mi_henkan_arrange:
    str_mi_henkan_arrange += mi_henkan_arrange

#変数の変換ルールを並び替え
for i in range(len(str_mi_henkan_arrange)):
    num = int(str_mi_henkan_arrange[i])-1
    rule_mi_arrange.append(rule_mi[num])
    
#変数の組み合わせルールを数字のみの配列で並び替え
str1 = ""
for j in range(len(rule_mi_multi)):
    if rule_mi_multi[j] == ",":
        rule_mi_multi_arrange.append(str1)
        str1 = ""
    else:
        str1 += rule_mi_multi[j]

for i in range(len(str_mi_henkan_arrange)):
    num = int(str_mi_henkan_arrange[i])-1
    if rule_mi_multi_arrange[num] != "":
        rule_mi_multi_arrange2.append(rule_mi_multi_arrange[num])
        
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
    
    #微分
    if(mi.text == 'd'):
        find = 0
        element = str(mi)+str(list_next_mi[0])
        if len(list_d) == 0:
            counter_d += 1
            list_d_arrange.append(str(counter_d))
        else:
            #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
            for j in range(len(list_d)):
                if list_d[j] == element:
                    list_d_arrange[j] +=(str(counter_d))
                    find = 1
                    break
            if find == 0:
                counter_d += 1
                list_d_arrange.append(str(counter_d))
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
        #mrowが使われていたら省く
        if  mi.parent.name != 'msub' and mi.parent.parent.name != 'msub': #行列の成分の場合は除外
            if list_next_mi[0].name == 'mrow':
                list_next_mi_not_mrow = list_next_mi[0].contents #mrowの子のタグを取得
                list_next_mi_not_mrow = [i for i in list_next_mi_not_mrow if i != '\n'] #改行を削除
            else:
                list_next_mi_not_mrow = list_next_mi #miの兄弟
            
            #関数か乗算
            if mi.parent.name != 'mfenced' and list_next_mi_not_mrow[0].name == 'mi' and mi_af_true == 1:
                find = 0
                if len(list_af_or_it) == 0:
                    #list_af_or_it.append(element)
                    #list_af_or_it_num.append(1)
                    counter_af_or_it += 1
                    list_af_or_it_arrange.append(str(counter_af_or_it))
                else:
                    #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                    for j in range(len(list_af_or_it)):
                        if list_af_or_it[j] == element:
                            #list_af_or_it_num[j] += 1
                            list_af_or_it_arrange[j] +=(str(counter_af_or_it))
                            find = 1
                            break
                    if find == 0:
                        #list_af_or_it.append(element)
                        #list_af_or_it_num.append(1)
                        counter_af_or_it += 1
                        list_af_or_it_arrange.append(str(counter_af_or_it))
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
                        #list_af_or_zahyou.append(element)
                        #list_af_or_zahyou_num.append(1)
                        counter_af_or_zahyou += 1
                        list_af_or_zahyou_arrange.append(str(counter_af_or_zahyou))
                    else:
                        #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                        for j in range(len(list_af_or_zahyou)):
                            if list_af_or_zahyou[j] == element:
                                #list_af_or_zahyou_num[j] += 1
                                list_af_or_zahyou_arrange[j] +=(str(counter_af_or_zahyou))
                                find = 1
                                break
                        if find == 0:
                            #list_af_or_zahyou.append(element)
                            #list_af_or_zahyou_num.append(1)
                            counter_af_or_zahyou += 1
                            list_af_or_zahyou_arrange.append(str(counter_af_or_zahyou))
                #関数か乗算
                elif len(list_child_mfenced) == 1:
                    #print('\n')
                    #print(list_next_mi_not_mrow[0])
                    find = 0
                    if len(list_af_or_it) == 0:
                        #list_af_or_it.append(element)
                        #list_af_or_it_num.append(1)
                        counter_af_or_it += 1
                        list_af_or_it_arrange.append(str(counter_af_or_it))
                    else:
                        #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                        for j in range(len(list_af_or_it)):
                            if list_af_or_it[j] == element:
                                #list_af_or_it_num[j] += 1
                                list_af_or_it_arrange[j] +=(str(counter_af_or_it))
                                find = 1
                                break
                        if find == 0:
                            #list_af_or_it.append(element)
                            #list_af_or_it_num.append(1)
                            counter_af_or_it += 1
                            list_af_or_it_arrange.append(str(counter_af_or_it))
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
                            #list_af_or_zahyou.append(element)
                            #list_af_or_zahyou_num.append(1)
                            counter_af_or_zahyou += 1
                            list_af_or_zahyou_arrange.append(str(counter_af_or_zahyou))
                        else:
                            #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                            for j in range(len(list_af_or_zahyou)):
                                if list_af_or_zahyou[j] == element:
                                    #list_af_or_zahyou_num[j] += 1
                                    list_af_or_zahyou_arrange[j] +=(str(counter_af_or_zahyou))
                                    find = 1
                                    break
                            if find == 0:
                                #list_af_or_zahyou.append(element)
                                #list_af_or_zahyou_num.append(1)
                                counter_af_or_zahyou += 1
                                list_af_or_zahyou_arrange.append(str(counter_af_or_zahyou))
                        break
                #関数か乗算
                if af_or_zahyou_true == 0:
                    find = 0
                    if len(list_af_or_it) == 0:
                        #list_af_or_it.append(element)
                        #list_af_or_it_num.append(1)
                        counter_af_or_it += 1
                        list_af_or_it_arrange.append(str(counter_af_or_it))
                    else:
                        #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                        for j in range(len(list_af_or_it)):
                            if list_af_or_it[j] == element:
                                #list_af_or_it_num[j] += 1
                                list_af_or_it_arrange[j] +=(str(counter_af_or_it))
                                find = 1
                                break
                        if find == 0:
                            #list_af_or_it.append(element)
                            #list_af_or_it_num.append(1)
                            counter_af_or_it += 1
                            list_af_or_it_arrange.append(str(counter_af_or_it))
        
        #関数か乗算（底が記述されている対数関数logの場合）
        list_next_msub = [tag for tag in mi.parent.next_siblings] #同じ階層の後ろのタグを取得
        list_next_msub = [i for i in list_next_msub if i != '\n'] #改行を削除
        if mi.text == 'log' and mi.parent.name == 'msub' and len(list_next_msub) > 0:
            element = str(mi.parent)
            element += str(list_next_msub[0])
            element = element.replace('\n','')
            
            find = 0
            if len(list_af_or_it) == 0:
                counter_af_or_it += 1
                list_af_or_it_arrange.append(str(counter_af_or_it))
            else:
                #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                for j in range(len(list_af_or_it)):
                    if list_af_or_it[j] == element:
                        list_af_or_it_arrange[j] +=(str(counter_af_or_it))
                        find = 1
                        break
                if find == 0:
                    counter_af_or_it += 1
                    list_af_or_it_arrange.append(str(counter_af_or_it))
                    
              
#InvisiblePlusの挿入箇所抽出
for mn in list_mn:
    list_next_mn = [tag for tag in mn.next_siblings] #同じ階層の後ろのタグを取得
    list_next_mn = [i for i in list_next_mn if i != '\n'] #改行を削除
    if len(list_next_mn) > 0:
        if list_next_mn[0].name == 'mfrac':
            element = str(mn) + str(list_next_mn[0]).replace('\n','')
            find = 0
            if len(list_ip) == 0:
                #list_ip.append(element)
                #list_ip_num.append(1)
                counter_ip += 1
                list_ip_arrange.append(str(counter_ip))
                
            else:
                #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                for j in range(len(list_ip)):
                    if list_ip[j] == element:
                        #list_ip_num[j] += 1
                        list_ip_arrange[j] +=(str(counter_ip))
                        find = 1
                        break
                if find == 0:
                    #list_ip.append(element)
                    #list_ip_num.append(1)
                    counter_ip += 1
                    list_ip_arrange.append(str(counter_ip))
                    
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
                counter_ic += 1
                list_ic_arrange.append(str(counter_ic))
            else:
                #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                for j in range(len(list_ic)):
                    if list_ic[j] == element:
                        list_ic_arrange[j] +=(str(counter_ic))
                        find = 1
                        break
                if find == 0:
                    counter_ic += 1
                    list_ic_arrange.append(str(counter_ic))
                    
            #mrowの要素が1つかつ３文字以上のmnの場合
            if len(list_child_mrow) == 1 and len(list_child_mrow[0].string) > 2 and list_child_mrow[0].name == 'mn':
                element = list_child_mrow[0].string.replace('\n','')
                find = 0
                if len(list_ic_mn) == 0:
                    counter_ic_mn += 1
                    list_ic_mn_arrange.append(str(counter_ic))
                else:
                    #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
                    for j in range(len(list_ic_mn)):
                        if list_ic_mn[j] == element:
                            list_ic_mn_arrange[j] +=(str(counter_ic_mn))
                            find = 1
                            break
                    if find == 0:
                        counter_ic_mn += 1
                        list_ic_mn_arrange.append(str(counter_ic))
                        
#転置行列
for msup in list_msup:
    list_child_msup = msup.contents #子のタグを取得
    list_child_msup = [i for i in list_child_msup if i != '\n'] #改行を削除
    #t乗だったら
    if len(list_child_msup) == 2 and list_child_msup[1].name == 'mi' and (list_child_msup[1].string == 't' or list_child_msup[1].string == 'T'):
        element = msup
        find = 0
        if len(list_tenchi) == 0:
            counter_tenchi += 1
            list_tenchi_arrange.append(str(counter_tenchi))
        else:
            #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
            for j in range(len(list_tenchi)):
                if list_tenchi[j] == element:
                    list_tenchi_arrange[j] +=(str(counter_tenchi))
                    find = 1
                    break
                if find == 0:
                    counter_tenchi += 1
                    list_tenchi_arrange.append(str(counter_tenchi))

 

#変換ルールを並び替え
#関数か乗算
for af_or_it_arrange in list_af_or_it_arrange:
    str_af_or_it_arrange += af_or_it_arrange

for i in range(len(str_af_or_it_arrange)):
    num = int(str_af_or_it_arrange[i])-1
    rule_af_or_it_arrange.append(rule_af_or_it[num])

#関数か座標
for af_or_zahyou_arrange in list_af_or_zahyou_arrange:
    str_af_or_zahyou_arrange += af_or_zahyou_arrange

for i in range(len(str_af_or_zahyou_arrange)):
    num = int(str_af_or_zahyou_arrange[i])-1
    rule_af_or_zahyou_arrange.append(rule_af_or_zahyou[num])

#InvisiblePlus
for ip_arrange in list_ip_arrange:
    str_ip_arrange += ip_arrange

for i in range(len(str_ip_arrange)):
    num = int(str_ip_arrange[i])-1
    rule_ip_arrange.append(rule_ip[num])

#InvisibleComma
for ic_arrange in list_ic_arrange:
    str_ic_arrange += ic_arrange

for i in range(len(str_ic_arrange)):
    num = int(str_ic_arrange[i])-1
    rule_ic_arrange.append(rule_ic[num])

for ic_mn_arrange in list_ic_mn_arrange:
    str_ic_mn_arrange += ic_mn_arrange

for i in range(len(str_ic_mn_arrange)):
    num = int(str_ic_mn_arrange[i])-1
    rule_ic_mn_arrange.append(rule_ic[num])
    
#転置行列
for tenchi_arrange in list_tenchi_arrange:
    str_tenchi_arrange += tenchi_arrange

for i in range(len(str_tenchi_arrange)):
    num = int(str_tenchi_arrange[i])-1
    rule_tenchi_arrange.append(rule_tenchi[num])
    
#カウンターリセット
counter_mi = 0
counter_af_or_it = 0
counter_af_or_zahyou = 0
counter_ip = 0
counter_ic = 0
counter_ic_mn = 0
counter_e = 0
counter_tenchi = 0
counter_d = 0

#それぞれのmathタグに対する処理
for m in range(len(mathlist)):
    math = mathlist[m]
    mathsoup = BeautifulSoup(str(math), "html.parser")
    #タグのリストを作成
    list_mi = math.find_all('mi')
    list_mi_text = [tag.text for tag in math('mi')]
    list_mn = math.find_all('mn')
    list_msub = math.find_all('msub')
    list_msup = math.find_all('msup')
    list_mfenced = math.find_all('mfenced')
    list_mo = math.find_all('mo')
    #変数の変換
    str1 = ""
    j = 0
    rule_mi_multi_counter = 0
    for i in range(len(list_mi_text)):
        str1 = list_mi_text[i]
        parent_tag = list_mi[i].parent
        insert_counter = len([tag for tag in list_mi[i].previous_siblings])
        if len(str1) > 1:
            counter += 1
            #counter2 = 0
            #for num in list_mi_henkan_num:
            #    counter2 += num
             #   if counter <= num:
              #      break
                    
            #if list_mi_henkan_num[counter] != 1:
            if rule_mi_arrange[counter] != '0':
                #複数の変数として扱う
                #どこで変数を区切るかのルールを適用(何文字目を変数の先頭とするか、のリスト）
                #list = rule_mi_multi[counter]
                str2 = ''
                #変数が２文字だったら変数を区切る場所は一意なので勝手に変換する
                if len(str1) == 2:
                    #１文字目のタグを作成、挿入
                    print(2)
                    newtag = soup.new_tag('mi')
                    newtag.string = str1[0]  # タグのテキストを設定
                    parent_tag.insert(insert_counter, newtag)  # 0番目の位置にタグを挿入
                    insert_counter += 1
                    
                    #２文字目のタグを作成、挿入
                    newtag = soup.new_tag('mi')
                    newtag.string = str1[1]  # タグのテキストを設定
                    parent_tag.insert(insert_counter, newtag)  # 0番目の位置にタグを挿入
                    list_mi[i].decompose()
                    
                    print(str1)
                    #ログ出力
                    message = "mathタグ"+str(m+1)+"箇所目:文字"+str1+"を"+str(str1[0])+"と"+str(str1[1])+"に分割しました。\n"
                    with open(logfile, mode='a') as l:
                        l.write(message)
                        
                #変数が３文字以上だったら変換ルールに従って区切る
                else:
                    #for j in range(len(rule_mi_multi_arrange2[rule_mi_multi_counter])):
                    for k in range(len(str1)):
#                        print(rule_mi_multi_arrange2)
#                        print(rule_mi_multi_counter)
                        message = "mathタグ"+str(m+1)+"箇所目:文字"+str1+"を"
                        if len(rule_mi_multi_arrange2[rule_mi_multi_counter]) > j:
                            if str(k) == rule_mi_multi_arrange2[rule_mi_multi_counter][j]:
                                #print(rule_mi_multi_arrange2[rule_mi_multi_counter][j])
                                #タグを作成、挿入
                                newtag = soup.new_tag('mi')
                                newtag.string = str2  # タグのテキストを設定
                                parent_tag.insert(insert_counter, newtag)  # 0番目の位置にタグを挿入
                                j += 1
                                insert_counter += 1
                                #ログ出力
                                message += str2 + "と"
                                    
                                str2 = ''
                                str2 += str1[k]
                            else:
                                str2 += str1[k]
                                
                            if k == len(str1)-1:
                                #タグを作成、挿入
                                newtag = soup.new_tag('mi')
                                newtag.string = str2  # タグのテキストを設定
                                parent_tag.insert(insert_counter, newtag)  # 0番目の位置にタグを挿入
                                j += 1
                                #ログ出力
                                message += str2
                        else:
                            str2 += str1[k]
                            if k == len(str1)-1:
                                #タグを作成、挿入
                                newtag = soup.new_tag('mi')
                                newtag.string = str2  # タグのテキストを設定
                                parent_tag.insert(insert_counter, newtag)  # 0番目の位置にタグを挿入
                                j += 1
                                
                                #ログ出力
                                message += str2
                    
                    rule_mi_multi_counter += 1
                    j = 0
                    #元のタグを削除
                    list_mi[i].decompose()
                    
                    #ログ出力
                    message += "に分割しました。\n"
                    with open(logfile, mode='a') as l:
                        l.write(message)
                    
    #見えない演算子の変換
    #InvisibleTimesかApplyFunctionの挿入
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
        
        #演算子の挿入を行うための変数
        parent_tag = mi.parent
        parent2_tag = parent_tag.parent
        insert_counter = len([tag for tag in mi.previous_siblings])
        
        #改行を挿入する際に使用
        new_line = soup.new_string("\n")
        
        #ネイピア数e
        if(mi.text == 'e'):
            #改行を挿入
            #parent_tag.insert(insert_counter+1, new_line)
            #変換
            if rule_e[counter_e] == str(0):
                #ApplyFunctionのタグを作成、挿入
                #newtag = soup.new_tag('mo')
                #newtag.string = "&ApplyFunction;"  # タグのテキストを設定
                mi.string = "&ExponentialE;"  # タグのテキストを設定
                #parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入

                #ログ出力
                message = "mathタグ"+str(m+1)+"箇所目:文字eをネイピア数に変換しました。\n"
                with open(logfile, mode='a') as l:
                    l.write(message)
            counter_e += 1;
                
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
            if  parent_tag.name != 'msub' and parent2_tag.name != 'msub':
                #mrowが使われていたら省く
                if list_next_mi[0].name == 'mrow':
                    list_next_mi_not_mrow = list_next_mi[0].contents #mrowの子のタグを取得
                    list_next_mi_not_mrow = [i for i in list_next_mi_not_mrow if i != '\n'] #改行を削除
                else:
                    list_next_mi_not_mrow = list_next_mi #miの兄弟
                
                #miが連続していたら勝手にInvisibleTimes挿入(微分の可能性がある場合はスルー）
                if list_next_mi_not_mrow[0].name == 'mi' and mi_af_true == 0 and mi.text != 'd':
                    print(mi)
                    #改行を挿入
                    parent_tag.insert(insert_counter+1, new_line)
                    #InvisibleTimesのタグを作成、挿入
                    newtag = soup.new_tag('mo')
                    newtag.string = "&InvisibleTimes;"  # タグのテキストを設定
                    parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入
                    
                    #ログ出力
                    message = "mathタグ"+str(m+1)+"箇所目:"+str(mi)+"の直後に「InvisibleTimes」を自動挿入しました。\n"
                    with open(logfile, mode='a') as l:
                        l.write(message)
                            
                #関数か乗算（三角関数、底が記述されていない対数関数logの場合）
                if parent_tag.name != 'mfenced' and list_next_mi_not_mrow[0].name == 'mi' and mi_af_true == 1:
                    #改行を挿入
                    parent_tag.insert(insert_counter+1, new_line)
                    #変換
                    if rule_af_or_it_arrange[counter_af_or_it] == str(0):
                        #ApplyFunctionのタグを作成、挿入
                        newtag = soup.new_tag('mo')
                        newtag.string = "&ApplyFunction;"  # タグのテキストを設定
                        parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入
                        
                        #ログ出力
                        message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「ApplyFunction」を挿入しました。\n"
                        with open(logfile, mode='a') as l:
                            l.write(message)
                    else:
                        #InvisibleTimesのタグを作成、挿入
                        newtag = soup.new_tag('mo')
                        newtag.string = "&InvisibleTimes;"  # タグのテキストを設定
                        parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入
                        
                        #ログ出力
                        message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「InvisibleTimes」を挿入しました。\n"
                        with open(logfile, mode='a') as l:
                            l.write(message)

                    counter_af_or_it += 1
        #
        #            find = 0
        #            if len(list_af_or_it) == 0:
        #                #list_af_or_it.append(element)
        #                #list_af_or_it_num.append(1)
        #                counter_af_or_it += 1
        #                list_af_or_it_arrange.append(str(counter_af_or_it))
        #            else:
        #                #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
        #                for j in range(len(list_af_or_it)):
        #                    if list_af_or_it[j] == element:
        #                        #list_af_or_it_num[j] += 1
        #                        list_af_or_it_arrange[j] +=(str(counter_af_or_it))
        #                        find = 1
        #                        break
        #                if find == 0:
        #                    #list_af_or_it.append(element)
        #                    #list_af_or_it_num.append(1)
        #                    counter_af_or_it += 1
        #                    list_af_or_it_arrange.append(str(counter_af_or_it))
                elif list_next_mi_not_mrow[0].name == 'mfenced':
                    list_child_mfenced = list_next_mi_not_mrow[0].contents #子のタグを取得
                    list_child_mfenced = [i for i in list_child_mfenced if i != '\n'] #改行を削除
                    #print('list_child_mfenced')
                    #print('\n')
                    #if len(list_child_mfenced) != 0:
                    #関数か座標
                    if len(list_child_mfenced) > 1:
                        #変換
                        if rule_af_or_zahyou_arrange[counter_af_or_zahyou] == str(0):
                            #改行を挿入
                            parent_tag.insert(insert_counter+1, new_line)
                            #ApplyFunctionのタグを作成、挿入
                            newtag = soup.new_tag('mo')
                            newtag.string = "&ApplyFunction;"  # タグのテキストを設定
                            parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入
                            
                            #ログ出力
                            message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「ApplyFunction」を挿入しました。\n"
                            with open(logfile, mode='a') as l:
                                l.write(message)
                        #座標だったら処理必要なし
                        counter_af_or_zahyou += 1
        #                find = 0
        #                if len(list_af_or_zahyou) == 0:
        #                    #list_af_or_zahyou.append(element)
        #                    #list_af_or_zahyou_num.append(1)
        #                    counter_af_or_zahyou += 1
        #                    list_af_or_zahyou_arrange.append(str(counter_af_or_zahyou))
        #                else:
        #                    #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
        #                    for j in range(len(list_af_or_zahyou)):
        #                        if list_af_or_zahyou[j] == element:
        #                            #list_af_or_zahyou_num[j] += 1
        #                            list_af_or_zahyou_arrange[j] +=(str(counter_af_or_zahyou))
        #                            find = 1
        #                            break
        #                    if find == 0:
        #                        #list_af_or_zahyou.append(element)
        #                        #list_af_or_zahyou_num.append(1)
        #                        counter_af_or_zahyou += 1
        #                        list_af_or_zahyou_arrange.append(str(counter_af_or_zahyou))
                    #関数か乗算
                    elif len(list_child_mfenced) == 1:
                        #改行を挿入
                        parent_tag.insert(insert_counter+1, new_line)
                        #変換
                        if rule_af_or_it_arrange[counter_af_or_it] == str(0):
                            #ApplyFunctionのタグを作成、挿入
                            newtag = soup.new_tag('mo')
                            newtag.string = "&ApplyFunction;"  # タグのテキストを設定
                            parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入
                            
                            #ログ出力
                            message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「ApplyFunction」を挿入しました。\n"
                            with open(logfile, mode='a') as l:
                                l.write(message)
                        else:
                            #InvisibleTimesのタグを作成、挿入
                            newtag = soup.new_tag('mo')
                            newtag.string = "&InvisibleTimes;"  # タグのテキストを設定
                            parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入
                            
                            #ログ出力
                            message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「InvisibleTimes」を挿入しました。\n"
                            with open(logfile, mode='a') as l:
                                l.write(message)

                        counter_af_or_it += 1
        #                find = 0
        #                if len(list_af_or_it) == 0:
        #                    #list_af_or_it.append(element)
        #                    #list_af_or_it_num.append(1)
        #                    counter_af_or_it += 1
        #                    list_af_or_it_arrange.append(str(counter_af_or_it))
        #                else:
        #                    #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
        #                    for j in range(len(list_af_or_it)):
        #                        if list_af_or_it[j] == element:
        #                            #list_af_or_it_num[j] += 1
        #                            list_af_or_it_arrange[j] +=(str(counter_af_or_it))
        #                            find = 1
        #                            break
        #                    if find == 0:
        #                        #list_af_or_it.append(element)
        #                        #list_af_or_it_num.append(1)
        #                        counter_af_or_it += 1
        #                        list_af_or_it_arrange.append(str(counter_af_or_it))
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
                            #変換
                            if rule_af_or_zahyou_arrange[counter_af_or_zahyou] == str(0):
                                #改行を挿入
                                parent_tag.insert(insert_counter+1, new_line)
                                #ApplyFunctionのタグを作成、挿入
                                newtag = soup.new_tag('mo')
                                newtag.string = "&ApplyFunction;"  # タグのテキストを設定
                                parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入
                                
                                #ログ出力
                                message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「ApplyFunction」を挿入しました。\n"
                                with open(logfile, mode='a') as l:
                                    l.write(message)
                            #座標だったら処理必要なし
                             
                            counter_af_or_zahyou += 1
        #                    find = 0
        #                    if len(list_af_or_zahyou) == 0:
        #                        #list_af_or_zahyou.append(element)
        #                        #list_af_or_zahyou_num.append(1)
        #                        counter_af_or_zahyou += 1
        #                        list_af_or_zahyou_arrange.append(str(counter_af_or_zahyou))
        #                    else:
        #                        #すでに同じ変換ルールを適用できる箇所が抽出されているかどうか
        #                        for j in range(len(list_af_or_zahyou)):
        #                            if list_af_or_zahyou[j] == element:
        #                                #list_af_or_zahyou_num[j] += 1
        #                                list_af_or_zahyou_arrange[j] +=(str(counter_af_or_zahyou))
        #                                find = 1
        #                                break
        #                        if find == 0:
        #                            #list_af_or_zahyou.append(element)
        #                            #list_af_or_zahyou_num.append(1)
        #                            counter_af_or_zahyou += 1
        #                            list_af_or_zahyou_arrange.append(str(counter_af_or_zahyou))
                            break
                    #関数か乗算
                    if af_or_zahyou_true == 0:
                        #改行を挿入
                        parent_tag.insert(insert_counter+1, new_line)
                        #変換
                        if rule_af_or_it_arrange[counter_af_or_it] == str(0):
                            #ApplyFunctionのタグを作成、挿入
                            newtag = soup.new_tag('mo')
                            newtag.string = "&ApplyFunction;"  # タグのテキストを設定
                            parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入
                            
                            #ログ出力
                            message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「ApplyFunction」を挿入しました。\n"
                            with open(logfile, mode='a') as l:
                                l.write(message)
                        else:
                            #InvisibleTimesのタグを作成、挿入
                            newtag = soup.new_tag('mo')
                            newtag.string = "&InvisibleTimes;"  # タグのテキストを設定
                            parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入
                            
                            #ログ出力
                            message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「InvisibleTimes」を挿入しました。\n"
                            with open(logfile, mode='a') as l:
                                l.write(message)

                        counter_af_or_it += 1
            
            #関数か乗算（底が記述されている対数関数logの場合）
            list_next_msub = [tag for tag in parent_tag.next_siblings] #同じ階層の後ろのタグを取得
            list_next_msub = [i for i in list_next_msub if i != '\n'] #改行を削除
            if mi.text == 'log' and mi.parent.name == 'msub' and len(list_next_msub) > 0:
                #変換
                if rule_af_or_it_arrange[counter_af_or_it] == str(0):
                    #ApplyFunctionのタグを作成、挿入
                    newtag = soup.new_tag('mo')
                    newtag.string = "&ApplyFunction;"  # タグのテキストを設定
                    parent_tag.insert_after(newtag)  # 0番目の位置にタグを挿入
                    
                    #ログ出力
                    message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「ApplyFunction」を挿入しました。\n"
                    with open(logfile, mode='a') as l:
                        l.write(message)
                else:
                    #InvisibleTimesのタグを作成、挿入
                    newtag = soup.new_tag('mo')
                    newtag.string = "&InvisibleTimes;"  # タグのテキストを設定
                    parent_tag.insert_after(newtag)  # 0番目の位置にタグを挿入
                    
                    #ログ出力
                    message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「InvisibleTimes」を挿入しました。\n"
                    with open(logfile, mode='a') as l:
                        l.write(message)
                #改行を挿入
                parent_tag.insert_after(new_line)

                counter_af_or_it += 1
        
        #微分
        if(mi.text == 'd'):
            #改行を挿入
            #parent_tag.insert(insert_counter+1, new_line)
            #変換
            
            if rule_d[counter_d] == str(0):
                print(counter_d)
                #DifferentialDのタグを作成、挿入
                newtag = soup.new_tag('mo')
                newtag.string = "&DifferentialD;"  # タグのテキストを設定
                parent_tag.insert(insert_counter+1, newtag)  # 0番目の位置にタグを挿入
                #元のmiタグを削除
                mi.decompose()

                #ログ出力
                message = "mathタグ"+str(m+1)+"箇所目:文字dを微分記号に変換しました。\n"
                with open(logfile, mode='a') as l:
                    l.write(message)
            counter_d += 1;
                        
                
                  
    #InvisiblePlusの挿入、<mn>と<mi>,かっこの間のInvisibleTimes挿入
    for mn in list_mn:
        list_next_mn = [tag for tag in mn.next_siblings] #同じ階層の後ろのタグを取得
        list_next_mn = [i for i in list_next_mn if i != '\n'] #改行を削除
        #演算子の挿入を行うための変数
        parent_tag = mn.parent
        insert_counter = len([tag for tag in mn.previous_siblings])
        new_line = soup.new_string("\n")
        
        if len(list_next_mn) > 0:
            if list_next_mn[0].name == 'mfrac':
                element = str(mn) + str(list_next_mn[0]).replace('\n','')
                #改行を挿入
                parent_tag.insert(insert_counter+1, new_line)
                #変換
                if rule_ip_arrange[counter_ip] == str(0):
                    #InvisiblePlusのタグを作成、挿入
                    #parent_tag.insert(insert_counter+1, new_line)
                    newtag = soup.new_tag('mo')
                    newtag.string = "&#x2064;"  # タグのテキストを設定
                    parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入
                    
                    #ログ出力
                    message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「InvisiblePlus」を挿入しました。\n"
                    with open(logfile, mode='a') as l:
                        l.write(message)
                else:
                    #InvisibleTimesのタグを作成、挿入
                    newtag = soup.new_tag('mo')
                    newtag.string = "&InvisibleTimes;"  # タグのテキストを設定
                    parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入
                    
                    #ログ出力
                    message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「InvisibleTimes」を挿入しました。\n"
                    with open(logfile, mode='a') as l:
                        l.write(message)
                
                counter_ip += 1
                
            #文字かかっこだったら勝手にInvisibleTimes挿入
            elif list_next_mn[0].name == 'mi' or list_next_mn[0].name == 'mfenced' or (list_next_mn[0].name == 'mo' and list_next_mn[0].string == '('):
                element = str(mn)
                #改行を挿入
                parent_tag.insert(insert_counter+1, new_line)
                #InvisibleTimesのタグを作成、挿入
                #parent_tag.insert(insert_counter+1, new_line)
                newtag = soup.new_tag('mo')
                newtag.string = "&InvisibleTimes;"  # タグのテキストを設定
                parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入
                
                #ログ出力
                message = "mathタグ"+str(m+1)+"箇所目:"+element+"の直後に「InvisibleTimes」を自動挿入しました。\n"
                with open(logfile, mode='a') as l:
                    l.write(message)
                
    #かっこの後に勝手にInvisibleTimesを勝手に挿入する
    for mfenced in list_mfenced:
        list_next_mfenced = [tag for tag in mfenced.next_siblings] #同じ階層の後ろのタグを取得
        list_next_mfenced = [i for i in list_next_mfenced if i != '\n'] #改行を削除
        
        parent_tag = mfenced.parent
        insert_counter = len([tag for tag in mfenced.previous_siblings])
        new_line = soup.new_string("\n")
        element = str(mfenced).replace('\n','')
        
        if len(list_next_mfenced) > 0:
            if list_next_mfenced[0].name == 'mn' or list_next_mfenced[0].name == 'mi' or list_next_mfenced[0].name == 'mfenced' or (list_next_mfenced[0].name == 'mo' and list_next_mfenced[0].string == '('):
                #改行を挿入
                parent_tag.insert(insert_counter+1, new_line)
                #InvisibleTimesのタグを作成、挿入
                #parent_tag.insert(insert_counter+1, new_line)
                newtag = soup.new_tag('mo')
                newtag.string = "&InvisibleTimes;"  # タグのテキストを設定
                parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入
                
                #ログ出力
                message = "mathタグ"+str(m+1)+"箇所目:"+element+"の直後に「InvisibleTimes」を自動挿入しました。\n"
                
                with open(logfile, mode='a') as l:
                    l.write(message)
    
    #かっこのうしろにInvisibleTimesを勝手に挿入
    for mo in list_mo:
        element = ""
        if mo.string == '(':
            list_next_mo = [tag for tag in mo.next_siblings] #同じ階層の後ろのタグを取得
            list_next_mo = [i for i in list_next_mo if i != '\n'] #改行を削除
            
            #print(mfenced)
            #print(str(list_next_mfenced))
            
            parent_tag = mo.parent
            new_line = soup.new_string("\n")
            fence = 1 #閉じていないかっこの数
            element += str(mo)
            
            for next_mo in list_next_mo:
                #かっこが閉じていない状態
                if fence != 0:
                    element += str(next_mo)
                    #新たなかっこが出てきたら
                    if next_mo.name == 'mo' and next_mo.string == '(':
                        fence += 1
                    #かっこが閉じられたら
                    if next_mo.name == 'mo' and next_mo.string == ')':
                        insert_counter = len([tag for tag in next_mo.previous_siblings])
                        fence -= 1
                #かっこが閉じている状態
                else:
                    #かっこが閉じてて、その後ろに変数、数字、かっこのどれかがあったら
                    if next_mo.name == 'mn' or next_mo.name == 'mi' or next_mo.name == 'mfenced' or (next_mo.name == 'mo' and next_mo.string == '('):
                        #改行を挿入
                        parent_tag.insert(insert_counter+1, new_line)
                        #InvisibleTimesのタグを作成、挿入
                        #parent_tag.insert(insert_counter+1, new_line)
                        newtag = soup.new_tag('mo')
                        newtag.string = "&InvisibleTimes;"  # タグのテキストを設定
                        parent_tag.insert(insert_counter+2, newtag)  # 0番目の位置にタグを挿入
                        
                        #ログ出力
                        message = "mathタグ"+str(m+1)+"箇所目:"+element+"の直後に「InvisibleTimes」を自動挿入しました。\n"
                        with open(logfile, mode='a') as l:
                            l.write(message)
                        break
                    #かっこの後ろが変数、数字、かっこ以外だったら
                    else:
                        break
                        
    #InvisibleCommaの挿入
    for msub in list_msub:
        list_child_msub = msub.contents #子のタグを取得
        list_child_msub = [i for i in list_child_msub if i != '\n'] #改行を削除
        #演算子の挿入を行うための変数
        parent_tag = list_child_msub[1]
        insert_counter = len([tag for tag in msub.previous_siblings])
        new_line = soup.new_string("\n")
        element = str(msub).replace('\n','')
        #print(list_child_msub)
        
        if list_child_msub[1].name == 'mrow':
            list_child_mrow = list_child_msub[1].contents #子のタグを取得
            list_child_mrow = [i for i in list_child_mrow if i != '\n'] #改行を削除
            original_mn = list_child_mrow[0].string
            #mrowの要素がmn1つかつ複数文字の場合
            if len(list_child_mrow) == 1 and len(original_mn) > 1 and list_child_mrow[0].name == 'mn':
                #mnの中身が2文字
                if len(list_child_mrow[0].string) == 2:
                    #改行を挿入
                    parent_tag.insert(2, new_line)
                    #変換
                    if rule_ic_arrange[counter_ic] == str(0):
                        #一つ目のmnタグを作成、挿入
                        newtag = soup.new_tag('mi')
                        newtag.string = original_mn[0]  # タグのテキストを設定
                        parent_tag.insert(1, newtag)  # 0番目の位置にタグを挿入
                        #改行を挿入
                        parent_tag.insert(2, new_line)
                        
                        #InvisibleCommaのタグを作成、挿入
                        newtag = soup.new_tag('mo')
                        newtag.string = "&InvisibleComma;"  # タグのテキストを設定
                        parent_tag.insert(4, newtag)  # 0番目の位置にタグを挿入
                        #改行を挿入
                        #parent_tag.insert(4, new_line)
                        
                        #一つ目のmnタグを作成、挿入
                        newtag = soup.new_tag('mi')
                        newtag.string = original_mn[1]  # タグのテキストを設定
                        parent_tag.insert(6, newtag)  # 0番目の位置にタグを挿入
                        #改行を挿入
                        #parent_tag.insert(6, new_line)
                        
                        #元のmnタグを削除
                        list_child_mrow[0].decompose()
                        
                        #ログ出力
                        message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「InvisibleComma」を挿入しました。\n"
                        with open(logfile, mode='a') as l:
                            l.write(message)
                    counter_ic += 1
                #mnの中身が2文字以上
                else:
                    #変換
                    if rule_ic_arrange[counter_ic] == str(0):
                        #１文字目のタグを作成、挿入
                        newtag = soup.new_tag('mi')
                        mn1 = ""
                        mn2 = ""
                        for i in range(int(rule_ic_mn[counter_ic_mn])):
                            mn1 += original_mn[i]  # タグのテキストを設定
                        newtag.string = mn1
                        parent_tag.insert(1, newtag)  # 0番目の位置にタグを挿入
                        #改行を挿入
                        parent_tag.insert(2, new_line)
                        
                        #InvisibleCommaのタグを作成、挿入
                        newtag = soup.new_tag('mo')
                        newtag.string = "&InvisibleComma;"  # タグのテキストを設定
                        parent_tag.insert(4, newtag)  # 0番目の位置にタグを挿入
                        #改行を挿入
                        #parent_tag.insert(4, new_line)
                        
                        #２文字目のタグを作成、挿入
                        newtag = soup.new_tag('mi')
                        for i in range(int(rule_ic_mn[counter_ic_mn]), len(original_mn)):
                            mn2 += original_mn[i]  # タグのテキストを設定
                        newtag.string = mn2
                        parent_tag.insert(6, newtag)  # 0番目の位置にタグを挿入
                        #改行を挿入
                        #parent_tag.insert(6, new_line)
                        
                        #元のmnタグを削除
                        list_child_mrow[0].decompose()
                        counter_ic_mn += 1
                        
                        #ログ出力
                        message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「InvisibleComma」を挿入しました。\n"
                        with open(logfile, mode='a') as l:
                            l.write(message)
                    counter_ic += 1
                    
            #mrowの要素が2つの場合
            if len(list_child_mrow) == 2:
            
                #mrowの要素のいずれかが数字以外
                if list_child_mrow[0].name != 'mn' or list_child_mrow[1].name != 'mn':
                    #改行を挿入
                    parent_tag.insert(2, new_line)
                    #変換
                    if rule_ic_arrange[counter_ic] == str(0):
                        #InvisibleCommaのタグを作成、挿入
                        newtag = soup.new_tag('mo')
                        newtag.string = "&InvisibleComma;"  # タグのテキストを設定
                        parent_tag.insert(3, newtag)  # 0番目の位置にタグを挿入
                        
                        #ログ出力
                        message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「InvisibleComma」を挿入しました。\n"
                        with open(logfile, mode='a') as l:
                            l.write(message)
                    else:
                        #InvisibleTimesのタグを作成、挿入
                        newtag = soup.new_tag('mo')
                        newtag.string = "&InvisibleTimes;"  # タグのテキストを設定
                        parent_tag.insert(3, newtag)  # 0番目の位置にタグを挿入
                        
                        #ログ出力
                        message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「InvisibleTimes」を挿入しました。\n"
                        with open(logfile, mode='a') as l:
                            l.write(message)
                    counter_ic += 1
                #mrowの要素が二つとも数字
                else:
                    #変換
                    #print("rule_ic_arrange="+str(rule_ic_arrange))
                    #print(counter_ic)
                    if rule_ic_arrange[counter_ic] == str(0):
                        #改行を挿入
                        parent_tag.insert(2, new_line)
                        #InvisibleCommaのタグを作成、挿入
                        newtag = soup.new_tag('mo')
                        newtag.string = "&InvisibleComma;"  # タグのテキストを設定
                        parent_tag.insert(3, newtag)  # 0番目の位置にタグを挿入
                        
                        #ログ出力
                        message = "mathタグ"+str(m+1)+"箇所目:"+element+"に「InvisibleComma」を挿入しました。\n"
                        with open(logfile, mode='a') as l:
                            l.write(message)
                    else:
                        #2つのmnタグを1つにまとめる
                        list_child_mrow[0].append(list_child_mrow[1].string)
                        #newtag = soup.new_tag('mn')
                        #newtag.string = list_child_mrow[0].string + list_child_mrow[1].string  # タグのテキストを設定
                        #parent_tag.insert(3, newtag)  # 0番目の位置にタグを挿入
                        list_child_mrow[1].extract()
                        list_child_mrow = list_child_msub[1].contents
                        list_child_mrow[2].extract()
                        
                        #ログ出力
                        message = "mathタグ"+str(m+1)+"箇所目:"+element+"の"+list_child_mrow[0].string+"を1つのタグにまとめました。\n"
                        with open(logfile, mode='a') as l:
                            l.write(message)
                    counter_ic += 1
                    
    #転置行列
    for msup in list_msup:
        list_child_msup = msup.contents #子のタグを取得
        list_child_msup = [i for i in list_child_msup if i != '\n'] #改行を削除
        #t乗だったら
        if len(list_child_msup) == 2 and list_child_msup[1].name == 'mi' and (list_child_msup[1].string == 't' or list_child_msup[1].string == 'T'):
            element = msup
            #変換
            if rule_tenchi_arrange[counter_tenchi] == str(0):
                #tのタグをmoに変える
                list_child_msup[1].decompose() #元々のタグを削除
                newtag = soup.new_tag('mo')
                newtag.string = "T"  # タグのテキストを設定
                msup.insert(3, newtag)  # 0番目の位置にタグを挿入
                
                #ログ出力
                message = "mathタグ"+str(m+1)+"箇所目:"+element+"を転置行列に変換しました。\n"
                with open(logfile, mode='a') as l:
                    l.write(message)
            counter_tenchi += 1;
        
#正規的な表現形式記述に変換
outputfile = os.path.dirname(os.path.abspath(__file__)) + "/output.html"
#html =soup.contents
#html = soup.prettify("utf-8")
with open(outputfile, mode='w') as f:
    f.write(str(soup.decode(formatter=None)))
with open(outputfile) as f:
    print(f.read())
