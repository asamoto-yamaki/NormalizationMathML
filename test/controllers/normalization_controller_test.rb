require "test_helper"

class NormalizationControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get normalization_index_url
    assert_response :success
  end
end
