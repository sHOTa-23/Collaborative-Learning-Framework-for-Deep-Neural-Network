file_list=("test_server_utils.py" "test_server.py" "test_versioning.py" "test_datahannel_count_average.py" "test_client.py" "test_datachannel_client.py")

for py_file in "${file_list[@]}"
do
    python3 ${py_file}
done