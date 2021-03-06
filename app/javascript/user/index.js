// This file is automatically compiled by Webpack, along with any other files
// present in this directory. You're encouraged to place your actual application logic in
// a relevant structure within app/javascript and only use these pack files to reference
// that code so it'll be compiled.

import Rails from "@rails/ujs"
import Turbolinks from "turbolinks"
import * as ActiveStorage from "@rails/activestorage"
import "channels"

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


Rails.start()
Turbolinks.start()
ActiveStorage.start()


