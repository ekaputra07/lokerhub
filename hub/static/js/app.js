// (C) LokerHub 2014
jQuery(document).ready(function($){

    var indeed_page = 1;
    var category = $('#indeed').data('category');
    var load_indeed = function(page){
        $('.loadmore .btn').text('Memuat...');
        $.post('/indeed/'+category+'/ajax/?page='+indeed_page, {csrfmiddlewaretoken: window.csrf_token}, function(resp){
            $('.loadmore').before(resp.html);
            if(!resp.next_page){
                $('.loadmore').hide();
            }else{
                indeed_page = resp.next_page;
                $('.loadmore .btn').text('Berikutnya');
            }
                
        });
    };

    if($('#indeed').length > 0){
        load_indeed();

        $('.loadmore .btn').click(function(){
            load_indeed();
        });
    }

});