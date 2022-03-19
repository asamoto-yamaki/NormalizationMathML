class NormalizationsController < ApplicationController
  def index
      #@normalization=Normalization.new
  end
#
#  def create
#      uploaded_file = fileupload_param[:file]
#      output_path = Rails.root.join('public', uploaded_file.original_filename)
#
#      File.open(output_path, 'w+b') do |fp|
#          fp.write  uploaded_file.read
#      end
#
#      redirect_to action: 'index'
#  end
#
#  private
#  def fileupload_param
#      params.require(:fileupload).permit(:file)
#  end
  
  def rule
#      @inputfile = params[:inputfile]
#      logger.debug("入力ファイル")
#      logger.debug(@inputfile)
#
#      if @rule.nil? == false then
#          require 'open3'
#          command = "/usr/local/bin/python3 /Users/yamakisumina/Desktop/修論/apps/NormalizationMathML/app/controllers/syuron_extract.py file " + @inputfile
#          o, e, s = Open3.capture3(command)
#          @kekka = o
#          logger.debug(@output)
#          logger.debug(e)
#          else
#          logger.debug("null")
#      end
      require 'open3'
      command = "/usr/local/bin/python3 " + Dir.pwd + "/app/controllers/syuron_extract.py file " + Dir.pwd + "/app/controllers/input.html"
      
      o, e, s = Open3.capture3(command)
      @kekka = o
      logger.debug(e)
      logger.debug("command")
      logger.debug(command)
      #@kekka = `/usr/local/bin/python3 /Users/yamakisumina/Desktop/修論/apps/NormalizationMathML/app/controllers/syuron_extract.py file /Users/yamakisumina/Desktop/修論/apps/NormalizationMathML/app/controllers/input.html`;
  end
  def conversion
      @rule_mi = params[:rule_mi]
      @rule_mi_multi = params[:rule_mi_multi]
      @rule_af_or_it = params[:rule_af_or_it]
      @rule_af_or_zahyou = params[:rule_af_or_zahyou]
      @rule_ip = params[:rule_ip]
      @rule_ic = params[:rule_ic]
      @rule_ic_mn = params[:rule_ic_mn]
      @rule_e = params[:rule_e]
      @rule_tenchi = params[:rule_tenchi]
      @rule_d = params[:rule_d]
      logger.debug("変換ルール")
      logger.debug(@rule_mi)
      logger.debug(@rule_mi_multi)
      logger.debug(@rule_af_or_it)
      logger.debug(@rule_af_or_zahyou)
      logger.debug(@rule_ip)
      logger.debug(@rule_ic)
      logger.debug(@rule_ic_mn)
      logger.debug(@rule_e)
      logger.debug(@rule_tenchi)
      
      if @rule_mi.nil? == false then
          require 'open3'
          command = "/usr/local/bin/python3 " + Dir.pwd + "/app/controllers/syuron_conversion.py file " + Dir.pwd + "/app/controllers/input.html " + @rule_mi + " " + @rule_mi_multi + " " + @rule_af_or_it + " " + @rule_af_or_zahyou + " " + @rule_ip + " " + @rule_ic + " " + @rule_ic_mn + " " + @rule_e + " " + @rule_tenchi + " " + @rule_d
          
          logger.debug("command")
          logger.debug(command)
          o, e, s = Open3.capture3(command)
          @output = o
          #logger.debug(@output)
          logger.debug(e)
      end
  end
  def download
    download_file_name = Dir.pwd + "/app/controllers/output.html"
    send_file download_file_name,type: 'application/octet-stream'
  end
  def downloadlog
    download_file_name = Dir.pwd + "/app/controllers/log.txt"
    send_file download_file_name,type: 'application/octet-stream'
  end
  
end
