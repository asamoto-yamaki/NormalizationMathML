class CreateDirectors < ActiveRecord::Migration[6.1]
  def change
    create_table :directors do |t|
      t.string :upload_file_name
      t.binary :upload_file

      t.timestamps
    end
  end
end
