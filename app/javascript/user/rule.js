// This file is automatically compiled by Webpack, along with any other files
// present in this directory. You're encouraged to place your actual application logic in
// a relevant structure within app/javascript and only use these pack files to reference
// that code so it'll be compiled.

import Rails from "@rails/ujs"
import Turbolinks from "turbolinks"
import * as ActiveStorage from "@rails/activestorage"
import "channels"
/*
const kekka_str = @kekka;
let element_ste = "";
let list_counter = 0;
let element_change = 0;
let list_af_or_it = [];
let list_af_or_zahyou = [];
let list_ip = [];
let list_ic = [];
for (var i=0; i<kekka_str.length;i++){
    str_i = kekka_str.chartAt(i);
    if(str_i == '['){
	list_counter += 1;
    }else if(str_i == ','){
	element_change = 1;
    }
    else{
	if(list_counter == 1){
	    if(element_change == 0){
		element_str += str_i;
	    }else{
		list_af_or_it.push(element_str);
		element_str = "";
		element_change = 0;
	    }
	}else if(list_counter == 2){
	    list_af_or_zahyou.push(str_i);
	}else if(list_counter == 3){
	    list_ip.push(str_i);
	}else if(list_counter == 4){
	    list_ic.push(str_i);
	}
    }
}

var kekkalist = [];
kakkalist.push(@list_kekka);
console.log(kekkalist);
let str = 'a';
document.getElementById('str').innerHTML = str;
// input要素
const fileInput = document.getElementById('file');
// changeイベントで呼び出す関数
const handleFileSelect = () => {
  const files = fileInput.files;
  for (let i = 0; i < files.length; i++) {
    console.log(files[i]);
  }
  const reader = new FileReader();
    reader.onload = () => {
      console.log(reader.result);
      const pre = document.getElementById('pre1');
      pre.textContent = reader.result;
    };

    reader.readAsText(files[0]);

}
// ファイル選択時にhandleFileSelectを発火
fileInput.addEventListener('change', handleFileSelect);
*/

Rails.start()
Turbolinks.start()
ActiveStorage.start()


