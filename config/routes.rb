Rails.application.routes.draw do
  get 'normalizations/index'
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/index.html
  get 'normalizations/rule'
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/rule.html
  get 'normalizations/conversion'
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/conversion.html
  get 'normalizations/download'
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/download.html
  get 'normalizations/downloadlog'
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/downloadlog.html
#    resources :normalizations, only: [index, :create, :rule, :conversion, :download]
end
