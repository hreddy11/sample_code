    <script>
        $(document).ready(function() {
            // Fetch and display GCS files
            $.get('/custom_ui/get_files', function(data) {
                var $fileList = $('#file-list');
                $fileList.empty();
                if (Array.isArray(data)) {
                    data.forEach(function(file) {
                        $fileList.append(`<li class="list-group-item">${file}</li>`);
                    });
                } else {
                    $fileList.append(`<li class="list-group-item">${data.message}</li>`);
                }
            });

            // Get table info
            $('#get-table-info').click(function() {
                var tableName = $('#table-dropdown').val();
                if (tableName) {
                    $.post('/custom_ui/get_table_info', JSON.stringify({table_name: tableName}), function(data) {
                        $('#table-info').text(data.table_info).show();
                        $('#trigger-dag').show();
                    }, 'json');
                }
            });

            // Trigger DAG
            $('#trigger-dag').click(function() {
                var tableName = $('#table-dropdown').val();
                $.post('/custom_ui/trigger_dag', JSON.stringify({dag_id: tableName + '_dag'}), function(data) {
                    alert(data.message);
                }, 'json');
            });
        });
    </script>
